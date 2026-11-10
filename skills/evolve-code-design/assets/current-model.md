# Current System Model

<!-- Keep this document focused on the accepted current design. Do not append task logs,
complete class inventories, or full ADR history. Split only when ownership or audience differs. -->

- Document owner: `<name-or-role>`
- Verified revision: `<commit-or-version>`
- Verification date: `<YYYY-MM-DD>`
- Scope: `<whole-system-or-bounded-context>`

## 1. System purpose

Explain the problem the system solves, its primary users, and the current scope in a few paragraphs.

`<Describe intent without narrating implementation history.>`

## 2. Core concepts and vocabulary

| ID | Canonical term | Human meaning | Owns | Does not own | Terms to avoid |
|---|---|---|---|---|---|
| `K-001` | `<Concept>` | `<Natural-language definition>` | `<Rules or state>` | `<Adjacent responsibilities>` | `<Ambiguous synonyms>` |

State important concept relationships below. Reference detailed decisions instead of repeating them.

`<Concept A> → <relationship> → <Concept B>`

## 3. Rules and invariants

| ID | Rule or invariant | Scope | How it is verified |
|---|---|---|---|
| `K-010` | `<Behavior that must remain true>` | `<Concept or module>` | `<Test, check, or review>` |

## 4. Current module boundaries

| Module | Responsibility | Must not depend on | Key collaborators |
|---|---|---|---|
| `<module>` | `<Current accepted responsibility>` | `<Forbidden dependency>` | `<Required collaborator>` |

Describe only dependencies and boundaries that a developer must understand to work safely. Generate exhaustive dependency graphs from code when needed.

## 5. External contracts and constraints

| Record ID | Constraint | Source | Impact |
|---|---|---|---|
| `C-001` | `<Protocol, compatibility, legal, or operational constraint>` | `<Authoritative reference>` | `<Design consequence>` |

## 6. Accepted design–implementation differences

Use this section only for intentional, unresolved differences. Remove entries when the transition finishes.

| Difference | Reason | Transition record | Current status |
|---|---|---|---|
| `<Accepted design vs. current implementation>` | `<Why the difference is temporarily valid>` | `<Change or ADR reference>` | `<active/blocked>` |

Unexpected differences are architecture drift: investigate rather than documenting them as intentional.

## 7. Active decision references

| Decision | Canonical reference | Current consequence |
|---|---|---|
| `<Short label>` | `<ADR or record ID>` | `<One current-state sentence; do not copy the ADR>` |

Superseded decisions remain in their historical location and stay out of the active model.
