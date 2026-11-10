---
name: evolve-code-design
description: Start only on an explicit user instruction or explicit external workflow command to evolve new or existing software designs through single-agent work or temporary multi-agent design groups. After the user selects a task and scope, execute autonomously with requirement provenance, bounded global reflection, behavior verification, and minimal documentation. Use for explicit requests for design optimization, refactoring, architecture review, re-evaluation of agent decisions, or design feedback. Do not start solely because repository context suggests an optimization opportunity.
---

# Evolve Code Design

Start only on an explicit user instruction or explicit external workflow command. The user decides whether a task starts; after task and scope are selected, agents decide how to complete it. Human participation can enter at any stage but is not the default control loop.

## 1. Start, recommend, and select

Do not start design optimization, group formation, or an iteration cycle merely because code context suggests an opportunity.

### Concrete instruction

When the user explicitly requests a design review, optimization, proposal, or implementation, proceed within the stated scope without redundant task-selection questions. Analysis-only requests do not authorize modification.

### Invocation without a concrete task

When the user explicitly invokes this workflow without a concrete task:

1. Inspect only the minimum context needed to make relevant recommendations.
2. Offer a small set of evidence-relevant actions, such as a quick single-agent review, multi-agent design optimization, bounded iterative optimization, analysis-only, or implementation of an existing proposal.
3. Include a recommendation and the reason, then wait for the user's selection. Use a structured question mechanism when available.
4. Do not form the group, modify code, or begin iterative optimization before the user selects.

Use repository context to recommend tasks, never to decide that a task should start.

### After selection

Use one agent for clear, low-risk work, local naming, simple expression changes, and small edits with explicit boundaries. After the user selects a task, form a temporary design group when multiple plausible concept or responsibility models would materially affect business semantics, dependencies, evolution cost, or behavior constraints; also use one for architecture, repeated design dissatisfaction, or a newly discovered capability gap.

For every multi-agent design task, read and follow the complete collaboration protocol in `assets/AGENTS.md`; this `SKILL.md` provides the invocation and delivery workflow, not a reduced substitute for that protocol.

A minimal group has:

- A concept designer for domain meaning and responsibility boundaries.
- A skeptical reviewer for concrete defects, counterexamples, assumptions, and dependencies.
- An evolution reviewer for behavior protection, migration cost, and the smallest viable path.

Each perspective first inspects original input and primary evidence without reading the coordinator's conclusions. Do not merely rename one conclusion three times. Do not build a fixed multi-agent scheduler.

## 2. Preserve input provenance

Preserve original requests or immutable references. Classify human input as goal, constraint, authorization, or quality preference, and distinguish exploration, suggestions, explicit requests, and formal approval.

Keep the agent interpretation separate and mark its confirmation status. Never promote an agent inference, group recommendation, or group decision into a user instruction or requirement.

Create a Change Manifest from `assets/change-manifest.example.yaml` only after the user selects non-trivial work whose group decisions, participation, authorization, execution state, or evidence should persist.

## 3. Run the selected autonomous design loop

After the user selects the task and scope:

1. Inspect code, tests, configuration, constraints, and affected concepts.
2. Have each perspective independently diagnose problems and form alternatives before comparing conclusions.
3. Cross-examine assumptions and proposals using concrete defects, counterexamples, and applicability limits rather than generic risks.
4. Synthesize a Design Proposal with current behavior, alternatives, structure views when useful, trade-offs, recommendation, evaluation points, and required scope.
5. Record adopted reasons, rejected alternatives, responses to material objections, unresolved disagreements, and credible minority positions.
6. Decide by evidence rather than majority vote. Agreement does not prove correctness, and minority objections require explicit responses.
7. If evidence cannot distinguish alternatives, preserve candidates or the current design instead of forcing consensus. `keep` is a valid group outcome.
8. Reopen the group only for new evidence, a newly discovered capability gap, or a demonstrated defect in its own proposal.
9. Stop when no new evidence or material alternatives remain or the authorized design is verified.

A Design Proposal coordinates agents and may also help humans evaluate direction. It is not inherently a human approval request. The goal is better judgment, not a higher agreement rate.

Every optimization claim must state what specifically improved and use evidence matched to its goal: concept accuracy, rule ownership, and lifecycles for conceptual models; cohesion and change reasons for responsibilities; dependency direction, coupling, and change impact for module boundaries; shared language and reduced ambiguity for naming; behavior baselines, tests, and compatibility for behavior changes; and before/after measurements for performance, resources, or cost. Do not use “more elegant” as sufficient evidence or impose numeric metrics on every conceptual improvement.

Do not start a new optimization or iteration cycle automatically after completing the selected task. Present further work as another user-selectable recommendation.

