# Design Decisions

Compact log. Each entry: decision, rationale, alternatives rejected, impact.

## DD-001 Closed-world scenarios
Scenario as the unit, with strict observable-world / evaluation-world /
mutation-layer separation enforced by gates. Rejected: flat fixture library
(no leakage guarantees). Impact: directory layout, isolation tests.

## DD-002 Four epistemic statuses plus atomicity
supported / contradicted / not_provided / indeterminate, with claims
decomposed until each carries one status. Rejected: partially_supported
(pushes ambiguity into scoring). Impact: claim schema, oracle contracts.

## DD-003 Passage-level provenance
Evidence references cite passage IDs, never bare documents. Rejected:
document-level citation (cannot test citation-to-passage). Impact: document
fixture schema.

## DD-004 No SAR simulation
No SAR labels in fixtures; no simulated filing artifacts; the term appears
only in documentation explaining this boundary. Rejected: fictional SAR
facsimiles (inappropriate under SAR confidentiality norms even as fiction).

## DD-005 Invented-morphology naming
Names built from constructed syllables; no real-name-pool libraries.
Screening verifies fixture names against the generator's emitted registry.
Rejected: faker-style pools (real-name collision risk). Impact: screening.py.

## DD-006 Three-level ownership representation
documentary_facts / derived_relationships / control_conclusions kept apart.
Rejected: single ownership graph (conflates evidence, arithmetic, judgment).

## DD-007 Two-level determinism
Reproducibility under environment.lock.yaml; portability across OSes under
that same lock; no claim across unpinned environments. Rejected: universal
byte-identity claims (unprovable).

## DD-008 Single-defect plausible mutations
One semantic defect per corruption; must remain plausible in isolation.
Rejected: compound or absurd mutations (detection unattributable or trivial).

## DD-009 Corpus contract as public API
schemas/corpus-contract.yaml carries meanings; generated JSON Schemas carry
shapes. Downstream consumers read the contract, not the directory layout.

## DD-010 Separation from evaluation machinery
No scorers, runners, adapters, or semantic evaluation anywhere. Rejected:
bundling a harness (blurs corpus validity with evaluator behavior).

## DD-011 Pydantic as single schema source
schemas/*.schema.json generated from tools/_schema_models.py so published
schemas and runtime validation cannot drift. Rejected: hand-written JSON
Schema alongside code (two normative sources).

## DD-012 Python 3.12.3 pin (specification deviation)
The build specification named 3.11.x; the build environment provides 3.12.3.
The operative requirement is an exact pin, which environment.lock.yaml makes.
Flagged for domain-author ratification at the Stage 1 gate.

## DD-013 Stage 1 probe fixture
CUST-0000 exercises the full generation path to prove determinism before any
scenario exists. Retired when AML-S01 lands; scenario_ref STAGE1-PROBE marks
it unmistakably as non-corpus content.

## DD-014 Corporate suffix allowlist in screening
Generic suffixes and descriptors (Ltd, S.A., Trust, Holdings, Holding,
Components, Trading) carry no identity and are exempt from the morphology
pattern. Explicit synthetic design choice. Impact: screening.py.

## DD-015 Token distinctness across scenario roles
All scenario names route through a deterministic collision-avoidance helper
so the only name similarity in a scenario is a deliberate one. Found when
AML-S01's first generation gave a person the same token as the entity-trap
companies. Rejected: accept collisions (unintended confounds pollute the
anti-shortcut audit). Impact: generate.py, all scenarios.

## DD-016 Temporal consistency gate
No dated artifact may contain a date later than its own. Found by external
review of AML-S01 (a case note knew the reference date twelve days in its
future); fixed in content and converted into a permanent validator gate.

## DD-017 C12 decomposition and atomicity gate
An external review found AML-S01-C12 bundled three propositions carrying
different statuses (registry silence, entity-level relationship, personal
relationships with principals, arm's length character). Decomposed into C12,
C12a, C12b, C12c and converted into a validator gate flagging conjunctive
propositions for review. The scenario gained claim_decomposition and
evidence_sufficiency coverage as a result.

## DD-018 Numerical construction variety (Stage 3 constraint)
AML-S01 places an undocumented USD 98,000 against a USD 100,000 threshold.
The near-threshold construction is retained as a deliberate numerical trap,
with a Stage 3 constraint: no more than two scenarios may use a near-miss
threshold construction, and no two may use the same margin or the same round
threshold, so the pattern does not become recognizable corpus grammar.

## DD-019 Schema regeneration drift gate
The published JSON Schemas are generated from tools/_schema_models.py. An
external review found the repository shipped with scenario.schema.json stale
after the models changed: the generation step had been run in the build
environment but the regenerated artifact was not carried into the delivered
archive. The validator now compares every published schema against the source
model on every run, so drift fails a gate rather than a test alone.

## DD-020 Design authority versus domain authority
Review proposals split into benchmark-construction rules (builder authority,
adopted: GR-05, GR-08, GR-10, GR-11, GR-12, GR-13) and claims about real
banking practice (domain-author authority, recorded unratified). The split
exists because an LLM review cannot ratify a domain claim, however confidently
argued, and adjudication by the domain author is weaker provenance than
origination. GENERATION.md carries authority per rule.
