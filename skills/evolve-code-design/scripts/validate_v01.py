#!/usr/bin/env python3
"""Validate v0.1 records; use JSON Schema when available, otherwise a guarded schema subset."""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing dependency: yaml. Requires PyYAML.", file=sys.stderr)
    sys.exit(2)

try:
    from jsonschema import Draft2020Validator
except ImportError:
    Draft2020Validator = None

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    "manifest": ROOT / "assets" / "change-manifest.schema.yaml",
    "knowledge": ROOT / "assets" / "knowledge-record.schema.yaml",
}
PASS_STATES = {"passed", "passed_with_limitations"}
AUTHORIZED_STATES = {"Authorized", "Implementing", "Validating", "Completed"}
STRUCTURAL_FEEDBACK = {"responsibility_boundary", "abstraction_boundary", "concept_boundary", "architecture"}
PREFIX_BY_KIND = {
    "constraint": "C-",
    "assumption": "A-",
    "decision_reference": "D-",
    "design_fact": "K-",
    "quality_preference": "Q-",
}
INACTIVE_LIFECYCLES = {"resolved", "invalidated", "expired", "superseded"}
RISK_AUTHORIZATION = {
    "database_migration": "migration",
    "compatibility_change": "compatibility_change",
    "production_operation": "production_operation",
    "security_change": "security_change",
}
SUPPORTED_SCHEMA_KEYWORDS = {
    "$schema", "$id", "$defs", "$ref", "title", "description", "type", "required",
    "properties", "additionalProperties", "items", "uniqueItems", "enum", "const",
    "pattern", "minLength", "allOf", "if", "then", "else",
}


def load_yaml(path):
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def unsupported_keyword_errors(schema):
    errors = []

    def visit(node, path):
        if not isinstance(node, dict):
            return
        for keyword in node:
            if keyword not in SUPPORTED_SCHEMA_KEYWORDS:
                errors.append(f"{path}: unsupported schema keyword {keyword!r} in fallback validator")
        for container in ("$defs", "properties"):
            for name, subschema in node.get(container, {}).items():
                visit(subschema, f"{path}.{container}.{name}")
        for keyword in ("items", "additionalProperties", "if", "then", "else"):
            subschema = node.get(keyword)
            if isinstance(subschema, dict):
                visit(subschema, f"{path}.{keyword}")
            elif keyword == "items" and isinstance(subschema, list):
                errors.append(f"{path}.items: array-form items is unsupported in fallback validator")
        for index, subschema in enumerate(node.get("allOf", [])):
            visit(subschema, f"{path}.allOf[{index}]")

    visit(schema, "$")
    return errors


def resolve_ref(root, reference):
    if not reference.startswith("#/"):
        raise ValueError(f"Only local schema references are supported: {reference}")
    node = root
    for raw_part in reference[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        node = node[part]
    return node


def matches_type(instance, expected):
    checks = {
        "object": lambda value: isinstance(value, dict),
        "array": lambda value: isinstance(value, list),
        "string": lambda value: isinstance(value, str),
        "null": lambda value: value is None,
        "boolean": lambda value: isinstance(value, bool),
        "number": lambda value: isinstance(value, (int, float)) and not isinstance(value, bool),
        "integer": lambda value: isinstance(value, int) and not isinstance(value, bool),
    }
    expected_types = [expected] if isinstance(expected, str) else expected
    return any(checks[item](instance) for item in expected_types)


def validate_node(instance, schema, root, path, errors):
    if "$ref" in schema:
        validate_node(instance, resolve_ref(root, schema["$ref"]), root, path, errors)
        return
    if "type" in schema and not matches_type(instance, schema["type"]):
        errors.append(f"{path}: expected type {schema['type']}")
        return
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} is not in the allowed enum")
    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            errors.append(f"{path}: string is shorter than minLength")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append(f"{path}: string does not match {schema['pattern']!r}")
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}: missing required property {key!r}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in properties:
                    errors.append(f"{path}: unexpected property {key!r}")
        for key, subschema in properties.items():
            if key in instance:
                validate_node(instance[key], subschema, root, f"{path}.{key}", errors)
    if isinstance(instance, list):
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in instance]
            if len(serialized) != len(set(serialized)):
                errors.append(f"{path}: array items must be unique")
        if "items" in schema:
            for index, item in enumerate(instance):
                validate_node(item, schema["items"], root, f"{path}[{index}]", errors)
    for subschema in schema.get("allOf", []):
        validate_node(instance, subschema, root, path, errors)
    if "if" in schema:
        condition_errors = []
        validate_node(instance, schema["if"], root, path, condition_errors)
        branch = "then" if not condition_errors else "else"
        if branch in schema:
            validate_node(instance, schema[branch], root, path, errors)


