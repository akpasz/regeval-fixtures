# SPDX-License-Identifier: Apache-2.0
"""Unit tests for the declared mutation invariant (DD-026). These exercise the
checker directly with valid and deliberately mislabelled corruptions, so the
invariant is proven rather than only exercised through the corpus."""
import pathlib
import sys
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import mutation_check  # noqa: E402

GOOD = "The registry extract [DOC-1005-P01] records 26,500 monthly. The customer stated it was paid."


class TestMutationCheck(unittest.TestCase):
    def test_valid_citation_swap(self):
        bad = GOOD.replace("[DOC-1005-P01]", "[DOC-1004-P01]")
        self.assertEqual(mutation_check.check(
            GOOD, bad, "citation_swap", "[DOC-1005-P01]", "[DOC-1004-P01]"), [])

    def test_citation_swap_without_a_citation_is_rejected(self):
        bad = GOOD.replace("26,500", "22,000")
        f = mutation_check.check(GOOD, bad, "citation_swap", "26,500", "22,000")
        self.assertTrue(any("passage reference" in x for x in f))

    def test_valid_value_alteration(self):
        bad = GOOD.replace("26,500", "22,000")
        self.assertEqual(mutation_check.check(
            GOOD, bad, "value_alteration", "26,500", "22,000"), [])

    def test_value_alteration_without_a_value_is_rejected(self):
        bad = GOOD.replace("The customer stated", "The file documents")
        f = mutation_check.check(GOOD, bad, "value_alteration",
                                 "The customer stated", "The file documents")
        self.assertTrue(any("one value with another" in x for x in f))

    def test_valid_qualifier_flattening(self):
        bad = GOOD.replace("The customer stated", "The file documents")
        self.assertEqual(mutation_check.check(
            GOOD, bad, "qualifier_flattening",
            "The customer stated", "The file documents"), [])

    def test_qualifier_flattening_keeping_attribution_is_rejected(self):
        bad = GOOD.replace("The customer stated", "The auditor stated")
        f = mutation_check.check(GOOD, bad, "qualifier_flattening",
                                 "The customer stated", "The auditor stated")
        self.assertTrue(any("attribution intact" in x for x in f))

    def test_declared_span_must_be_present(self):
        bad = GOOD.replace("26,500", "22,000")
        f = mutation_check.check(GOOD, bad, "value_alteration", "99,999", "22,000")
        self.assertTrue(any("expected_original absent" in x for x in f))

    def test_other_text_changing_is_rejected(self):
        bad = GOOD.replace("26,500", "22,000").replace("monthly", "weekly")
        f = mutation_check.check(GOOD, bad, "value_alteration", "26,500", "22,000")
        self.assertTrue(any("other text also changed" in x for x in f))

    def test_unknown_class_is_rejected(self):
        bad = GOOD.replace("26,500", "22,000")
        f = mutation_check.check(GOOD, bad, "typo", "26,500", "22,000")
        self.assertTrue(any("unknown mutation class" in x for x in f))

    def test_every_corpus_corruption_is_valid(self):
        d = ROOT / "kyc-aml" / "validation-cases" / "corruptions"
        files = sorted(d.glob("*.yaml"))
        self.assertGreater(len(files), 0)
        for f in files:
            c = yaml.safe_load(f.read_text())
            self.assertEqual(mutation_check.check(
                c["known_good_answer"], c["corrupted_answer"], c["mutation_class"],
                c["expected_original"], c["expected_corrupted"]), [], f.name)


if __name__ == "__main__":
    unittest.main()
