# Legacy Stabilization Protocol

Use this protocol only when the selected goal includes conflicting facts, unclear authority, unverifiable critical behavior, or unsafe change boundaries. Do not run it for every legacy project, and do not turn stabilization into whole-repository normalization.

## Contents

1. Mode triage
2. Runtime and evidence baseline
3. Change impact and action boundaries
4. Local stabilization and gradual convergence
5. Micro-stabilization during iteration
6. Exit conditions and outcome evaluation

## 1. Mode triage

### Enter stabilization when material signals exist

- Build, startup, deployment, or test status is unknown.
- Documentation, code, configuration, and observed behavior conflict.
- Multiple implementations or architectures coexist without clear routing or ownership.
- Critical business semantics or compatibility requirements are undocumented.
- Shared state, runtime conventions, callbacks, retries, or external consumers create hidden dependencies.
- A small change may have broad unknown impact.

### Continue with optimization when evidence is sufficient

- Critical paths are reproducible and verifiable.
- Relevant facts have sources and scope.
- High-impact dependencies and compatibility constraints are understood.
- Current change can be bounded and verified.

Use a lightweight global triage followed by deep analysis only for high-risk areas. Do not require complete repository understanding.

### Apply three levels, not three equal-weight loops

- **Micro-stabilization**: lightweight checks after meaningful changes.
- **Optimization**: continuous work when evidence supports the current decision.
- **Stabilization**: targeted deeper work when critical facts or change boundaries are unsafe.

## 2. Runtime and evidence baseline

### Execute before claiming

When relevant and safe, actually run build, tests, and local startup. Do not infer runtime health from documentation.

Record for each:

```yaml
status: PASS | FAIL | BLOCKED | NOT_RUN
revision: <commit or version>
environment: <local, CI, container, service dependencies>
evidence_ref: <command output or run reference>
```

`BLOCKED` is not failure, and `NOT_RUN` is not success. If the environment is unavailable, limit action scope rather than waiting indefinitely or claiming runtime verification.

### Build an Evidence & Conflict Map as a task artifact

```yaml
claim:
  statement: What external path is the users API?
current_behavior: unverified
original_intent: unknown
compatibility_requirements: unknown
target_behavior: undecided
sources:
  - ref: README.md
    status: outdated_claim
  - ref: frontend/api.ts
    status: observed_call
  - ref: backend/routes.ts
    status: observed_registration
status: disputed | confirmed | inferred | unknown
next_validation: Inspect gateway configuration and execute an API contract test
```

Separate:

- **Current behavior**: what the implementation and runtime do now.
- **Original intent**: what the design was meant to do.
- **Compatibility requirements**: behavior external actors still depend on.
- **Target behavior**: the explicitly decided future behavior.

### Respect evidence limits

| Evidence | Can support | Cannot prove alone |
|---|---|---|
| Source code | An implementation exists | It is used in production or is correct |
| Static call graph | A potential call path | Runtime always follows it |
| Unit test | Specific assertions hold in a fixture | Business behavior is correct |
| Integration test | Components cooperate in a test environment | No other production dependencies exist |
| Deployment config | A deployment intention or configured value | The configuration is active everywhere |
| Production logs | Behavior occurred in a time window | All consumers and paths are known |
| Characterization test | Current behavior is characterized | Current behavior should be preserved forever |

## 3. Change impact and action boundaries

Before a significant modification, create a small Change Impact Map:

```yaml
target: OrderService.update_status
known_callers:
  - api/order_controller
  - payment/webhook
  - jobs/order_recovery
known_bypass_paths:
  - legacy/payment_handler
verified_paths:
  - api/order_controller
unknown:
  - external integrations
  - production recovery scripts
  - dynamic configuration
coverage: partial
evidence_confidence: medium
change_risk: high
allowed_change:
  - add characterization tests
  - add an adapter
  - migrate a verified internal caller
restricted_change:
  - remove the legacy handler
  - redesign the order state machine
validation:
  - old/new behavior comparison
  - state consistency check
```

### Decide using two independent dimensions

- **Evidence confidence**: how well current behavior and constraints are understood.
- **Change risk**: blast radius, irreversibility, compatibility, data, security, and operational impact.

| Evidence | Risk | Action |
|---|---|---|
| High | Low | Proceed within the selected goal and existing authority |
| High | High | Increase verification, recovery, integration checks, and migration controls |
| Low | Low | Prefer local reversible work and observation; do not claim broad understanding |
| Low | High | Do not perform structural deletion, migration, or redesign; investigate or request a decision |

