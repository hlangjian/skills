# Agent Design Governance v0.1

## Purpose

Optimize for correct behavior, conceptual clarity, and ease of human understanding. Start only on an explicit user instruction or explicit external workflow command. After the user selects a task and scope, an autonomous agent or temporary agent design group becomes the decision and execution subject. Human participation is dynamic input, not the default control loop.

Trivial edits require no Change Manifest, design group, or global review. Repository context may inform recommendations but must never start a task by itself.

## 1. Start, recommend, and select execution

Do not start design optimization, group formation, or an iteration cycle merely because code context suggests an opportunity.

When the user gives a concrete design review, optimization, proposal, or implementation instruction, proceed within the stated scope without redundant task-selection questions. Analysis-only requests do not authorize modification.

When the user explicitly invokes this workflow without a concrete task:

1. Inspect only the minimum context needed for relevant recommendations.
2. Offer a small set of evidence-relevant actions, such as quick single-agent review, multi-agent design optimization, bounded iterative optimization, analysis-only, or implementation of an existing proposal.
3. Include a recommendation and reason, then wait for the user's selection. Use a structured question mechanism when available.
4. Do not form a group, create a Change Manifest, modify code, or begin iteration before selection.

After selection, use one agent for clear, low-risk work, local naming, simple expression changes, and small edits with explicit boundaries. Form a temporary design group when multiple plausible concept or responsibility models would materially affect business semantics, dependencies, evolution cost, or behavior constraints; also use one for architecture, repeated design dissatisfaction, or a newly discovered capability gap. Do not wait for a human to assemble the group and do not build a fixed multi-agent platform.

A minimal group contains independent perspectives:

- Concept designer: identify domain concepts, rules, lifecycles, and responsibility boundaries.
- Skeptical reviewer: challenge inherited assumptions, abstractions, dependencies, and premature consensus with concrete defects or counterexamples.
- Evolution reviewer: evaluate behavior protection, migration cost, compatibility, and the smallest viable path.

Each perspective first inspects original requests and primary evidence without reading the coordinator's conclusions. Do not simulate independence by giving three labels to one untested conclusion. Dissolve the group after completion or when its stop conditions are met.

## 2. Preserve intent and provenance

- Preserve original human requests or immutable references when present.
- Keep agent interpretations separate from original input.
- Classify human input as `goal`, `constraint`, `authorization`, or `quality_preference`; none substitutes for another.
- Distinguish exploration, suggestions, explicit requests, and formal approval.
- Never promote an agent inference, group recommendation, or group decision into a user instruction or requirement.
- Distinguish truth status, decision ownership, retrieval tier, and current change cost.
- Treat code as authority for current implementation, not proof that its design is necessary.

When information is incomplete, first inspect code, tests, configuration, and authoritative documents. Proceed with low-risk reversible choices. Seek human input only when semantics, values, or reserved permissions cannot be resolved from evidence and materially affect the result.

## 3. Run the selected autonomous design loop

After the user selects the task and scope:

1. Collect primary evidence and affected concepts.
2. Have each perspective independently produce a diagnosis and materially different alternatives before comparing conclusions.
3. Cross-examine assumptions, responsibilities, dependencies, and migration costs. Require specific defects, counterexamples, or applicability limits rather than generic risk statements.
4. Synthesize a Design Proposal with current behavior, alternatives, structure views when useful, trade-offs, recommendation, evaluation points, and required scope.
5. Record how the decision was reached: adopted reasons, rejected alternatives, responses to material objections, unresolved disagreements, and minority positions that remain credible.
6. Decide by evidence rather than majority vote. Agreement does not prove correctness, and a minority objection must not be discarded without an explicit response.
7. If evidence cannot distinguish alternatives, preserve the candidates or the current design instead of forcing consensus. Choosing `keep` is a valid group outcome.
8. Reopen the group only for new evidence, a newly discovered capability gap, or a demonstrated defect in its own proposal.
9. Stop when no new evidence or material alternatives remain, further proposals repeat trade-offs, or the authorized design is verified.

A Design Proposal is a coordination artifact for agents and, when present, humans. It is not inherently a request for human approval. Its purpose is better design judgment, not a higher agreement rate.

Every optimization claim must state what specifically improved and use evidence matched to its goal: concept accuracy, rule ownership, and lifecycles for conceptual models; cohesion and change reasons for responsibilities; dependency direction, coupling, and change impact for module boundaries; shared language and reduced ambiguity for naming; behavior baselines, tests, and compatibility for behavior changes; and before/after measurements for performance, resources, or cost. Do not use “more elegant” as sufficient evidence or impose numeric metrics on every conceptual improvement.

Do not start another optimization or iteration automatically after completing the selected task. Present further work as another recommendation awaiting user selection.

## 4. Allow dynamic human participation

Human feedback without a concrete task authorizes investigation only. Treat “this design feels awkward” as an investigation signal, not a confirmed diagnosis or an automatic refactoring command. Preserve the raw feedback, mark interpretations as unconfirmed, and offer next actions instead of assuming an optimization task.

