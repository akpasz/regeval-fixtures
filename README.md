# regeval-fixtures

Synthetic fixtures and a seed validation corpus for evaluating AI systems in
regulated financial workflows, beginning with a KYC/AML vertical slice.

All content is synthetic. Every customer, company, person, transaction, alert,
document and memo is generated. Nothing derives from any real case, filing or
record.

## Why this exists

The governance framework at
[ai-governance-gap](https://github.com/akpasz/ai-governance-gap) takes a
position in Section 04: validation evidence for a generative or agentic system
must demonstrate discrimination. For each test you must be able to say what a
failing system does that a passing system does not, and prove it by corrupting
a known good answer and confirming the check catches the defect. That framework
then states plainly that it does not supply a corpus.

This repository is a seed corpus toward that need, and an extensible
specification for building more. Twelve scenarios cannot represent regulated
finance. They can demonstrate a construction pattern and give a downstream
harness a stable contract.

## The central quality criterion

> The corpus must test a system's reasoning against evidence, not its ability
> to recognise the corpus author's construction patterns.

Four properties are proven independently, each by its own gate:

1. **Realistic enough.** Texture is authorised by the domain author, or
   recorded as unratified. See DOMAIN_REVIEW.md.
2. **Closed world, no leakage.** What a system may see is separated from what
   an evaluator knows, enforced across named leakage channels.
3. **Epistemically well specified.** Every material proposition is atomic and
   carries one of four statuses with passage level evidence.
4. **Mutations discriminate.** Each corruption introduces exactly one semantic
   defect of a declared class, and remains plausible in isolation.

## Named principle

**Domain plausibility, not production representativeness.** Domain plausibility
is reviewed by the domain author. Production representativeness is not claimed.

## The three layers

```
OBSERVABLE WORLD    kyc-aml/fixtures/     what a system under test may see
        |
        v
SYSTEM UNDER TEST   (not in this repository)
        |
        v
EVALUATION WORLD    kyc-aml/answers/      what the evaluator knows
        |
        v
MUTATION LAYER      validation-cases/corruptions/
```

Isolation is enforced by gates, not convention. No fixture may contain answer
key material, carry an evaluation-only field, or leak resolution state in a
filename.

## Epistemic model

Every claim carries exactly one status:

| status | meaning |
| --- | --- |
| `supported` | the observable world establishes it |
| `contradicted` | the observable world contains evidence against it |
| `not_provided` | no evidence either way; asserting it is fabrication |
| `indeterminate` | evidence exists and does not resolve the question |

There is no `partially_supported`. Claims are decomposed until each portion
carries one status. Evidence references cite passage IDs, never bare documents,
and every reference carries a type: `documented`, `stated_by_customer`,
`system_observation`, `analyst_observation`, `derived`, `unverified`.

## What is in the corpus

Twelve scenarios, 86 claims, twelve validation cases with twelve corruptions.
Each scenario is a closed world spanning customers, transactions, alerts,
documents, case notes and a policy context, with a complete answer key that
enumerates what the corpus does **not** support.

| id | construction | tier | disposition |
| --- | --- | --- | --- |
| AML-S01 | layered ownership, trust, entity name trap | 4 | continue with EDD |
| AML-S02 | cash deposits reconciled by later takings records | 2 | close |
| AML-S03 | wire funnel, unresponsive customer | 3 | escalate |
| AML-S04 | screening near match excluded on attributes | 5 | split |
| AML-S05 | prior closed case, unverified explanation | 3 | close |
| AML-S06 | invoice reconciliation, later evidence worsens | 2 | escalate |
| AML-S07 | dispersed ownership, no controller to find | 4 | close |
| AML-S08 | personal account, ownership inapplicable | 3 | escalate |
| AML-S09 | documentary scope, no transactions | 2 | close |
| AML-S10 | three mandate versions, effective dates | 4 | escalate |
| AML-S11 | transliteration variants, true match | 5 | escalate |
| AML-S12 | change of name, resolves to identity | 3 | close |

Eleven evaluation dimensions are covered, none by fewer than two scenarios:
citation, absence, ownership, qualifier, numerical, entity resolution, evidence
sufficiency, claim decomposition, temporal update, negative control,
disposition.

## Using it without a harness

Give a system a scenario's observable fixtures and the task from its validation
case. Compare the answer against the oracle in `validation-cases/cases*.yaml`:
required elements, forbidden elements, allowed variants, uncertainty
requirement. Then give the system the corrupted answer from `corruptions/` and
confirm your check detects the defect. If it does not, the check does not
discriminate, whatever it scores on the good answer.

## Reproducing

```
pip install pydantic==2.9.2 pyyaml==6.0.2
python tools/build.py
python -m unittest discover -s tests
```

`build.py` runs generate, coverage, diversity, anti-shortcut, manifest and
validate in order. Two clean runs under the pinned environment in
`environment.lock.yaml` produce byte-identical output. Portability means byte
identity across Windows, macOS and Linux under that same lock. No identity
claim is made outside it.

## The corpus contract

`schemas/corpus-contract.yaml` is the public API. A downstream consumer reads
statuses, evidence types, failure modes, oracle types, coverage dimensions,
scenario lifecycle and mutation rules from it rather than inferring them from
the directory layout.

## Licensing

Code under Apache 2.0 (`LICENSE-CODE`). Fixtures, schemas as published
artifacts, and documentation under CC BY 4.0 (`LICENSE-CONTENT`), including all
generated fixture content.

## Limitations

Read `LIMITATIONS.md` before use. In particular, AML/KYC domain texture is not
validated against practitioner experience, and the corpus makes no claim about
institutional field names, alert conventions, evidence sequencing, case note
style or investigation timing.

## Contributing

See `CONTRIBUTING.md` for the scenario admission requirements, the ID
retirement rule and versioning semantics.

Developed by [Kishor Akshinthala](https://www.linkedin.com/in/kishorakshinthala/).
