---
name: evolve-code-design
description: Govern design-sensitive software changes with requirement provenance, low-cost human design guidance, bounded global reflection, behavior verification, and minimal long-lived documentation. Use for non-trivial features, class or module design, refactoring, architecture reviews, ambiguous requirements, re-evaluation of previous agent decisions, vague feedback such as “this design feels awkward,” or requests to challenge the current design. Skip the full workflow for conversational explanations and trivial edits.
---

# Evolve Code Design

Apply a lightweight governance loop without creating a knowledge-management or approval bureaucracy.

## 1. Select workflow depth and participation

Skip the Change Manifest for trivial edits with no conceptual or contractual impact. When the user only asks for a design opinion or analysis, provide analysis without creating a change or modifying code.

Default to delegation for clear, low-risk work. Investigate available evidence before asking humans. Use consultation only for product semantics or important value trade-offs. Use approval for work beyond existing scope or high-impact design, data, compatibility, security, or production changes.

For every consultation, state what the human must decide, what was investigated, concrete options and the agent recommendation, and what happens without an answer. No response is not approval.

## 2. Preserve human input semantics

Preserve the original request or an immutable reference. Classify human input as goal, constraint, authorization, or quality preference, and distinguish exploration, suggestions, explicit requests, and formal approval.

Keep the agent interpretation separate and mark its confirmation status. Never turn an agent inference into a human requirement.

Create a Change Manifest from `assets/change-manifest.example.yaml` for non-trivial work whose participation, authorization, execution state, or evidence should persist.

## 3. Handle vague design feedback

When the human says “this feels awkward,” “too complex,” or “I do not like this model,” do not demand a technical diagnosis and do not immediately rewrite code.

1. Record the raw feedback and target in the Manifest.
2. Investigate concepts, responsibilities, dependencies, control flow, and cognitive cost.
3. Mark agent explanations as unconfirmed until validated.
4. Classify impact as `local_expression`, `responsibility_boundary`, `abstraction_boundary`, `concept_boundary`, or `architecture`.
5. Handle low-risk `local_expression` under existing delegated authority without mandatory design approval.
6. For structural or architectural feedback, compare current, minimal, and materially different designs; present a Design Proposal and obtain human design acceptance before execution.
7. If the human likes a direction but dislikes its responsibility split, return to investigation and revise the proposal instead of mechanically implementing it.
8. Stop when the human decides, no material alternatives remain, or further proposals repeat the same trade-offs.

For `Challenge Current Design`, question the current decomposition while preserving user constraints, behavior protection, and authorization requirements.

A Design Proposal contains current behavior, evidence-backed problems, alternatives, trade-offs, migration cost, agent recommendation, human decisions needed, and required scope. Add a compact structure tree or responsibility view when it lowers evaluation cost.

## 4. Authorize the actual operation

Record `change_class` separately from `authorization_level`. The class describes task nature; the level is determined by scope, impact, and risk. Features and bug fixes may require any level.

Use `local` for delegated low-impact edits, `independent_refactor` for separately approved structural work, and `architecture` for core concept or significant boundary changes. Keep authorized and proposed scope separate.

Record design acceptance, implementation, migration, compatibility change, security change, and production operation separately. Bind each approval to a plan revision, scope, conditions, approver, and original source.

Design acceptance does not authorize implementation. Implementation approval does not authorize migration, compatibility removal, security changes, or production operations.

For architecture-level changes, obtain human design acceptance and human implementation approval before implementation. Pause affected work if the plan or required scope materially changes.

Use `Blocked` for human and non-human waits. Use `waiting_for=authorization` plus `authorization_kind` for approvals; use `external_dependency`, `environment`, `technical_resolution`, or `other` for non-human blockers.

## 5. Implement and verify

Identify concepts, rules, invariants, lifecycles, and reasons for change before changing class or module boundaries. Prefer the smallest understandable design that solves the actual problem.

Establish behavior protection before structural changes. Run relevant checks during implementation. Bind final evidence to the resulting revision and preserve limitations. Never report `not_run` or `inconclusive` as success.

Keep functional and structural changes separate when combining them would obscure review or rollback.

## 6. Reflect globally with a budget

Inspect affected concepts, callers, dependencies, and invariants. Expand only on concrete evidence.

Choose one result:

- `keep`: no design action is justified.
- `observe`: retain a material issue or opportunity with a revisit trigger.
- `propose`: request separately scoped design work.

Do not reopen rejected designs without new evidence. Do not use an agent-generated assumption or old design choice as the sole reason to reject a better model. State separately whether an alternative is conceptually better and whether it should be implemented now.

## 7. Update knowledge by exception

Default to no documentation update.

Update long-term knowledge only when current concepts, boundaries, constraints, significant decisions, active assumptions, or confirmed cross-task quality preferences changed. Keep one fact in one canonical location and reference it elsewhere.

Keep raw feedback and unconfirmed interpretations in task records. Promote a quality preference only after the human confirms its cross-task applicability, scope, and source. Do not turn preferences into absolute rules.

Use `active`, `reference`, and `retired` as retrieval states independently of truth and decision status. Exclude retired records from default design context. Create an ADR only for a significant decision with durable trade-offs.

## 8. Use bundled resources

- Merge `assets/AGENTS.md` into a project only when asked to adopt the workflow; never overwrite an existing file.
- Use `assets/current-model.md` for the concise current-design view.
- Start manifests and knowledge records from the two `.example.yaml` files, replacing all example content with project facts.
- Validate against the two Schema files after creating or modifying machine records.

```bash
python scripts/validate_v01.py manifest <path-to-manifest.yaml>
python scripts/validate_v01.py knowledge <path-to-records.yaml>
```

The validator uses the installed `jsonschema` library when available. Without it, the fallback supports only the keywords used by the bundled schemas and rejects unsupported keywords instead of silently ignoring them. Do not represent the fallback as a general-purpose JSON Schema validator.

Read `assets/AGENTS.md` when installing the workflow or resolving governance ambiguity. Read schemas only when creating or validating records.

## 9. Deliver a concise result

Report behavior and design decisions, validation evidence and limitations, human decisions and exact authorizations, global reflection when applicable, documentation changes or why none were needed, and unresolved assumptions or proposed work.

Do not narrate tool calls or produce a chronological implementation log.

## Non-goals for v0.1

Do not introduce a knowledge graph, atomize every paragraph, build a multi-agent scheduler, create permanent records for every feedback comment, run exhaustive periodic reviews, or make ordinary tasks wait for approval. Add machinery only after observed failures justify it.
