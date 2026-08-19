# Generation

Seed 20260630, reference date 2026-06-30, environment per
environment.lock.yaml. Regenerate: `python kyc-aml/generation/generate.py`
then `python tools/manifest.py`. Two clean runs are byte-identical under the
pinned environment. Names come from invented morphology with deterministic
collision avoidance (DD-015); name-registry.yaml is the screening reference.

## Rule provenance

Each rule below carries its authority. This distinction is load-bearing: a
rule about how an evaluation corpus should be constructed rests on benchmark
design reasoning, which the builder can supply. A rule about what a bank
system actually looks like rests on domain knowledge, which it cannot.

- **DESIGN**: benchmark construction decision, builder authority, in force.
- **DOMAIN-UNRATIFIED**: claim about real banking practice, proposed but not
  confirmed by the domain author. NOT in force. Recorded so the corpus does
  not silently adopt builder guesses as fact.

## Rules in force (DESIGN)

**GR-08 Source documents expose facts, not conclusions.** A source artifact
presents what a source records. Material analytical conclusions are derived
by the reader from those facts. Applied to AML-S01: the registry extract
lists the payee's actual shareholders and registration details; nothing
states that the entities are unrelated. The non-relationship is now claim
C08, derived from three source facts. Rationale: an evaluation testing
reasoning must not pre-write the reasoning into the evidence.

**GR-10 Temporal availability is a hard invariant.** No artifact may rely on
information unavailable at its own timestamp. Enforced by validator (DD-016).

**GR-11 Not every artifact is load-bearing.** Each scenario contains
plausible evidence that no evaluation target depends on. Applied to AML-S01:
four routine domestic transactions were added as explicitly non-load-bearing
evidence, recorded by claim C14; an insurance certificate (DOC-1006) was also
added as plausible contextual evidence and is deliberately not referenced by
any evaluation claim. The asymmetry is intentional: certifying every
irrelevant artifact in the answer key would make irrelevance itself a
benchmark signal. Rationale: a corpus where every document is answer-bearing
teaches recognition of construction rather than reasoning against evidence.

**GR-12 The canonical scenario is not a template.** Subsequent scenarios must
vary document structure, evidence distribution, ownership complexity,
narrative style, temporal pattern, and ambiguity placement. No AML-S01
defect composition is required elsewhere.

**GR-05 Evidence provenance is preserved.** Customer assertions,
independently sourced records, system observations, and derived conclusions
remain distinguishable via evidence_type. Already enforced by schema.

**GR-13 Variation over standardization.** Where a realism question has no
single correct answer across institutions, the corpus varies rather than
standardizing. No single alert style, field-naming convention, BO document
sequence, case-note format, or investigation duration is mandatory.

## Rules proposed but NOT in force (DOMAIN-UNRATIFIED)

These await domain-author ratification at the Stage 2 gate. Each is a claim
about real banking practice that the builder cannot validate. They are listed
in DOMAIN_REVIEW.md with their proposed content.

- Alert scenario-name form and the shape of a rule reference
- "Name match" versus similarity-score language in monitoring output
- Whether typology characterization appears in system output or only in
  analyst notes
- Customer record field naming (relationship_start_date, country_of_
  incorporation, industry_code) and the standard field set
- Whether risk_rating appears as an observable field
- Transaction record field set and remittance-reference conventions
- The realistic beneficial-ownership evidence packet and its arrival order
- Case-note length, register, and templated section structure
- Whether prior closed alerts appear as observable fixtures
- Realistic elapsed time from alert to first analyst action