def schema_errors(document, schema):
    if Draft2020Validator is not None:
        Draft2020Validator.check_schema(schema)
        validator = Draft2020Validator(schema)
        return [
            f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}"
            for error in sorted(validator.iter_errors(document), key=lambda item: list(item.absolute_path))
        ]

    unsupported = unsupported_keyword_errors(schema)
    if unsupported:
        return sorted(unsupported)
    errors = []
    try:
        validate_node(document, schema, schema, "$", errors)
    except (ValueError, KeyError) as exc:
        errors.append(f"$: unsupported or invalid schema reference: {exc}")
    return sorted(errors)


def current_approvals(document, kind):
    return [
        item
        for item in document.get("authorizations", [])
        if item.get("kind") == kind
        and item.get("status") == "approved"
        and item.get("plan_revision") == document.get("plan_revision")
    ]


def validate_manifest_semantics(document):
    errors = []
    execution = document.get("execution", {})
    status = execution.get("status")
    authorization_level = document.get("authorization_level")
    plan_revision = document.get("plan_revision")

    for index, approval in enumerate(document.get("authorizations", [])):
        location = f"authorizations[{index}]"
        if approval.get("status") == "approved":
            if not approval.get("approver") or not approval.get("source_ref"):
                errors.append(f"{location}: approved authorization needs approver and source_ref")
            if not approval.get("original_statement"):
                errors.append(f"{location}: approved authorization needs the original approval statement")
            if approval.get("plan_revision") != plan_revision:
                errors.append(f"{location}.status: approval for an old plan_revision must be expired")

    if status == "Blocked":
        if not execution.get("blocked_reason"):
            errors.append("execution.blocked_reason: required when status is Blocked")
        if not execution.get("waiting_for"):
            errors.append("execution.waiting_for: required when status is Blocked")

    waiting_for = execution.get("waiting_for")
    authorization_kind = execution.get("authorization_kind")
    if waiting_for == "consultation":
        if not any(item.get("status") == "pending" for item in document.get("consultations", [])):
            errors.append("consultations: a pending consultation is required while waiting for consultation")
    elif waiting_for == "authorization":
        if not authorization_kind:
            errors.append("execution.authorization_kind: required while waiting for authorization")
        elif not any(
            item.get("kind") == authorization_kind and item.get("status") == "pending"
            for item in document.get("authorizations", [])
        ):
            errors.append(f"authorizations: a pending {authorization_kind} authorization is required while waiting")
    elif authorization_kind:
        errors.append("execution.authorization_kind: allowed only when waiting_for is authorization")

    for index, consultation in enumerate(document.get("consultations", [])):
        if consultation.get("status") == "answered" and not consultation.get("answer_ref"):
            errors.append(f"consultations[{index}].answer_ref: required when answered")

    structural_feedback = any(
        item.get("impact") in STRUCTURAL_FEEDBACK for item in document.get("design_feedback", [])
    )
    proposal = document.get("design_proposal")
    needs_proposal = authorization_level == "architecture" or structural_feedback
    if status in AUTHORIZED_STATES and needs_proposal:
        if not proposal:
            errors.append("design_proposal: required for architecture-level work or structural design feedback")
        elif len(proposal.get("alternatives", [])) < 2:
            errors.append("design_proposal.alternatives: at least two material alternatives are required")

    if proposal:
        if proposal.get("revision") != plan_revision:
            errors.append("design_proposal.revision: must match current plan_revision")
        alternative_ids = {item.get("id") for item in proposal.get("alternatives", [])}
        recommended = proposal.get("recommendation", {}).get("alternative_id")
        if recommended not in alternative_ids:
            errors.append("design_proposal.recommendation.alternative_id: must reference an alternative")

    if status in AUTHORIZED_STATES and (authorization_level == "architecture" or structural_feedback):
        design_acceptance = current_approvals(document, "design_acceptance")
        if not design_acceptance:
            errors.append("authorizations: current human design_acceptance is required for structural feedback or architecture")
        elif any(item.get("approver_type") != "human" for item in design_acceptance):
            errors.append("authorizations: structural feedback or architecture design_acceptance requires a human approver")

    if authorization_level in {"independent_refactor", "architecture"} and status in AUTHORIZED_STATES:
        implementation = current_approvals(document, "implementation")
        if not implementation:
            errors.append("authorizations: current implementation approval is required")
        else:
            approved_scope = set().union(*(set(item.get("scope", [])) for item in implementation))
            missing_scope = set(document.get("scope", {}).get("authorized", [])) - approved_scope
            if missing_scope:
                errors.append(f"authorizations: implementation scope does not cover {sorted(missing_scope)}")

    if authorization_level == "architecture" and status in AUTHORIZED_STATES:
        implementation = current_approvals(document, "implementation")
        if any(item.get("approver_type") != "human" for item in implementation):
            errors.append("authorizations: architecture implementation requires a human approver")

    if status in AUTHORIZED_STATES:
        for operation in document.get("risk_operations", []):
            kind = RISK_AUTHORIZATION[operation]
            approvals = current_approvals(document, kind)
            if not approvals:
                errors.append(f"authorizations: {operation} requires current {kind} approval")
            elif any(item.get("approver_type") != "human" for item in approvals):
                errors.append(f"authorizations: {operation} requires a human approver")

    validation = document.get("validation", {})
    evidence = validation.get("evidence", [])
    target_revision = validation.get("target_revision")
    for index, item in enumerate(evidence):
        if item.get("status") == "passed_with_limitations" and not item.get("limitations"):
            errors.append(f"validation.evidence[{index}].limitations: must explain passed_with_limitations")

    if status == "Completed":
        if not target_revision:
            errors.append("validation.target_revision: required when status is Completed")
        for required_check in validation.get("required", []):
            matching = [item for item in evidence if item.get("name") == required_check]
            if not matching:
                errors.append(f"validation.evidence: missing required check {required_check!r}")
                continue
            successful = [
                item
                for item in matching
                if item.get("status") in PASS_STATES and item.get("revision") == target_revision
            ]
            if not successful:
                errors.append(
                    f"validation.evidence: required check {required_check!r} lacks a passing result at target_revision"
                )

    return errors


