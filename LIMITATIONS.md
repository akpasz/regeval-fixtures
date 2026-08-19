# Limitations

Stage 2 draft. Finalized at Stage 6.

## Domain texture is unvalidated

AML/KYC domain texture remains unvalidated against practitioner experience.
The corpus makes no claim about institutional field names, alert conventions,
evidence-pack sequencing, case-note style, prior-alert prevalence, or
investigation timing. Where the fixtures adopt a convention in these areas,
it is a builder construction, recorded as unratified in
kyc-aml/generation/GENERATION.md and DOMAIN_REVIEW.md, not a representation
of how any institution operates.

## Synthetic data limits

Synthetic fixtures cannot capture the volume, noise, and inconsistency of
production data. No claim is made that a system passing on this corpus will
perform comparably in production.

## Name screening

Screening is a risk-reduction mechanism, not an assertion of uniqueness.
Heuristic screening cannot establish that a generated name matches no real
person or entity. See tools/SCREENING.md.

## Scale

The corpus is a seed: a small number of scenarios cannot represent the range
of regulated financial workflows, and coverage of any evaluation dimension by
one or two scenarios is single-point-of-proof, reported as such by the
coverage tooling.

## Scope and labels

The corpus models synthetic U.S. banking workflow conventions and does not
represent the requirements of any specific institution, regulator,
jurisdiction, or compliance program. Coverage labels describe synthetic
scenario design and evaluation targets; they are not a typology taxonomy,
red-flag catalogue, detection rule set, or monitoring tuning methodology.
Failure modes describe system behaviour under evaluation, not
suspicious-activity categories.

## Ownership arithmetic

Ownership percentages and thresholds in fixtures are illustrative synthetic
arithmetic. They are not institutional beneficial-ownership determinations
and carry no regulatory meaning.

## Independence checking

The anti-shortcut audit is heuristic. At this corpus size obvious leakage can
be caught; statistical independence cannot be established, and the report
states so.
