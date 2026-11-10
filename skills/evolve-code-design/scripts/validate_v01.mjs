#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import YAML from "yaml";

let Ajv2020 = null;
if (!process.env.VALIDATE_DISABLE_AJV) {
  try {
    ({ default: Ajv2020 } = await import("ajv/dist/2020.js"));
  } catch {
    Ajv2020 = null;
  }
}

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SCHEMAS = {
  manifest: path.join(ROOT, "assets", "change-manifest.schema.yaml"),
  knowledge: path.join(ROOT, "assets", "knowledge-record.schema.yaml"),
};
const PASS_STATES = new Set(["passed", "passed_with_limitations"]);
const AUTHORIZED_STATES = new Set(["Authorized", "Implementing", "Validating", "Completed"]);
const STRUCTURAL_FEEDBACK = new Set([
  "responsibility_boundary",
  "abstraction_boundary",
  "concept_boundary",
  "architecture",
]);
const PREFIX_BY_KIND = {
  constraint: "C-",
  assumption: "A-",
  decision_reference: "D-",
  design_fact: "K-",
  quality_preference: "Q-",
};
const INACTIVE_LIFECYCLES = new Set(["resolved", "invalidated", "expired", "superseded"]);
const RISK_AUTHORIZATION = {
  database_migration: "migration",
  compatibility_change: "compatibility_change",
  production_operation: "production_operation",
  security_change: "security_change",
};
const SUPPORTED_SCHEMA_KEYWORDS = new Set([
  "$schema", "$id", "$defs", "$ref", "title", "description", "type", "required",
  "properties", "additionalProperties", "items", "uniqueItems", "enum", "const",
  "pattern", "minLength", "allOf", "if", "then", "else",
]);

function loadYaml(filePath) {
  return YAML.parse(fs.readFileSync(filePath, "utf8"));
}