## 4. Allow dynamic human participation

When a human provides design feedback without a concrete task, treat it as permission to investigate only. Preserve the raw feedback, mark agent interpretations as unconfirmed, and then offer relevant next actions instead of assuming an optimization task.

After the user selects work, use existing authority for low-risk `local_expression`. For `responsibility_boundary`, `abstraction_boundary`, `concept_boundary`, or `architecture`, automatically invoke group review and a Design Proposal. Do not automatically require human design acceptance.

If a human likes a direction but dislikes its responsibility split, return to group investigation and revise it. Human design acceptance is required only when listed in `required_human_authorizations`.

Ask for human semantics or value judgments only when evidence cannot resolve a material decision. State what was investigated, options, the group recommendation, and what can proceed without an answer. No response is not approval, but it does not block work that has no required human wait.

## 5. Authorize actions independently of task type

Record `change_class` separately from `authorization_level`. The class describes task nature; the level describes impact and action authority. Features and bug fixes may require any level.

- `local`: work within existing agent authority.
- `independent_refactor`: requires current implementation authorization from an authorized agent, human, or system.
- `architecture`: requires current design and implementation authorizations from authorized agents, humans, or systems.

Approval is not inherently human. Use `required_human_authorizations` only for explicitly reserved decisions; those kinds require a human approver. Other approvals may come from an authorized agent or system. An autonomous workflow may contain reserved human authorizations; only dependent work waits.

Keep design acceptance, implementation, migration, compatibility change, security change, and production operation separate. Bind each to plan revision, scope, conditions, approver, and source. Design acceptance alone does not authorize implementation or operations.

Pause only work dependent on missing authority or input. When independent work is not dependent on the blocked operation, split it into a separate Change and complete it independently instead of adding operation-level scheduling to one Manifest. Use `Blocked` for human and non-human waits, with `waiting_for=authorization` plus `authorization_kind` for approval waits.

## 6. Implement and verify

Identify concepts, rules, invariants, lifecycles, and reasons for change before changing class or module boundaries. Prefer the smallest understandable design that solves the actual problem.

Establish behavior protection before structural changes. Run relevant checks during implementation. Bind final evidence to the resulting revision and preserve limitations. Never report `not_run` or `inconclusive` as success.

Stay within authorized scope and keep functional and structural changes separate when combining them would obscure review or rollback.

## 7. Reflect and update knowledge by exception

Inspect affected concepts, callers, dependencies, and invariants after meaningful changes within the selected task. Choose `keep`, `observe`, or `propose`. Invoke a broader group only on concrete evidence. Do not reopen rejected designs without new evidence or start another user-unselected optimization cycle.

Default to no documentation update. Update only when current concepts, boundaries, constraints, significant decisions, active assumptions, or confirmed cross-task quality preferences changed.

Keep one fact in one canonical location. Use `active`, `reference`, and `retired` as retrieval states independently of truth and decision status. Keep raw feedback in task records and promote quality preferences only after human confirmation of cross-task scope. Create an ADR only for a significant decision with durable trade-offs.

## 8. Use bundled resources

- Merge `assets/AGENTS.md` into a project only when asked to adopt the workflow; never overwrite an existing file.
- Use `assets/current-model.md` for the concise current-design view.
- Start manifests and knowledge records from the two `.example.yaml` files, replacing all example content with project facts.
- Validate against the two Schema files after creating or modifying machine records.

```bash
python scripts/validate_v01.py manifest <path-to-manifest.yaml>
python scripts/validate_v01.py knowledge <path-to-records.yaml>
```

The validator uses `jsonschema` when available. Without it, the fallback supports only bundled-schema keywords and rejects unsupported keywords instead of ignoring them. Do not represent it as a general-purpose JSON Schema validator.

Read `assets/AGENTS.md` when installing the workflow, resolving governance ambiguity, or performing any multi-agent design task. Read schemas only when creating or validating records.

## 9. Deliver a concise result

Report behavior and design decisions, group conclusions and unresolved disagreements when relevant, validation evidence and limitations, human input and exact authorizations when used, global reflection, documentation changes or why none were needed, and remaining assumptions or proposed work.

Present any new optimization or iteration as a separate recommendation awaiting user selection. Do not narrate tool calls or produce a chronological implementation log.

## Non-goals for v0.1

Do not start from repository context alone, introduce a knowledge graph, atomize every paragraph, build a fixed multi-agent platform, create permanent records for every feedback comment, run exhaustive periodic reviews, make ordinary tasks wait for approval, or start unselected iterations. Automatically using a temporary design group after task selection is required when triggered; building a multi-agent scheduler is not.
