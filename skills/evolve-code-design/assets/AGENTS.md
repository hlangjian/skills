# Agent Design Governance v0.1

## Purpose

Optimize for correct behavior, conceptual clarity, and ease of human understanding. Start only on an explicit user goal or explicit external workflow command. After the overall goal and system scope are selected, autonomous agents and temporary design groups discover opportunities, set technical priorities, decompose work, iterate, and verify across that scope. Humans participate through requirements, corrections, and aesthetic feedback rather than per-change scheduling.

Trivial edits require no design group, execution Manifest, or global review. Repository context may inform recommendations but must never start work by itself.

## 1. Invoke and frame the overall goal

When the user gives a concrete goal and system scope, begin without redundant task-selection questions. Analysis-only goals do not authorize modification.

When the user explicitly invokes this workflow without a concrete goal:

1. Inspect only the minimum context needed to recommend meaningful objectives.
2. Offer goal-level options such as system design assessment, domain optimization, bounded iterative optimization, or analysis-only.
3. Recommend one with a reason and wait for the user to select the overall goal and system scope. Use a structured question mechanism when available.
4. Do not start optimization before that selection.

The overall goal is selected once. Do not ask the user to select every subsequent work item, and do not expand into a new goal or system scope without another explicit instruction.

After goal selection, perform a lightweight evidence triage. Enter targeted stabilization only when conflicting facts, unclear authority, unverifiable critical behavior, or unsafe change boundaries make optimization unsafe. Otherwise continue directly with discovery and prioritization. Do not require stabilization for every legacy project.

When stabilization is required, read `references/legacy-stabilization.md`: execute relevant runtime checks where safe, establish evidence and conflict maps, define change impact and action boundaries, and stabilize only affected areas until they can safely support optimization. This is a targeted prerequisite, not whole-repository normalization.

## 2. Discover and prioritize opportunities autonomously

Read `references/discovery-strategies.md`. Analyze the whole selected goal scope, including multiple modules or domains when authorized:

1. Inspect code, tests, contracts, execution paths, dependencies, data, history, and current design knowledge.
2. Reconstruct state transitions, cross-cutting rules, implicit dependencies, change propagation, responsibility and change causes, and failure recovery.
3. Separate observed facts, reconstructed structures, inferred constraints, counterevidence, and open questions.
4. Form evidence-backed optimization candidates with material impact, dependencies, confidence, migration cost, and validation options.
5. Set technical priority and sequence using correctness, consistency, cognitive and change cost, dependency order, evidence confidence, migration risk, and the user's quality preferences.

Maintain an evolving opportunity map as an analysis artifact, not a permanent document by default. It guides autonomous work selection without claiming global optimality or replacing business strategy.

Give each material opportunity a stable identity and lightweight lifecycle so later iterations do not rediscover it or lose prior reasoning:

```text
discovered → investigating → validated → prioritized → selected → in_progress → resolved
                    ├─ rejected
                    ├─ deferred
                    └─ superseded
```

Keep dependencies, evidence references, rejection or deferral reasons, and `revisit_when` conditions. Do not propose rejected opportunities again without new evidence, do not reimplement resolved ones, and reopen deferred or rejected ones only when conditions change. Keep the map task-scoped unless an opportunity demonstrates durable cross-goal value.

## 3. Iterate within goal and budget

After goal selection, establish the acceptable cost envelope: compute and model calls, time, context, and human attention. If the user gives no preference, start with the least expensive approach that can obtain high-signal evidence and escalate only when material uncertainty or risk justifies it.

Use host-managed iteration, time, token, concurrency, session, and model budgets when available; do not recreate them as a separate configuration system. Track goal-level iterations and per-item rework semantically, and stop with current evidence and open questions when the host budget is exhausted rather than forcing a conclusion.

For each work item, without per-item user selection:

1. Choose the next evidence-backed opportunity according to the map and current authority.
2. Use one agent for local execution or form a temporary design group for material design judgment.
3. Compare current, minimal, and materially different designs where relevant, then obtain required authorization from an authorized agent, human, or system.
4. Implement an independently verifiable unit of work with explicit behavior and migration scope.
5. Validate behavior and claimed improvements, review side effects, and update the system model and opportunity map.
6. Reassess priorities and continue the next useful iteration within the same goal, host budget, and stop conditions.

Do not turn the goal into one giant unverifiable change. Execution units support verification; they do not limit overall optimization to a single Change. Reassess and revise the plan when later evidence invalidates earlier assumptions.