function stableStringify(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(",")}]`;
  const keys = Object.keys(value).sort();
  return `{${keys.map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`).join(",")}}`;
}

function unsupportedKeywordErrors(schema) {
  const errors = [];
  function visit(node, location) {
    if (!node || typeof node !== "object" || Array.isArray(node)) return;
    for (const keyword of Object.keys(node)) {
      if (!SUPPORTED_SCHEMA_KEYWORDS.has(keyword)) {
        errors.push(`${location}: unsupported schema keyword '${keyword}' in fallback validator`);
      }
    }
    for (const container of ["$defs", "properties"]) {
      for (const [name, subschema] of Object.entries(node[container] ?? {})) {
        visit(subschema, `${location}.${container}.${name}`);
      }
    }
    for (const keyword of ["items", "additionalProperties", "if", "then", "else"]) {
      const subschema = node[keyword];
      if (subschema && typeof subschema === "object" && !Array.isArray(subschema)) {
        visit(subschema, `${location}.${keyword}`);
      } else if (keyword === "items" && Array.isArray(subschema)) {
        errors.push(`${location}.items: array-form items is unsupported in fallback validator`);
      }
    }
    for (const [index, subschema] of (node.allOf ?? []).entries()) {
      visit(subschema, `${location}.allOf[${index}]`);
    }
  }
  visit(schema, "$");
  return errors;
}

function resolveRef(root, reference) {
  if (!reference.startsWith("#/")) throw new Error(`Only local schema references are supported: ${reference}`);
  let node = root;
  for (const rawPart of reference.slice(2).split("/")) {
    const part = rawPart.replaceAll("~1", "/").replaceAll("~0", "~");
    node = node[part];
  }
  return node;
}

function matchesType(instance, expected) {
  const checks = {
    object: (value) => value !== null && typeof value === "object" && !Array.isArray(value),
    array: Array.isArray,
    string: (value) => typeof value === "string",
    null: (value) => value === null,
    boolean: (value) => typeof value === "boolean",
    number: (value) => typeof value === "number" && Number.isFinite(value),
    integer: (value) => Number.isInteger(value),
  };
  const expectedTypes = typeof expected === "string" ? [expected] : expected;
  return expectedTypes.some((type) => checks[type](instance));
}

function validateNode(instance, schema, root, location, errors) {
  if (schema.$ref) {
    validateNode(instance, resolveRef(root, schema.$ref), root, location, errors);
    return;
  }
  if (schema.type && !matchesType(instance, schema.type)) {
    errors.push(`${location}: expected type ${JSON.stringify(schema.type)}`);
    return;
  }
  if ("const" in schema && stableStringify(instance) !== stableStringify(schema.const)) {
    errors.push(`${location}: expected constant ${JSON.stringify(schema.const)}`);
  }
  if (schema.enum && !schema.enum.some((value) => stableStringify(value) === stableStringify(instance))) {
    errors.push(`${location}: value is not in the allowed enum`);
  }
  if (typeof instance === "string") {
    if (instance.length < (schema.minLength ?? 0)) errors.push(`${location}: string is shorter than minLength`);
    if (schema.pattern && !new RegExp(schema.pattern).test(instance)) {
      errors.push(`${location}: string does not match ${JSON.stringify(schema.pattern)}`);
    }
  }
  if (instance !== null && typeof instance === "object" && !Array.isArray(instance)) {
    for (const key of schema.required ?? []) {
      if (!(key in instance)) errors.push(`${location}: missing required property '${key}'`);
    }
    const properties = schema.properties ?? {};
    if (schema.additionalProperties === false) {
      for (const key of Object.keys(instance)) {
        if (!(key in properties)) errors.push(`${location}: unexpected property '${key}'`);
      }
    }
    for (const [key, subschema] of Object.entries(properties)) {
      if (key in instance) validateNode(instance[key], subschema, root, `${location}.${key}`, errors);
    }
  }
  if (Array.isArray(instance)) {
    if (schema.uniqueItems) {
      const serialized = instance.map(stableStringify);
      if (new Set(serialized).size !== serialized.length) errors.push(`${location}: array items must be unique`);
    }
    if (schema.items) {
      instance.forEach((item, index) => validateNode(item, schema.items, root, `${location}[${index}]`, errors));
    }
  }
  for (const subschema of schema.allOf ?? []) validateNode(instance, subschema, root, location, errors);
  if (schema.if) {
    const conditionErrors = [];
    validateNode(instance, schema.if, root, location, conditionErrors);
    const branch = conditionErrors.length === 0 ? "then" : "else";
    if (schema[branch]) validateNode(instance, schema[branch], root, location, errors);
  }
}

function schemaErrors(document, schema) {
  if (Ajv2020) {
    const ajv = new Ajv2020({ allErrors: true, strict: false });
    const validate = ajv.compile(schema);
    if (validate(document)) return [];
    return (validate.errors ?? []).map((error) => `${error.instancePath || "$"}: ${error.message}`);
  }
  const unsupported = unsupportedKeywordErrors(schema);
  if (unsupported.length) return unsupported.sort();
  const errors = [];
  try {
    validateNode(document, schema, schema, "$", errors);
  } catch (error) {
    errors.push(`$: unsupported or invalid schema reference: ${error.message}`);
  }
  return errors.sort();
}

function currentApprovals(document, kind) {
  return (document.authorizations ?? []).filter(
    (item) => item.kind === kind && item.status === "approved" && item.plan_revision === document.plan_revision,
  );
}

function validateManifestSemantics(document) {
  const errors = [];
  const execution = document.execution ?? {};
  const status = execution.status;
  const authorizationLevel = document.authorization_level;
  const requiredHuman = new Set(document.required_human_authorizations ?? []);

  for (const [index, approval] of (document.authorizations ?? []).entries()) {
    const location = `authorizations[${index}]`;
    if (approval.status === "approved") {
      if (!approval.approver || !approval.source_ref) errors.push(`${location}: approved authorization needs approver and source_ref`);
      if (!approval.original_statement) errors.push(`${location}: approved authorization needs the original approval statement`);
      if (approval.plan_revision !== document.plan_revision) {
        errors.push(`${location}.status: approval for an old plan_revision must be expired`);
      }
    }
  }

  if (status === "Blocked") {
    if (!execution.blocked_reason) errors.push("execution.blocked_reason: required when status is Blocked");
    if (!execution.waiting_for) errors.push("execution.waiting_for: required when status is Blocked");
  }

  const waitingFor = execution.waiting_for;
  const authorizationKind = execution.authorization_kind;
  if (waitingFor === "consultation") {
    if (!(document.consultations ?? []).some((item) => item.status === "pending")) {
      errors.push("consultations: a pending consultation is required while waiting for consultation");
    }
  } else if (waitingFor === "authorization") {
    if (!authorizationKind) {
      errors.push("execution.authorization_kind: required while waiting for authorization");
    } else if (!(document.authorizations ?? []).some((item) => item.kind === authorizationKind && item.status === "pending")) {
      errors.push(`authorizations: a pending ${authorizationKind} authorization is required while waiting`);
    }
  } else if (authorizationKind) {
    errors.push("execution.authorization_kind: allowed only when waiting_for is authorization");
  }

  for (const [index, consultation] of (document.consultations ?? []).entries()) {
    if (consultation.status === "answered" && !consultation.answer_ref) {
      errors.push(`consultations[${index}].answer_ref: required when answered`);
    }
  }

  const structuralFeedback = (document.design_feedback ?? []).some((item) => STRUCTURAL_FEEDBACK.has(item.impact));
  const proposal = document.design_proposal;
  const needsProposal = authorizationLevel === "architecture" || structuralFeedback;
  if (AUTHORIZED_STATES.has(status) && needsProposal) {
    if (!proposal) {
      errors.push("design_proposal: required for architecture-level work or structural design feedback");
    } else if ((proposal.alternatives ?? []).length < 2) {
      errors.push("design_proposal.alternatives: at least two material alternatives are required");
    }
  }

  if (proposal) {
    if (proposal.revision !== document.plan_revision) errors.push("design_proposal.revision: must match current plan_revision");
    const alternativeIds = new Set((proposal.alternatives ?? []).map((item) => item.id));
    if (!alternativeIds.has(proposal.recommendation?.alternative_id)) {
      errors.push("design_proposal.recommendation.alternative_id: must reference an alternative");
    }
  }

  if (authorizationLevel === "architecture" && AUTHORIZED_STATES.has(status)) {
    if (!currentApprovals(document, "design_acceptance").length) {
      errors.push("authorizations: current design_acceptance is required for architecture-level work");
    }
  }

  if (["independent_refactor", "architecture"].includes(authorizationLevel) && AUTHORIZED_STATES.has(status)) {
    const implementation = currentApprovals(document, "implementation");
    if (!implementation.length) {
      errors.push("authorizations: current implementation approval is required");
    } else {
      const approvedScope = new Set(implementation.flatMap((item) => item.scope ?? []));
      const missingScope = (document.scope?.authorized ?? []).filter((item) => !approvedScope.has(item));
      if (missingScope.length) errors.push(`authorizations: implementation scope does not cover ${JSON.stringify(missingScope)}`);
    }
  }

  if (AUTHORIZED_STATES.has(status)) {
    for (const operation of document.risk_operations ?? []) {
      const kind = RISK_AUTHORIZATION[operation];
      if (!currentApprovals(document, kind).length) {
        errors.push(`authorizations: ${operation} requires current ${kind} approval`);
      }
    }
    for (const kind of requiredHuman) {
      const approvals = currentApprovals(document, kind);
      if (!approvals.length) {
        errors.push(`authorizations: reserved decision ${kind} requires current human approval`);
      } else if (approvals.some((item) => item.approver_type !== "human")) {
        errors.push(`authorizations: reserved decision ${kind} requires a human approver`);
      }
    }
  }

  const validation = document.validation ?? {};
  const evidence = validation.evidence ?? [];
  const targetRevision = validation.target_revision;
  for (const [index, item] of evidence.entries()) {
    if (item.status === "passed_with_limitations" && !(item.limitations ?? []).length) {
      errors.push(`validation.evidence[${index}].limitations: must explain passed_with_limitations`);
    }
  }

  if (status === "Completed") {
    if (!targetRevision) errors.push("validation.target_revision: required when status is Completed");
    for (const requiredCheck of validation.required ?? []) {
      const matching = evidence.filter((item) => item.name === requiredCheck);
      if (!matching.length) {
        errors.push(`validation.evidence: missing required check '${requiredCheck}'`);
        continue;
      }
      const successful = matching.some(
        (item) => PASS_STATES.has(item.status) && item.revision === targetRevision,
      );
      if (!successful) {
        errors.push(`validation.evidence: required check '${requiredCheck}' lacks a passing result at target_revision`);
      }
    }
  }

  return errors;
}

function validateKnowledgeSemantics(document) {
  const errors = [];
  const seenIds = new Set();
  for (const [index, record] of (document.records ?? []).entries()) {
    const recordId = record.id ?? `records[${index}]`;
    const location = `records[${index}]`;
    if (seenIds.has(recordId)) errors.push(`${location}.id: duplicate record ID '${recordId}'`);
    seenIds.add(recordId);

    const expectedPrefix = PREFIX_BY_KIND[record.kind];
    if (expectedPrefix && !recordId.startsWith(expectedPrefix)) {
      errors.push(`${location}.id: ${record.kind} must use prefix '${expectedPrefix}'`);
    }
    if (record.truth_status === "invalidated" && record.retrieval_tier === "active") {
      errors.push(`${location}.retrieval_tier: invalidated knowledge cannot remain active`);
    }
    if (["superseded", "rejected"].includes(record.decision_status) && record.retrieval_tier === "active") {
      errors.push(`${location}.retrieval_tier: inactive decisions cannot remain active`);
    }
    if (INACTIVE_LIFECYCLES.has(record.lifecycle_status) && record.retrieval_tier === "active") {
      errors.push(`${location}.retrieval_tier: inactive lifecycle records cannot remain active`);
    }
    if (record.kind === "constraint" && record.source?.type === "agent_inference" && record.truth_status !== "confirmed") {
      errors.push(`${location}.truth_status: an inferred constraint must be confirmed before use as a constraint`);
    }
    if (record.kind === "quality_preference") {
      if (record.truth_status !== "not_applicable") errors.push(`${location}.truth_status: quality preferences use not_applicable`);
      if (record.source?.type !== "user_request") errors.push(`${location}.source.type: quality preferences require a human source`);
      if (record.retrieval_tier === "active" && record.preference_status !== "confirmed") {
        errors.push(`${location}.preference_status: only confirmed preferences can be active`);
      }
    }
  }
  return errors;
}

function main() {
  const [kind, documentPath] = process.argv.slice(2);
  if (!SCHEMAS[kind] || !documentPath) {
    console.error("Usage: node scripts/validate_v01.mjs <manifest|knowledge> <document.yaml>");
    return 2;
  }

  let schema;
  let document;
  try {
    schema = loadYaml(SCHEMAS[kind]);
    document = loadYaml(documentPath);
  } catch (error) {
    console.error(`Unable to load input: ${error.message}`);
    return 2;
  }
  if (!document || typeof document !== "object" || Array.isArray(document)) {
    console.error("Document root must be a mapping.");
    return 1;
  }

  let errors = schemaErrors(document, schema);
  if (!errors.length) {
    errors = kind === "manifest" ? validateManifestSemantics(document) : validateKnowledgeSemantics(document);
  }
  if (errors.length) {
    for (const error of errors) console.error(`ERROR ${error}`);
    return 1;
  }
  const mode = Ajv2020 ? "ajv" : "guarded-subset";
  console.log(`OK ${documentPath}: valid ${kind} v0.1 (${mode})`);
  return 0;
}

export { schemaErrors, validateManifestSemantics, validateKnowledgeSemantics };

const isMainModule = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMainModule) process.exitCode = main();
