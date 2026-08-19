# Domain Review Record

The auditable boundary between builder-generated and domain-reviewed content.
Rules in force are recorded in kyc-aml/generation/GENERATION.md with their
authority. This file records the review itself.

## Attribution levels

- **domain-author-ratified**: confirmed by the domain author. Highest weight.
- **domain-author-adjudicated**: builder proposed, domain author confirmed or
  corrected. Weaker than originated, and recorded as such.
- **design**: benchmark construction decision on builder authority; not a
  claim about banking practice.
- **unratified**: builder proposal awaiting the domain author. Not in force.

## Review 1: Stage 2 canonical scenario (AML-S01)

- stage: canonical-scenario
- reviewer_role: domain_author
- date: (pending)
- approved: PENDING

### Applied on builder authority (design)

GR-05, GR-08, GR-10, GR-11, GR-12, GR-13 as recorded in GENERATION.md. Two
changed AML-S01 materially:

1. The corporate registry extract no longer states that the two similarly
   named entities are unrelated. It lists the payee's registration details
   and its actual shareholders. The non-relationship is derived (C08) from
   differing registration numbers, jurisdictions, and shareholder lists.
2. The scenario gained non-load-bearing evidence: four routine domestic
   transactions and an insurance certificate on file for KYC refresh. No
   claim depends on them, and C14 records that fact explicitly.

### Awaiting ratification (unratified)

The ten domain-texture items listed at the end of GENERATION.md. Each is a
claim about real banking practice. Builder proposals for each exist in the
review materials; none is in force. Where the domain author marks an item
unresolved rather than confirming or correcting it, LIMITATIONS.md records
the corpus as unvalidated on that dimension rather than treating a builder
guess as authoritative.

### Note on provenance quality

Proposals in this review cycle originated with the builder and, where later
confirmed, would be adjudicated rather than authored by the domain author.
That is a weaker provenance than domain-originated texture and is recorded
here so no reader mistakes adjudication for origination.