For every structural optimization, compare the recurring cost it removes with migration cost and permanent conceptual, operational, and maintenance complexity. Include the cost of new abstractions, agent sessions, review steps, documents, and knowledge records. Prefer a lower-complexity response or keep the current design when lifecycle cost exceeds demonstrated benefit.

Dependency discovery is not scope authorization. Agents may inspect out-of-scope dependencies to understand impact and record or propose opportunities, but must not execute changes there without a new explicit goal or scope instruction.

## 4. Compose role functions around budget

Treat concept design, skeptical review, evolution review, and coordination as functions, not fixed agent identities. Each function may be one agent, a small team, or a nested specialist group. Coordination itself may also be shared when scope requires it.

Start lean and escalate by evidence:

- **Lightweight**: one agent uses multiple reasoning frames, targeted tools, and asynchronous human feedback for small or low-risk problems.
- **Standard**: a small temporary group performs independent first-pass analysis, adversarial review, and focused verification for material design choices.
- **Deep**: nested specialist groups cover states, dependencies, failure recovery, testing, migration, and cost for high-impact or highly uncertain work.

Do not spend budget on more roles, documents, or agreement. Spend it on reducing consequential uncertainty. Downgrade scope or stop with unresolved questions when marginal evidence no longer justifies the cost.

Use role detail to diversify reasoning: concept design emphasizes domain meaning and lifecycles; skepticism emphasizes counterexamples, hidden dependencies, and failure conditions; evolution review emphasizes change causes, compatibility, and the cost of doing nothing. Require independent initial contexts and evidence inspection before conclusions are shared.

Delegate session creation, model selection, context isolation, and group conversation management to the host agent tool. When the host supports multiple models, use diversity for skeptical or high-risk review when affordable; otherwise use isolated contexts and detailed role frames. Do not create a separate model configuration or equate model diversity with truth.

The coordinator records adopted reasons, rejected alternatives, responses to material objections, unresolved disagreements, and credible minority positions. Decide by evidence rather than majority vote. Preserve candidates or the current design when evidence cannot distinguish them; `keep` is valid. Re-form only for new evidence, capability gaps, or demonstrated defects in the group's own proposal. The goal is better judgment, not a higher agreement rate.

## 5. Accept dynamic and asynchronous human participation

Humans may enter at any stage to add requirements, correct facts or implementation mistakes, express aesthetic preferences, redirect priorities, challenge the current design, or request a pause.

Treat “this design feels awkward” as an investigation signal, not a confirmed diagnosis or automatic refactoring command. Investigate and revise without demanding a technical solution from the human.

For reversible, low-risk work, offer asynchronous human evaluation instead of blocking independent progress. Provide a concise structure comparison, recommendation, evidence, open questions, and the exact revision being evaluated. Track evaluation conceptually as `pending`, `accepted`, `changes_requested`, `rejected`, or `superseded`.

`pending` is not acceptance and must not be reported as such. Continue only independent work that does not depend on that evaluation. Negative or corrective feedback reopens the affected work and updates the opportunity map. Irreversible or explicitly reserved high-risk operations still wait for their required evaluation or authorization.

Ask for human semantics or value judgments only when evidence cannot resolve a material decision. State what was investigated, options, the group recommendation, and what can proceed without an answer. Respect the user's attention budget when deciding whether and how often to ask.

## 6. Authorize and record execution only as needed

Record `change_class` separately from `authorization_level`; features and bug fixes may require any level.

- `local`: work within existing agent authority.
- `independent_refactor`: current implementation authorization from an authorized agent, human, or system.
- `architecture`: current design and implementation authorizations from authorized agents, humans, or systems.

An approval is not inherently human. Use `required_human_authorizations` only for explicitly reserved decisions. Overall agent autonomy may coexist with reserved human authorization; only dependent work waits.

Keep design acceptance, implementation, migration, compatibility change, security change, and production operation separate. Bind each to plan revision, scope, conditions, approver, and source. Material plan changes invalidate affected approval. Design acceptance alone never authorizes implementation or operations.

Create `.agent/changes/CHG-<id>.yaml` only for execution work whose authorization, state, or verification must persist. Manifests are optional execution records, not the unit that defines discovery, prioritization, iteration, or user involvement. Do not create one for every review comment or minor work item.

When independent work is not dependent on the blocked operation, split it into a separate execution record and continue. Do not expand one Manifest into an operation-level scheduler. A failed repair does not expand repair authority.