Risk is not automatic human approval, and evidence is not execution authority. Use the existing authorization model for actual permission.

### Coverage is explicit, never presumed complete

Record `covered`, `not_covered`, `unknown`, and `allowed_actions`. Typical uncovered areas include external consumers, dynamic registration, production scripts, feature flags, retries, and deployment-specific behavior.

A local scan proves only what was inspected. A finding of no disorder is limited to the recorded evidence and coverage.

## 4. Local stabilization and gradual convergence

### Classify conflicts before acting

- **Outdated description**: verify and update the description.
- **Technical defect**: fix and add regression evidence.
- **Legitimate domain difference**: preserve and document scope.
- **Historical compatibility**: isolate and adapt before migration.
- **Unknown business semantics**: retain `unknown` and request a business decision only when the answer affects action.

### Find propagation sources before cosmetic cleanup

Prioritize:

- Multiple authorities for one concept.
- Multiple owners of one business rule.
- Multiple writers of one state.
- Multiple entry points for one operation.
- Multiple configurations controlling one behavior.

### Isolate, migrate, then converge

For competing implementations:

1. Compare behavior, including validation, side effects, retries, and recovery; unknown is not “absent.”
2. Identify real consumers using static evidence, configuration, logs, contracts, and runtime traces where available.
3. Establish a stable adapter or entry point without deleting old implementations.
4. Make behavioral differences explicit in tests and contracts.
5. Migrate one verified caller and validate old/new behavior and integration.
6. Migrate subsequent callers only when evidence supports each step.
7. Consider deleting an old implementation only after remaining consumers and compatibility requirements are known.

Local consistency is preferred over global uniformity: identical semantics use identical rules; different semantics get explicit boundaries.

## 5. Micro-stabilization during iteration

After meaningful work, check only affected concepts and their fan-out:

- **Concept overlap**: was another name or abstraction introduced for an existing concept?
- **Rule ownership**: is there a new writer or authority for the same rule or state?
- **Bypass paths**: does new code bypass the established service, contract, or adapter?
- **Evidence validity**: do prior tests and design judgments still apply to the current revision?
- **Transition state**: is temporary compatibility logic owned, bounded, and scheduled for removal or re-evaluation?
- **Future maintainability**: can the next agent find the correct concept, rule, and entry point?

Handle findings at the smallest effective level:

- Fix micro-disorder within the current work item when possible.
- Pause affected work for local stabilization when multiple work items are affected.
- Enter targeted stabilization only when critical facts or behavior are no longer safe to change.
- Do not expand a local finding into whole-repository refactoring.

## 6. Exit conditions and outcome evaluation

### Exit stabilization when the baseline supports optimization

- Critical paths build and can be verified, or limitations are explicit.
- Material facts have sources, scope, and confidence.
- High-impact dependencies and compatibility constraints are known.
- Conflicts are classified, and unknowns are explicit.
- New development has clear local conventions and entry points.
- Current change has a bounded impact map, validation, and recovery path.

Exit does not mean the repository is uniformly designed or all chaos is eliminated.

### Keep governance artifacts temporary by default

- Do not create permanent maps for every observation.
- Retain only information with future decision value.
- Current-state records need owner, scope, verified revision, and invalidation conditions.
- Generate dependency and impact views from evidence when possible instead of maintaining parallel documents.

### Measure outcomes, not documentation volume

Useful signals include:

- **Impact prediction error**: actual impact exceeds or differs from the pre-change estimate.
- **Repeated decisions**: the same problem is repeatedly reanalyzed without new evidence.
- **New writers or bypasses**: new state owners or paths around the accepted boundary.
- **Critical path verifiability**: which high-risk paths can actually be exercised and checked.
- **Regression and recovery**: whether changes fail, roll back, or recover safely.
- **Future decision cost**: whether later work finds the correct rule and entry point faster.

Use these as review signals, not scoring targets.

### Adversarial acceptance checks

- **Dual implementations**: agent compares behavior and callers before deleting anything.
- **Unknown external consumer**: agent marks the unknown and restricts migration.
- **Documentation conflict**: agent verifies runtime facts instead of choosing the newest document.
- **Iteration-created writer**: agent detects a second state writer and stabilizes locally before continuing.
- **Undecidable business semantics**: agent stops only dependent decisions and presents evidence and alternatives rather than guessing.