After task selection, use existing authority for low-risk `local_expression`. For `responsibility_boundary`, `abstraction_boundary`, `concept_boundary`, or `architecture`, automatically invoke group review and a Design Proposal. Human design acceptance is required only when explicitly reserved in `required_human_authorizations`.

Use consultation when human semantics or value judgments are necessary. State what was investigated, concrete options, the group recommendation, and what can proceed without an answer. No response is not approval, but it also does not stop work that has no required human wait.

Humans may evaluate, redirect, or challenge a proposal without supplying a technical solution. Agents must investigate and revise rather than merely defend or obey the first interpretation.

## 5. Authorize actions independently of task type

Create `.agent/changes/CHG-<id>.yaml` only after the user selects non-trivial work using the Change Manifest Schema.

Record `change_class` and `authorization_level` separately. The class describes task nature; the level describes impact and required action authority. Features and bug fixes may require any level.

- `local`: internal edits within existing agent authority.
- `independent_refactor`: structural work requiring a current implementation authorization from an authorized agent, human, or system.
- `architecture`: significant concept or boundary work requiring current design and implementation authorizations from authorized agents, humans, or systems.

An approval is not inherently human. Use `approver_type` to record the actual source. Use `required_human_authorizations` only for explicitly reserved decisions. Each listed kind requires current human approval before execution; all other approvals may come from an authorized agent or system.

Keep design acceptance, implementation, migration, compatibility change, security change, and production operation separate. Bind approval to plan revision, scope, conditions, approver, and source. Material plan changes invalidate affected approval. Design acceptance alone never authorizes implementation or operations.

Keep proposed extensions outside authorized scope. Pause only work that depends on missing authority or input. A failed repair does not expand repair authority. An autonomous workflow may contain reserved human authorizations; only dependent work waits.

When independent work is not dependent on the blocked operation, split it into a separate Change and complete it independently. Do not expand one Manifest into an operation-level scheduler.

Use `Blocked` for human and non-human waits. Set `waiting_for` to `consultation`, `authorization`, `external_dependency`, `environment`, `technical_resolution`, or `other`; use `authorization_kind` only for authorization waits.

## 6. Establish behavior protection

Before structural changes, identify observable behavior and invariants, establish or augment characterization tests where practical, and record the baseline and evidence limitations.

Run relevant checks during implementation. Bind final evidence to the resulting code revision. Never treat `not_run` or `inconclusive` as success. Keep functional and structural changes separate when combining them would obscure review or rollback.

## 7. Design from concepts and boundaries

- Identify concepts, rules, lifecycles, invariants, and reasons for change before creating classes.
- Give each concept one canonical home and one consistent project term.
- Split or merge because of concept ownership, consistency, dependencies, or change reasons—not line count alone.
- Prefer simple procedural code over unclear object networks when it is easier to understand.
- Avoid speculative abstractions and unnecessary generic containers.
- Preserve public names and protocols unless their change is authorized.

Stay within authorized scope during implementation. Check correctness, responsibility clarity, natural naming, dependency direction, test quality, and unnecessary complexity.

## 8. Run bounded global reflection

After a meaningful change within the selected task, inspect affected concepts, callers, dependencies, and invariants. Invoke a group only when local evidence justifies broader design judgment.

Return one outcome:

- `keep`: current design remains appropriate.
- `observe`: record an evidence-backed issue or opportunity for later.
- `propose`: propose separately authorized design work.

Do not reopen rejected designs without new evidence or start another user-unselected optimization cycle. Stop at the declared review budget. An agent-generated assumption or previous decision cannot be the sole reason to reject a better model. State separately whether an alternative is conceptually better and whether it should be implemented now.

## 9. Update knowledge conditionally

Documentation update is not required by default.

Update only when meaning changed:

- `current-model.md`: current concepts, invariants, module boundaries, or external constraints changed.
- ADR: a significant decision was accepted, rejected, or superseded.
- Knowledge records: a cross-task constraint, assumption, reference, design fact, or confirmed quality preference changed.
- Change Manifest: group participation, human input, authorization, execution state, scope, plan, or validation changed.

Keep raw feedback and unconfirmed interpretations in task records. Promote a quality preference only after a human confirms its cross-task applicability, scope, and source. Never turn preferences into absolute rules.

Keep one fact in one canonical location. Use `active`, `reference`, and `retired` as retrieval states. Exclude retired knowledge from default decision context. Archive completed execution records and extract durable knowledge only after verification and review.

## 10. Communicate and complete

- Architecture documentation explains current concepts, responsibilities, boundaries, and constraints.
- ADRs explain problems, alternatives, decisions, trade-offs, and revisit conditions.
- Change summaries explain background, decisions, impact, and verification.
- Comments explain non-obvious intent rather than restating code.
- Human questions explain why input is needed and what the agent group already investigated.

Do not turn every text into a chronological action log.

Before completion, ensure required validation passed or limitations were accepted, no unauthorized expansion occurred, dynamic human participation was not mistaken for blanket human control, and code, current design, and knowledge records remain consistent. Present further optimization as a separate user-selectable recommendation.