## 7. Verify improvements and reassess globally

Before a significant modification, define a small Change Impact Map using `references/legacy-stabilization.md`: known callers, bypass paths, verified paths, unknown coverage, evidence confidence, change risk, allowed changes, and validation. Evidence confidence and change risk are independent; restrict irreversible or broad actions when either is unfavorable.

Before structural changes, identify observable behavior and invariants, establish characterization tests where practical, and record baseline and evidence limitations. Bind final evidence to the resulting revision and never treat `not_run` or `inconclusive` as success.

Every optimization claim must state what specifically improved and use matching evidence: concept accuracy, rule ownership, and lifecycles for conceptual models; cohesion and change reasons for responsibilities; dependency direction, coupling, and change impact for module boundaries; shared language and reduced ambiguity for naming; behavior baselines, tests, and compatibility for behavior changes; and before/after measurements for performance, resources, or cost.

After meaningful work, reassess affected concepts, dependencies, invariants, and the opportunity map. Choose `keep`, `observe`, or `propose`. Use new evidence to revise the plan rather than defending earlier iterations.

Run a micro-stabilization check for concept overlap, new rule or state owners, bypass paths, evidence validity, temporary-compatibility lifecycle, and whether the next agent can still find the correct entry point. Fix micro-disorder within the current work item when possible, pause only affected work for local stabilization when several work items are involved, and enter targeted stabilization only when facts or behavior become unsafe. Never expand a local finding into whole-repository refactoring.

Default to sequential execution for dependent work. After integrating work items, repeat design-consistency and behavior verification rather than assuming independent success composes correctly. Later code changes invalidate affected prior evidence until revalidated. Pending asynchronous evaluation may remain unaccepted without preventing an evidence-based completion claim.

## 8. Update knowledge conditionally

Documentation update is not required by default. Update only when current concepts, boundaries, constraints, significant decisions, active assumptions, or confirmed cross-task quality preferences changed.

Keep one fact in one canonical location. Use `active`, `reference`, and `retired` as retrieval states independently of truth and decision status. Keep raw feedback in task records and promote quality preferences only after human confirmation of cross-task scope. Create an ADR only for a significant decision with durable trade-offs. Archive completed execution records and extract durable knowledge only after verification and review.

## 9. Stop and communicate

At each checkpoint, compare the next iteration's evidence-backed benefit with execution, migration, complexity, and human-attention costs. If continuing has sufficient value, proceed. Otherwise enter `offer_stop`: present current outcomes, remaining candidates, expected value, uncertainty, and cheaper alternatives without declaring the goal complete.

At `offer_stop`, the user may stop or continue. When the user explicitly continues within the current goal, enter `user_directed`: record the focus, unchanged scope, continuation reason, and next checkpoint. Continue with a new hypothesis, perspective, or validation method rather than repeating low-value work. User continuation does not override forbidden scope, required authorization, or host hard limits, and `no_material_opportunity` does not override an explicitly unmet user preference. Continuous mode still requires periodic checkpoints.

Stop when the goal is satisfied, the user stops, host limits are reached, required input is unavailable, or no continuation is selected after `offer_stop`.

Report goal progress, implemented changes, group conclusions and unresolved disagreements, validation evidence and limitations, human input and reserved authorizations when used, remaining opportunity candidates, and documentation changes or why none were needed. Present work outside the current goal as a new recommendation, not an automatically started iteration.

Use natural, purpose-appropriate explanations rather than chronological action logs. Architecture documentation explains current concepts, ADRs explain significant decisions, and change summaries explain background, impact, and verification.

## 10. Scope and limits

This workflow can analyze and optimize multiple modules or domains under one overall goal, and agents set their own technical priorities and iteration plans. It does not decide business strategy, staffing, financial budgets, or portfolio-level roadmaps, and it does not guarantee global optimality.

Conclusions depend on available evidence. Business ownership and authority questions may require human judgment. Detailed role framing and optional model diversity reduce anchoring but do not guarantee independence or truth. Budget includes human attention as well as compute, time, and context; asynchronous evaluation is pending until the human responds.

Never claim complete discovery of disorder. Record covered and uncovered areas, evidence confidence, and allowed actions; broader or irreversible actions require stronger coverage and evidence.

This workflow is not a CI/CD system, production operator, performance or security certification process, migration executor, or project-delivery manager. Small execution tasks should bypass its design-group and documentation workflow.
