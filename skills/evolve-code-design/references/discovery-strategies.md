# Structural Discovery Strategies

Use these strategies only after the user selects an overall goal and system scope for existing-code or existing-design review or optimization. The scope may span multiple modules or domains. Treat these strategies as exploration heuristics, not mandatory checklists, and do not manufacture findings to complete a view.

## Contents

1. Discovery loop and evidence levels
2. Six structural views
3. Group exploration protocol
4. Discovery record and exit conditions
5. Capability evaluation

## 1. Discovery loop and evidence levels

### Loop

1. **Frame**: Identify the overall goal, system scope, behavior questions, constraints, and available evidence. Do not expand scope without justification.
2. **Collect**: Inspect code, tests, call and event paths, configuration, data constraints, failure handling, and relevant change history.
3. **Reconstruct**: Build candidate structural views of states, rules, dependencies, responsibilities, changes, and recovery paths.
4. **Hypothesize**: State a falsifiable design problem, not a refactoring solution.
5. **Falsify**: Search for legitimate business differences, intentional isolation, alternative interpretations, and counterexamples.
6. **Validate**: Use tests, execution traces, data checks, dependency analysis, or repeated historical evidence to confirm or reject material impact.
7. **Decide**: Compare keeping the design, targeted verification, minimal repair, and redesign before proposing optimization.

For multi-module goals, aggregate validated candidates into an evolving opportunity map with material impact, dependencies, confidence, migration cost, validation options, and technical priority. Use it to choose and sequence work autonomously within the goal; do not require per-item user selection or treat it as a globally optimal roadmap.

### Evidence levels

Keep these levels distinct:

- **Observed**: Directly read from code, tests, configuration, data, traces, or history.
- **Reconstructed**: A structure that explains the observations.
- **Inferred**: A constraint, intention, or problem not yet proven by direct evidence.
- **Judgment**: A design or migration decision based on evidence and trade-offs.

A reconstructed structure is not automatically a defect. An inferred constraint is not automatically a user requirement.

## 2. Six structural views

### 2.1 State transition reconstruction

**Signals**

- Multiple fields, flags, or related records jointly determine available operations.
- Multiple components write the same state-defining fields.
- Retries, callbacks, jobs, and compensation change state through different paths.

**Reconstruct**

- Candidate states and the fields that define them.
- Operations and transitions, their guards, invariants, terminal states, and every writer.
- Retry, timeout, rollback, compensation, and event-order behavior.

**Falsify**

- Fields may be independent dimensions rather than one lifecycle.
- Different transitions may intentionally belong to different processes.
- A suspected illegal combination may be valid by business design.

**Validate**

- Test illegal combinations, duplicate transitions, retries, and out-of-order events.
- Compare guards across all entry points.
- Inspect data or traces for contradictory states when available.

**Possible responses**

Unify a guard, add characterization tests, clarify state ownership, consolidate a transition, or introduce an explicit state model only when it materially reduces demonstrated risk.

### 2.2 Cross-cutting rule tracing

**Signals**

- Semantically similar permission, amount, tenant, idempotency, time, or lifecycle rules appear in multiple paths.
- Some entry points omit a constraint enforced elsewhere.
- One rule change requires edits across otherwise unrelated modules.

**Reconstruct**

- The underlying rule, its owner, affected paths, semantic differences, and missing enforcement.
- Whether implementations share a genuine change reason.

**Falsify**

- Similar code may serve different business purposes.
- A path may intentionally differ because of its domain or risk model.
- Centralization may create a larger and less meaningful dependency.

**Validate**

- Compare behavior for identical inputs across entry points.
- Trace a rule change through every affected implementation.
- Ask domain owners only when code cannot resolve intended semantic differences.

**Possible responses**

Preserve local rules, document intentional differences, share a domain operation, centralize validation, or assign clear rule ownership without creating a generic service.

### 2.3 Implicit dependency reconstruction

**Signals**

- Components without static dependencies share tables, events, global state, configuration, or runtime conventions.
- A change in one component unexpectedly affects another.

**Reconstruct**

- Static calls plus data reads/writes, event subscriptions, shared state, configuration references, and deployment-time dependencies.
- Direction, ownership, and hidden cycles.

**Falsify**

- Shared infrastructure may be an intentional integration boundary.
- A static dependency cycle may not imply a domain cycle.

**Validate**

- Trace data or event flow across the reconstructed edge.
- Change or mock one side and observe the other in a controlled test.
- Compare actual integration behavior with the declared module boundary.

**Possible responses**

Make an implicit contract explicit, relocate ownership, reverse a dependency, isolate shared state, or preserve a deliberate integration mechanism.

### 2.4 Change propagation analysis

**Signals**

- Similar requirements repeatedly modify the same group of modules.
- Local patches cause broad regression or repeated follow-up fixes.

**Reconstruct**

- Co-change clusters, requirement-to-module mappings, call paths, and the rule or concept driving repeated changes.

**Falsify**

- Co-change may result from mechanical renames, formatting, generated code, or release-wide edits.
- Components may legitimately share one invariant.

**Validate**

- Inspect several distinct changes for the same causal mechanism.
- Separate semantic co-change from mechanical co-change.
- Measure whether a later change still requires the same diffusion.

**Possible responses**

Preserve coordinated ownership, introduce a stable seam, relocate a rule, or adjust a boundary only when propagation is demonstrably costly and recurring.

### 2.5 Responsibility and change-cause analysis

**Signals**

- A module handles business decisions, workflow coordination, and technical mechanisms.
- Different product concerns repeatedly modify the same class or module.
- Callers need internal knowledge to use an abstraction correctly.

