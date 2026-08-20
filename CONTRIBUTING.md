
## Scenario admission

A scenario is admitted when it: adds or deliberately reinforces a coverage
dimension; carries claims that are individually supported by observable
passages; states a disposition grounded in its policy context; introduces no
future knowledge; differs structurally from existing scenarios rather than only
in story; and does not announce its own answer in a source document.

## Identity and versioning

Scenario IDs are immutable and never recycled. Patch: documentation or non
semantic metadata. Minor: added content that does not invalidate existing
claims. Major: changed claim status, evidence, evaluation target, observable
fixture or answer semantics, which retires the ID.

## Building

`python tools/build.py` is the only supported build path. It owns the order of
generation, reports, manifest and validation. Do not regenerate a report
independently.
