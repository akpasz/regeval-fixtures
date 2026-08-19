# Validation cases

Cases are held in `cases*.yaml`, one file per build batch during incremental
construction. All files matching `cases*.yaml` are jointly canonical, and the
validator reads them together. A consumer should glob the pattern rather than
opening `cases.yaml` alone.

Each case names a corruption in `corruptions/`. A corruption differs from its
known good answer at exactly one change locus, and the difference is semantic
rather than a formatting or plausibility artifact.

Consolidation into a single canonical index is a Stage 6 task.