**Reconstruct**

- The module's actual responsibilities, rules it owns, callers it serves, and reasons each responsibility changes.
- Whether responsibilities share identity, lifecycle, invariants, and change reasons.

**Falsify**

- Multiple methods may still express one cohesive concept.
- Small classes are not automatically clearer, and splitting may only move complexity to collaborators.

**Validate**

- Compare caller usage, test setup, modification reasons, and the ability to explain the module in one natural sentence.
- Check whether a proposed boundary actually localizes future changes.

**Possible responses**

Keep a cohesive module, rename it to match reality, extract a genuinely independent rule, merge artificial fragments, or redesign ownership.

### 2.6 Failure and recovery analysis

**Signals**

- Retry, timeout, rollback, compensation, and recovery logic is duplicated or inconsistent.
- Failures leave partial state or repeat side effects.

**Reconstruct**

- Failure modes, side effects, idempotency expectations, recovery owners, resource lifetimes, and state after every exit path.

**Falsify**

- Different recovery behavior may reflect different external guarantees.
- Retry may be safe for one operation and unsafe for another.

**Validate**

- Inject failures at side-effect boundaries.
- Test repeated delivery, partial completion, rollback, and recovery after restart.
- Verify invariants after recovery, not only successful return values.

**Possible responses**

Clarify failure semantics, add idempotent handling, unify recovery ownership, introduce compensation, or preserve different policies with explicit rationale.

## 3. Group exploration protocol

Treat concept design, skeptical review, evolution review, and coordination as functions that may each be performed by one agent or a nested team. Start with the least expensive approach that can obtain high-signal evidence, and add specialists only when material uncertainty justifies the cost.

Use independent starting points rather than assigning disjoint checklists:

- Concept design starts with business concepts, state behavior, and rule ownership, optionally splitting into concept, state, and rule specialists for larger scopes.
- Skeptical review starts with counterexamples, missing constraints, failure paths, and alternative explanations, optionally splitting into dependency and recovery specialists.
- Evolution review starts with dependencies, change history, migration cost, and long-term evolution, optionally splitting into testing, migration, and cost specialists.

Each function may use all six views. Each first records independent observations and hypotheses before seeing the coordinator's synthesis. Delegate session and model management to the host tool; use model diversity only when available and justified by risk and budget, otherwise use isolated contexts and detailed role frames.

During cross-review:

1. Compare reconstructed structures before comparing solutions.
2. Require evidence for important findings and explicit counterevidence checks.
3. Preserve unresolved disagreements and credible minority interpretations.
4. Do not convert agreement into proof or turn a discovered pattern directly into a refactoring pattern.
5. Reduce scope or stop when additional analysis no longer produces enough new evidence to justify its computational and human-attention cost.

## 4. Discovery record and exit conditions

Keep discovery records as task artifacts, not permanent documentation by default. Give each material opportunity a stable identity and lifecycle so later iterations preserve prior evidence and avoid duplicate work:

```text
discovered → investigating → validated → prioritized → selected → in_progress → resolved
                    ├─ rejected
                    ├─ deferred
                    └─ superseded
```

Do not reopen rejected opportunities without new evidence, and re-evaluate deferred ones only when their revisit conditions change.

```yaml
id: O-001
status: discovered | investigating | validated | prioritized | selected |
        in_progress | resolved | rejected | deferred | superseded
depends_on: []
observations:
  - Direct code, test, trace, data, or history facts
reconstructed_structure:
  description: Candidate structural model
  confidence: low | medium | high
problem_hypothesis:
  description: Falsifiable design problem and material impact
evidence_for: []
counterevidence: []
open_questions: []
validation:
  method: Test, trace, data check, dependency analysis, or historical comparison
  result: confirmed | rejected | inconclusive
complexity:
  recurring_cost_removed: ""
  migration_cost: ""
  permanent_conceptual_cost: ""
  operational_cost: ""
  maintenance_cost: ""
scope:
  execution_authorized: true
  outside_goal_dependencies: []
decision: keep | observe | propose | needs_input
rejected_reason: null
revisit_when: []
```

Treat dependency discovery outside the goal as analysis input only: record or propose it, but do not execute there without a new explicit goal or scope instruction. Compare recurring cost removed with migration and permanent conceptual, operational, and maintenance complexity, including agent sessions and documentation. Prefer a lower-complexity response or `keep` when lifecycle cost exceeds demonstrated benefit.

Exit rules:

- `keep`: no material defect is demonstrated, or the structure is reasonable.
- `observe`: a meaningful signal exists with a concrete future validation trigger.
- `propose`: material impact is supported and improvement options can be compared.
- `needs_input`: evidence cannot resolve a material business or authority question.

Do not use `propose` when the only support is aesthetic preference, pattern recognition, or a static metric.

When the next iteration has low or uncertain marginal value, enter `offer_stop` rather than declaring completion. Present outcomes, remaining candidates, expected value, uncertainty, and cheaper alternatives. If the user continues within the current goal, enter `user_directed` with a specific focus and next checkpoint; require a new hypothesis, perspective, or validation method rather than repetition. Continuation never overrides scope, authorization, or host hard limits.

## 5. Capability evaluation

Evaluate discovery on a real, moderately complex module rather than counting findings.

Compare ordinary single-agent review with group-based structural discovery on the same evidence:

- New material findings supported by evidence.
- False positives and rejected hypotheses.
- Findings that change a design or verification decision.
- Evidence coverage for states, rules, dependencies, changes, responsibilities, and recovery.
- Human usefulness, analysis time, context consumption, and report length.

The goal is better decisions with fewer unsupported findings, not more patterns or longer reports.
