# SPDX-License-Identifier: Apache-2.0
"""Mechanical validation of a declared corruption (DD-026, completed).

A corruption declares what it changed, not merely that something changed:

    mutation_class      the kind of defect introduced
    expected_original   the exact span present in the known good answer
    expected_corrupted  the exact span that replaces it

The checks below verify all three against the actual text, so a mislabelled
corruption fails rather than passing on a negative test. Extracted from the
corpus validator so the invariant is unit testable in its own right."""
from __future__ import annotations

import re

PASSAGE = re.compile(r"\[[A-Z]+-\d+-P\d+\]")
ATTRIBUTION = re.compile(r"\b(stated|states|asserted|asserts|claimed|reported|"
                         r"according to|believes)\b", re.I)


def check(known_good: str, corrupted: str, mutation_class: str,
          expected_original: str, expected_corrupted: str) -> list[str]:
    """Return a list of findings. Empty means the corruption is valid."""
    out: list[str] = []

    # 1. the declared spans must be where they are declared to be
    if expected_original not in known_good:
        out.append("expected_original absent from the known good answer")
    if expected_original in corrupted:
        out.append("expected_original still present in the corrupted answer")
    if expected_corrupted not in corrupted:
        out.append("expected_corrupted absent from the corrupted answer")
    if expected_corrupted in known_good:
        out.append("expected_corrupted already present in the known good answer")

    # 2. replacing the declared span must reproduce the corrupted answer
    # exactly, which is what makes the mutation single and attributable
    if known_good.replace(expected_original, expected_corrupted) != corrupted:
        out.append("replacing the declared span does not reproduce the "
                   "corrupted answer, so other text also changed")

    # 3. the class must match what the declared spans actually do
    both = expected_original + " " + expected_corrupted
    if mutation_class == "citation_swap":
        if not (PASSAGE.search(expected_original) and PASSAGE.search(expected_corrupted)):
            out.append("citation_swap must replace one passage reference with another")
    elif mutation_class == "value_alteration":
        if not (re.search(r"\d", expected_original) and re.search(r"\d", expected_corrupted)):
            out.append("value_alteration must replace one value with another")
        if PASSAGE.search(both):
            out.append("value_alteration must not change a passage reference")
    elif mutation_class == "qualifier_flattening":
        if not ATTRIBUTION.search(expected_original):
            out.append("qualifier_flattening must remove an attribution phrase "
                       "from the original span")
        if ATTRIBUTION.search(expected_corrupted):
            out.append("qualifier_flattening must not leave the attribution intact")
    elif mutation_class in ("scope_extension", "reasoning_substitution",
                            "fabricated_activity"):
        if PASSAGE.search(both):
            out.append(f"{mutation_class} must not change a passage reference")
        if expected_original.strip() == expected_corrupted.strip():
            out.append("declared spans are identical")
    else:
        out.append(f"unknown mutation class {mutation_class}")
    return out