def validate_knowledge_semantics(document):
    errors = []
    seen_ids = set()
    for index, record in enumerate(document.get("records", [])):
        record_id = record.get("id", f"records[{index}]")
        location = f"records[{index}]"
        if record_id in seen_ids:
            errors.append(f"{location}.id: duplicate record ID {record_id!r}")
        seen_ids.add(record_id)
        kind = record.get("kind")
        expected_prefix = PREFIX_BY_KIND.get(kind)
        if expected_prefix and not str(record_id).startswith(expected_prefix):
            errors.append(f"{location}.id: {kind} must use prefix {expected_prefix!r}")
        if record.get("truth_status") == "invalidated" and record.get("retrieval_tier") == "active":
            errors.append(f"{location}.retrieval_tier: invalidated knowledge cannot remain active")
        if record.get("decision_status") in {"superseded", "rejected"} and record.get("retrieval_tier") == "active":
            errors.append(f"{location}.retrieval_tier: inactive decisions cannot remain active")
        if record.get("lifecycle_status") in INACTIVE_LIFECYCLES and record.get("retrieval_tier") == "active":
            errors.append(f"{location}.retrieval_tier: inactive lifecycle records cannot remain active")
        if (
            kind == "constraint"
            and record.get("source", {}).get("type") == "agent_inference"
            and record.get("truth_status") != "confirmed"
        ):
            errors.append(f"{location}.truth_status: an inferred constraint must be confirmed before use as a constraint")
        if kind == "quality_preference":
            if record.get("truth_status") != "not_applicable":
                errors.append(f"{location}.truth_status: quality preferences use not_applicable")
            if record.get("source", {}).get("type") != "user_request":
                errors.append(f"{location}.source.type: quality preferences require a human source")
            if record.get("retrieval_tier") == "active" and record.get("preference_status") != "confirmed":
                errors.append(f"{location}.preference_status: only confirmed preferences can be active")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=sorted(SCHEMAS))
    parser.add_argument("document", help="YAML document to validate")
    args = parser.parse_args()
    try:
        schema = load_yaml(SCHEMAS[args.kind])
        document = load_yaml(args.document)
    except (OSError, yaml.YAMLError) as exc:
        print(f"Unable to load input: {exc}", file=sys.stderr)
        return 2
    if not isinstance(document, dict):
        print("Document root must be a mapping.", file=sys.stderr)
        return 1
    errors = schema_errors(document, schema)
    if not errors:
        errors = validate_manifest_semantics(document) if args.kind == "manifest" else validate_knowledge_semantics(document)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    mode = "jsonschema" if Draft2020Validator is not None else "guarded-subset"
    print(f"OK {args.document}: valid {args.kind} v0.1 ({mode})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
