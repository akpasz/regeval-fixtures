# Changelog

Versioning starts at 0.1.0 deliberately. The corpus is a seed, its domain
texture is unratified, and its anti-shortcut audit is a limited heuristic. A
1.0 label would imply a maturity the repository does not claim.

## [0.1.0] - 2026-08-19

Initial release of the KYC/AML vertical slice.

**Corpus.** Twelve closed world scenarios, 86 atomic claims across four
epistemic statuses, twelve validation cases with twelve single defect
corruptions. Eleven evaluation dimensions covered, none by fewer than two
scenarios.

**Architecture.** Three layer separation of observable world, evaluation world
and mutation layer, enforced by gates. Passage level evidence provenance with
typed evidence. Machine readable ownership representation separating
documentary facts, derived relationships and control conclusions. Policy
context per scenario so dispositions are evaluation targets under declared
assumptions rather than assertions about practice.

**Verification.** Ground truth isolation, schema equality against a pydantic
source of truth with version stable emission, temporal availability, atomicity,
evidence resolution, coverage synchronisation, construction diversity, single
change locus and declared mutation class, name screening, forbidden strings and
determinism. One build entry point so no derived report can describe an earlier
state than the corpus.

**Provenance.** Six design rules in force on builder authority; ten claims
about banking practice recorded as unratified and not in force.

**Known limitations.** Domain texture unvalidated; anti-shortcut audit
implemented for six of thirteen feature checks and reported as PARTIAL;
construction outcome independence reported EXECUTED-PARTIAL, with document
light transaction scenarios currently all escalating.
