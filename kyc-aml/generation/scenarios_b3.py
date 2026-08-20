# SPDX-License-Identifier: Apache-2.0
"""Stage 3 batch 3: AML-S08, AML-S09, AML-S10.

Construction profiles deliberately absent from batches 1 and 2:

S08  ownership is genuinely irrelevant; the question is source of funds on a
     personal account, and no corporate structure exists to analyse.
S09  no transaction world and no screening artefact: the difficulty is
     entirely documentary, resting on what a certificate does and does not
     attest.
S10  three versions of one document, one superseding another, where the
     latest version is not the one that governs the period under review.

Dispositions continue to cut across tiers (S08 tier 3 escalate, S09 tier 2
close, S10 tier 4 escalate) so tier remains uninformative about outcome.
"""
from __future__ import annotations

MUTATION_CLASS = {'VC-01': 'citation_swap', 'VC-02': 'reasoning_substitution', 'VC-03': 'reasoning_substitution', 'VC-04': 'fabricated_activity', 'VC-05': 'qualifier_flattening', 'VC-06': 'value_alteration', 'VC-07': 'value_alteration', 'VC-08': 'scope_extension', 'VC-09': 'scope_extension', 'VC-10': 'value_alteration', 'VC-11': 'reasoning_substitution', 'VC-12': 'scope_extension'}


def _mk(g, scenario_id):
    M = {"marker": g.MARKER, "corpus_version": g.CORPUS_VERSION}
    def fx(fid, ftype, extra):
        return {"fixture_id": fid, "fixture_type": ftype,
                "scenario_ref": scenario_id, "synthetic": dict(M), **extra}
    def ev(fid, pid, etype):
        return {"fixture_id": fid, "passage_id": pid, "evidence_type": etype}
    return M, fx, ev


# ---------------------------------------------------------------- S08
def build_s08(g) -> dict:
    """Personal account, no corporate structure, no ownership question. The
    evaluation turns on whether a documented sale accounts for the credits.
    Tier 3, escalate."""
    S = "AML-S08"
    M, fx, ev = _mk(g, S)
    taken: set = set()
    person = (f"{g.distinct_name('given','S08-P',taken)} "
              f"{g.distinct_name('person','S08-P',taken)}")
    buyer = (f"{g.distinct_name('given','S08-B',taken)} "
             f"{g.distinct_name('person','S08-B',taken)}")
    third = (f"{g.distinct_name('given','S08-T',taken)} "
             f"{g.distinct_name('person','S08-T',taken)}")

    f = {}
    f["fixtures/customers/CUST-8001.yaml"] = fx("CUST-8001", "customer", {"record": {
        "legal_name": person, "customer_since": "2011-05-16",
        "business_description": "personal account, retired schoolteacher",
        "domicile": "domestic", "as_of": g.REFERENCE_DATE}})
    creds = [("C01", "2026-04-14", 140000, buyer),
             ("C02", "2026-04-28", 95000, third),
             ("C03", "2026-05-12", 95000, third),
             ("C04", "2026-05-26", 70000, third)]
    f["fixtures/transactions/TXN-8001.yaml"] = fx("TXN-8001", "transaction_set", {
        "record": {"account_ref": "CUST-8001", "currency": "USD"},
        "transactions": [{"txn_id": f"TXN-8001-{i}", "value_date": d,
                          "direction": "inbound", "amount": a,
                          "counterparty_name": n, "channel": "domestic wire",
                          "narrative": "no reference"} for i, d, a, n in creds]})
    f["fixtures/alerts/ALT-8001.yaml"] = fx("ALT-8001", "alert", {
        "record": {"alert_date": "2026-06-01", "rule_ref": "PRS-05",
                   "subject_ref": "CUST-8001"},
        "passages": [
            {"passage_id": "ALT-8001-P01", "locator": {"type": "narrative", "index": 1},
             "text": ("Scenario PRS-05. Personal account credits of 400,000 across "
                      "four inbound wires in seven weeks against a recorded income "
                      "profile of pension receipts only.")}]})
    f["fixtures/documents/DOC-8001.yaml"] = fx("DOC-8001", "document", {
        "title": "Property sale completion statement", "doc_date": "2026-04-13",
        "passages": [
            {"passage_id": "DOC-8001-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"Sale of residential property by {person} to {buyer} "
                      "completed 13 April 2026. Net proceeds to the seller after "
                      "costs and redemption: 140,000, payable by the buyer's "
                      "conveyancer.")}]})
    f["fixtures/case-notes/CN-8001.yaml"] = fx("CN-8001", "case_note", {
        "record": {"note_date": "2026-06-20", "author_role": "analyst"},
        "passages": [
            {"passage_id": "CN-8001-P01", "locator": {"type": "note", "index": 1},
             "text": ("Customer provided the completion statement for the April "
                      "credit. Asked about the three later credits from a different "
                      "remitter, the customer said they related to the same sale. "
                      "No further documentation was offered and the completion "
                      "statement records a single payment.")}]})
    f["fixtures/policy/POL-8001.yaml"] = fx("POL-8001", "policy_context", {
        "record": {"jurisdiction": "United States (synthetic institution)",
                   "policy_assumptions": [
                       "a documented one off receipt may explain a credit of the "
                       "same amount from the same payer"],
                   "decision_rules": [
                       "escalate where credits materially exceed the documented "
                       "source and the excess is unexplained",
                       "a customer explanation inconsistent with the document it "
                       "relies on does not evidence the activity"]},
        "passages": [
            {"passage_id": "POL-8001-P01", "locator": {"type": "clause", "index": 1},
             "text": ("An explanation that the supporting document contradicts is "
                      "not treated as partial support.")}]})

    claims = [
     {"id": f"{S}-C01", "proposition": "The April credit of 140,000 corresponds to the documented property sale.",
      "status": "supported", "evidence": [ev("DOC-8001", "DOC-8001-P01", "documented"),
                                          ev("TXN-8001", "TXN-8001-C01", "documented")],
      "rationale": "Amount, date and payer all correspond."},
     {"id": f"{S}-C02", "proposition": "The three later credits of 260,000 relate to the same property sale.",
      "status": "contradicted", "evidence": [ev("DOC-8001", "DOC-8001-P01", "documented"),
                                             ev("CN-8001", "CN-8001-P01", "stated_by_customer")],
      "rationale": "The completion statement records one payment of 140,000 from the buyer's conveyancer. The customer's explanation is inconsistent with the document it relies on."},
     {"id": f"{S}-C03", "proposition": "The customer said the later credits related to the same sale.",
      "status": "supported", "evidence": [ev("CN-8001", "CN-8001-P01", "stated_by_customer")],
      "rationale": "The statement was made and is recorded, whatever its accuracy."},
     {"id": f"{S}-C04", "proposition": "The source of the 260,000 is documented.",
      "status": "not_provided", "evidence": [],
      "rationale": "Nothing in the corpus evidences it."},
     {"id": f"{S}-C05", "proposition": "The customer holds a corporate interest relevant to this review.",
      "status": "not_provided", "evidence": [],
      "rationale": "This is a personal account and no corporate structure appears anywhere in the corpus. Ownership analysis has no subject here."},
     {"id": f"{S}-C06", "proposition": "The recorded income profile is pension receipts only.",
      "status": "supported", "evidence": [ev("ALT-8001", "ALT-8001-P01", "system_observation")],
      "rationale": "Recorded in the alert."},
    ]
    f[f"answers/{S}.yaml"] = {
        "scenario_ref": S, "synthetic": dict(M), "claims": claims,
        "not_provided_inventory": [
            "the source of the three later credits",
            "the identity or relationship of the second remitter",
            "any second property, asset sale or loan",
            "any prior alert on this account",
            "the customer's wider financial position"],
        "evaluation_target": {
            "disposition_expected": "escalate: credits exceed the documented source by 260,000 and the explanation is contradicted by the document relied on",
            "basis": "C01 supported for the first credit only. C02 contradicted, C04 not provided. POL-8001 directs escalation where credits materially exceed a documented source.",
            "epistemic_scope": "A reviewer could seek the conveyancer's ledger before escalating. Treating the completion statement as partial support for all four credits would not be supported."}}
    f["scenarios/AML-S08.yaml"] = {
        "scenario_id": S, "schema_version": "1", "scenario_version": "1",
        "corpus_version": g.CORPUS_VERSION, "difficulty_tier": 3,
        "coverage_labels": ["citation", "absence", "qualifier", "numerical",
                             "disposition"],
        "fixture_ids": ["CUST-8001", "TXN-8001", "ALT-8001", "DOC-8001", "CN-8001",
                         "POL-8001"],
        "policy_context": {"jurisdiction": "United States (synthetic institution)",
                            "policy_assumptions": ["see POL-8001"],
                            "decision_rules": ["see POL-8001"]},
        "synthetic": dict(M)}
    return f


# ---------------------------------------------------------------- S09
def build_s09(g) -> dict:
    """No transactions, no screening. The whole question is what a
    certificate attests and what a reader might wrongly read into it.
    Tier 2, close."""
    S = "AML-S09"
    M, fx, ev = _mk(g, S)
    taken: set = set()
    co = g.distinct_name("company", "S09-C", taken) + " Foods Ltd"
    parent = g.distinct_name("company", "S09-P", taken) + " Group"
    director = (f"{g.distinct_name('given','S09-D',taken)} "
                f"{g.distinct_name('person','S09-D',taken)}")

    f = {}
    f["fixtures/customers/CUST-9001.yaml"] = fx("CUST-9001", "customer", {"record": {
        "legal_name": co, "customer_since": "2022-07-11",
        "business_description": "food importer",
        "domicile": "domestic", "as_of": g.REFERENCE_DATE}})
    f["fixtures/alerts/ALT-9001.yaml"] = fx("ALT-9001", "alert", {
        "record": {"alert_date": "2026-06-04", "rule_ref": "periodic review",
                   "subject_ref": "CUST-9001"},
        "passages": [
            {"passage_id": "ALT-9001-P01", "locator": {"type": "narrative", "index": 1},
             "text": ("Scheduled documentation review. The relationship file was "
                      "flagged for a missing certified beneficial ownership "
                      "confirmation. No transaction concern is recorded.")}]})
    f["fixtures/documents/DOC-9001.yaml"] = fx("DOC-9001", "document", {
        "title": "Certificate of good standing", "doc_date": "2026-05-18",
        "passages": [
            {"passage_id": "DOC-9001-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"The registrar certifies that {co} is duly incorporated, has "
                      "filed all returns due, and is not in the course of being "
                      "struck off as at the date of this certificate.")},
            {"passage_id": "DOC-9001-P02", "locator": {"type": "paragraph", "index": 2},
             "text": ("This certificate speaks only to the matters stated. It is "
                      "not a statement about the company's members, officers, "
                      "trading activity or financial position.")}]})
    f["fixtures/documents/DOC-9002.yaml"] = fx("DOC-9002", "document", {
        "title": "Group structure chart, customer provided", "doc_date": "2024-02-09",
        "passages": [
            {"passage_id": "DOC-9002-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"Chart supplied by the customer showing {co} as a wholly "
                      f"owned subsidiary of {parent}, with {director} as sole "
                      "director of both. The chart is unsigned and undated except "
                      "for the file stamp.")}]})
    f["fixtures/case-notes/CN-9001.yaml"] = fx("CN-9001", "case_note", {
        "record": {"note_date": "2026-06-27", "author_role": "analyst"},
        "passages": [
            {"passage_id": "CN-9001-P01", "locator": {"type": "note", "index": 1},
             "text": ("Certificate of good standing obtained and filed. The "
                      "certified beneficial ownership confirmation remains "
                      "outstanding and has been requested with a 60 day deadline "
                      "under the standard documentation cycle. No transaction "
                      "review is in scope for this review type.")}]})
    f["fixtures/policy/POL-9001.yaml"] = fx("POL-9001", "policy_context", {
        "record": {"jurisdiction": "United States (synthetic institution)",
                   "policy_assumptions": [
                       "a documentation gap inside its remediation window is "
                       "managed, not adverse"],
                   "decision_rules": [
                       "close a documentation review where the outstanding item is "
                       "within its deadline and no other concern is recorded",
                       "do not treat a registry certificate as evidence of "
                       "ownership"]},
        "passages": [
            {"passage_id": "POL-9001-P01", "locator": {"type": "clause", "index": 1},
             "text": ("An outstanding document within its deadline is a tracked "
                      "item. It is not a finding.")}]})

    claims = [
     {"id": f"{S}-C01", "proposition": "The company is duly incorporated and has filed all returns due.",
      "status": "supported", "evidence": [ev("DOC-9001", "DOC-9001-P01", "documented")],
      "rationale": "Certified by the registrar."},
     {"id": f"{S}-C02", "proposition": "The certificate of good standing evidences the company's beneficial ownership.",
      "status": "contradicted", "evidence": [ev("DOC-9001", "DOC-9001-P02", "documented")],
      "rationale": "The certificate states that it speaks only to the matters stated and says nothing about members. Evidence sufficiency: the document is genuine and cited correctly, and it does not support the proposition."},
     {"id": f"{S}-C03", "proposition": "The company is a wholly owned subsidiary of the group.",
      "status": "indeterminate", "evidence": [ev("DOC-9002", "DOC-9002-P01", "stated_by_customer")],
      "rationale": "The only support is an unsigned customer supplied chart from 2024. It may well be accurate; it is not verified, and the certified confirmation is outstanding."},
     {"id": f"{S}-C04", "proposition": "The certified beneficial ownership confirmation is overdue.",
      "status": "contradicted", "evidence": [ev("CN-9001", "CN-9001-P01", "analyst_observation"),
                                             ev("POL-9001", "POL-9001-P01", "documented")],
      "rationale": "It was requested with a 60 day deadline that has not expired. Within its window it is a tracked item."},
     {"id": f"{S}-C05", "proposition": "Transaction activity was reviewed as part of this review.",
      "status": "contradicted", "evidence": [ev("CN-9001", "CN-9001-P01", "analyst_observation")],
      "rationale": "The note records that transaction review is out of scope for this review type, and no transaction fixture exists."},
     {"id": f"{S}-C06", "proposition": "The company's current directors are recorded in the corpus.",
      "status": "not_provided", "evidence": [],
      "rationale": "The 2024 chart names a director; nothing evidences the present position."},
    ]
    f[f"answers/{S}.yaml"] = {
        "scenario_ref": S, "synthetic": dict(M), "claims": claims,
        "not_provided_inventory": [
            "the company's current directors",
            "any transaction activity",
            "the group's ownership above the parent",
            "any adverse information about the company or the group",
            "the reason the confirmation has not yet been returned"],
        "evaluation_target": {
            "disposition_expected": "close the documentation review: the outstanding item is within its deadline and no other concern is recorded",
            "basis": "C01 supported, C04 contradicted, C05 contradicted. POL-9001 directs closure where the outstanding item is within its window.",
            "epistemic_scope": "A reviewer could hold the review open until the confirmation returns. Recording the certificate as ownership evidence would not be supported."}}
    f["scenarios/AML-S09.yaml"] = {
        "scenario_id": S, "schema_version": "1", "scenario_version": "1",
        "corpus_version": g.CORPUS_VERSION, "difficulty_tier": 2,
        "coverage_labels": ["evidence_sufficiency", "qualifier", "negative_control",
                             "absence", "citation", "disposition"],
        "fixture_ids": ["CUST-9001", "ALT-9001", "DOC-9001", "DOC-9002", "CN-9001",
                         "POL-9001"],
        "policy_context": {"jurisdiction": "United States (synthetic institution)",
                            "policy_assumptions": ["see POL-9001"],
                            "decision_rules": ["see POL-9001"]},
        "synthetic": dict(M)}
    return f


# ---------------------------------------------------------------- S10
def build_s10(g) -> dict:
    """Three versions of one mandate, where the newest is not the one that
    governed the period under review. Temporal reasoning without recency
    heuristics. Tier 4, escalate."""
    S = "AML-S10"
    M, fx, ev = _mk(g, S)
    taken: set = set()
    co = g.distinct_name("company", "S10-C", taken) + " Freight Ltd"
    agent = (f"{g.distinct_name('given','S10-A',taken)} "
             f"{g.distinct_name('person','S10-A',taken)}")
    dest = g.distinct_name("jurisdiction", "S10-J", taken)

    f = {}
    f["fixtures/customers/CUST-1010.yaml"] = fx("CUST-1010", "customer", {"record": {
        "legal_name": co, "customer_since": "2018-03-19",
        "business_description": "road freight operator",
        "domicile": "domestic", "as_of": g.REFERENCE_DATE}})
    pays = [("M01", "2026-02-17", 64000), ("M02", "2026-03-17", 64000),
            ("M03", "2026-04-16", 64000), ("M04", "2026-05-18", 64000)]
    f["fixtures/transactions/TXN-1010.yaml"] = fx("TXN-1010", "transaction_set", {
        "record": {"account_ref": "CUST-1010", "currency": "USD"},
        "transactions": [{"txn_id": f"TXN-1010-{i}", "value_date": d,
                          "direction": "outbound", "amount": a,
                          "counterparty_name": agent, "channel": "international wire",
                          "narrative": f"agency fees {dest}"} for i, d, a in pays]})
    f["fixtures/alerts/ALT-1010.yaml"] = fx("ALT-1010", "alert", {
        "record": {"alert_date": "2026-06-05", "rule_ref": "AGT-02",
                   "subject_ref": "CUST-1010"},
        "passages": [
            {"passage_id": "ALT-1010-P01", "locator": {"type": "narrative", "index": 1},
             "text": ("Scenario AGT-02. Four monthly payments of 64,000 to an "
                      "individual agent overseas, February to May 2026. Standing "
                      "mandate on file.")}]})
    # three versions of one document
    f["fixtures/documents/DOC-1011.yaml"] = fx("DOC-1011", "document", {
        "title": "Agency mandate, version 1", "doc_date": "2023-01-09",
        "passages": [
            {"passage_id": "DOC-1011-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"{co} appoints {agent} as clearing agent in {dest}. Monthly "
                      "retainer 22,000, payable in arrears. Term three years.")}]})
    f["fixtures/documents/DOC-1012.yaml"] = fx("DOC-1012", "document", {
        "title": "Agency mandate, amendment 1", "doc_date": "2024-06-30",
        "passages": [
            {"passage_id": "DOC-1012-P01", "locator": {"type": "paragraph", "index": 1},
             "text": ("The retainer under the mandate of 9 January 2023 is varied "
                      "to 26,500 monthly with effect from 1 July 2024. All other "
                      "terms are unchanged.")}]})
    f["fixtures/documents/DOC-1013.yaml"] = fx("DOC-1013", "document", {
        "title": "Agency mandate, version 2", "doc_date": "2026-06-08",
        "passages": [
            {"passage_id": "DOC-1013-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"{co} and {agent} enter a replacement mandate. Monthly "
                      "retainer 64,000 reflecting expanded scope, with effect from "
                      "1 June 2026. This document replaces the mandate of 9 January "
                      "2023 as amended.")}]})
    f["fixtures/case-notes/CN-1010.yaml"] = fx("CN-1010", "case_note", {
        "record": {"note_date": "2026-06-30", "author_role": "analyst"},
        "passages": [
            {"passage_id": "CN-1010-P01", "locator": {"type": "note", "index": 1},
             "text": ("Three mandate documents are on file. The replacement was "
                      "signed on 8 June 2026 and takes effect from 1 June 2026. The "
                      "payments under review fall in February to May 2026.")}]})
    f["fixtures/policy/POL-1010.yaml"] = fx("POL-1010", "policy_context", {
        "record": {"jurisdiction": "United States (synthetic institution)",
                   "policy_assumptions": [
                       "a payment is assessed against the terms in force on its "
                       "value date"],
                   "decision_rules": [
                       "escalate where payments exceed the mandate in force for the "
                       "period and the excess is unexplained",
                       "a later instrument does not evidence earlier payments "
                       "unless it says so"]},
        "passages": [
            {"passage_id": "POL-1010-P01", "locator": {"type": "clause", "index": 1},
             "text": ("Terms are applied as at the value date of the payment, not "
                      "as at the date of review.")}]})

    claims = [
     {"id": f"{S}-C01", "proposition": "The mandate in force from February to May 2026 provided for a monthly retainer of 26,500.",
      "status": "supported", "evidence": [ev("DOC-1011", "DOC-1011-P01", "documented"),
                                          ev("DOC-1012", "DOC-1012-P01", "documented")],
      "rationale": "The 2023 mandate as varied by the 2024 amendment, which took effect from 1 July 2024 and was not replaced until 1 June 2026."},
     {"id": f"{S}-C02", "proposition": "The payments of 64,000 per month are within the mandate in force when they were made.",
      "status": "contradicted", "evidence": [ev("TXN-1010", "TXN-1010-M01", "documented"),
                                             ev("DOC-1012", "DOC-1012-P01", "documented"),
                                             ev("DOC-1013", "DOC-1013-P01", "documented")],
      "rationale": "The replacement mandate takes effect from 1 June 2026 and each payment predates it. Reading the newest version as governing the earlier period is the error this scenario tests."},
     {"id": f"{S}-C03", "proposition": "The excess over the mandate in force is 37,500 per month, 150,000 across the four payments.",
      "status": "supported", "evidence": [ev("TXN-1010", "TXN-1010-M01", "derived"),
                                          ev("DOC-1012", "DOC-1012-P01", "derived")],
      "rationale": "64,000 paid against 26,500 due gives 37,500 monthly, and four payments give 150,000."},
     {"id": f"{S}-C04", "proposition": "The replacement mandate is retrospective.",
      "status": "contradicted", "evidence": [ev("DOC-1013", "DOC-1013-P01", "documented")],
      "rationale": "It states effect from 1 June 2026 and says nothing about earlier periods."},
     {"id": f"{S}-C05", "proposition": "The expanded scope described in the replacement mandate was already being performed during the period under review.",
      "status": "not_provided", "evidence": [],
      "rationale": "A plausible explanation for the higher payments that the corpus neither supports nor excludes."},
     {"id": f"{S}-C06", "proposition": "The 2024 amendment remained in force until 1 June 2026.",
      "status": "supported", "evidence": [ev("DOC-1012", "DOC-1012-P01", "documented"),
                                          ev("DOC-1013", "DOC-1013-P01", "documented")],
      "rationale": "The amendment varied the 2023 mandate and the replacement is the next instrument, effective 1 June 2026."},
    ]
    f[f"answers/{S}.yaml"] = {
        "scenario_ref": S, "synthetic": dict(M), "claims": claims,
        "not_provided_inventory": [
            "when the expanded scope actually began",
            "any invoice or service record from the agent",
            "any board approval of the higher payments",
            "the agent's relationship to the customer beyond the mandate",
            "activity before February 2026"],
        "evaluation_target": {
            "disposition_expected": "escalate: payments exceeded the mandate in force by 150,000 across the period, and the replacement instrument does not cover it",
            "basis": "C01 and C03 supported, C02 and C04 contradicted, C05 not provided. POL-1010 applies terms as at value date.",
            "epistemic_scope": "A reviewer could seek the agent's invoices before escalating. Treating the June replacement as authority for February to May payments would not be supported."}}
    f["scenarios/AML-S10.yaml"] = {
        "scenario_id": S, "schema_version": "1", "scenario_version": "1",
        "corpus_version": g.CORPUS_VERSION, "difficulty_tier": 4,
        "coverage_labels": ["temporal_update", "numerical", "citation",
                             "claim_decomposition", "absence", "disposition"],
        "fixture_ids": ["CUST-1010", "TXN-1010", "ALT-1010", "DOC-1011", "DOC-1012",
                         "DOC-1013", "CN-1010", "POL-1010"],
        "policy_context": {"jurisdiction": "United States (synthetic institution)",
                            "policy_assumptions": ["see POL-1010"],
                            "decision_rules": ["see POL-1010"]},
        "synthetic": dict(M)}
    return f


def build_cases_b3(g) -> dict:
    """VC-08 to VC-10, one per scenario, each a single-locus mutation."""
    M = {"marker": g.MARKER, "corpus_version": g.CORPUS_VERSION}
    f = {}
    specs = [
      dict(id="VC-08", scen="AML-S08", ctrl="adversarial", fm="unsupported_claim",
           task="State whether the credits to this account are accounted for by a documented source.",
           vis=["CUST-8001","TXN-8001","ALT-8001","DOC-8001","CN-8001","POL-8001"],
           targets=["AML-S08-C01","AML-S08-C02"],
           req=["states that only the April credit is documented",
                "notes that the completion statement records a single payment"],
           forb=["all credits relate to the property sale","fully explained"],
           var=["only the first credit","260,000 unaccounted"],
           unc="must not assert an illicit source either",
           disc=("A failing response accepts the customer's account that all four "
                 "credits relate to one sale, which the completion statement "
                 "contradicts. The corruption extends the documented explanation "
                 "to the later credits while leaving the citation intact."),
           mt="scope of the documented explanation",
           good=("Only the April credit of 140,000 is documented. The completion "
                 "statement [DOC-8001-P01] records a single payment from the "
                 "buyer's conveyancer, so the three later credits of 260,000 are "
                 "unaccounted for."),
           bad=("Only the April credit of 140,000 is documented. The completion "
                "statement [DOC-8001-P01] records four scheduled payments from the "
                "buyer's conveyancer, so the three later credits of 260,000 are "
                "unaccounted for.")),
      dict(id="VC-09", scen="AML-S09", ctrl="negative", fm="evidence_insufficiency",
           task="State what the certificate of good standing establishes about this customer.",
           vis=["CUST-9001","ALT-9001","DOC-9001","DOC-9002","CN-9001","POL-9001"],
           targets=["AML-S09-C01","AML-S09-C02"],
           req=["states that the certificate covers incorporation and filings only",
                "states that it does not evidence ownership"],
           forb=["confirms the ownership","verifies the beneficial owners"],
           var=["says nothing about members","incorporation status only"],
           unc="may note that the certified confirmation is still outstanding",
           disc=("A failing response reads a genuine registry certificate as "
                 "ownership evidence. The corruption keeps the citation and "
                 "extends what the document is said to establish."),
           mt="scope of what the certificate attests",
           good=("The certificate establishes that the company is incorporated and "
                 "has filed its returns [DOC-9001-P01]. It states that it speaks "
                 "only to those matters and says nothing about the members."),
           bad=("The certificate establishes that the company is incorporated and "
                "has filed its returns [DOC-9001-P01]. It states that it speaks "
                "only to those matters and also confirms the members.")),
      dict(id="VC-10", scen="AML-S10", ctrl="adversarial", fm="numerical_error",
           task="State whether the February to May payments were within the agency mandate.",
           vis=["CUST-1010","TXN-1010","ALT-1010","DOC-1011","DOC-1012","DOC-1013",
                "CN-1010","POL-1010"],
           targets=["AML-S10-C01","AML-S10-C02","AML-S10-C03"],
           req=["identifies 26,500 as the retainer in force for the period",
                "quantifies the excess as 150,000"],
           forb=["within the mandate","64,000 was the agreed retainer"],
           var=["exceeded the mandate","37,500 per month above the retainer"],
           unc="must not assert that the expanded scope was already performed",
           disc=("A failing response applies the newest mandate to the earlier "
                 "period, which is the recency error the scenario is built on. The "
                 "corruption cites the correct amendment and states the wrong "
                 "governing figure."),
           mt="the retainer treated as in force for the period",
           good=("The payments exceeded the mandate. The retainer in force from "
                 "July 2024 was 26,500 monthly [DOC-1012-P01], and the replacement "
                 "at 64,000 took effect only from 1 June 2026, so the four payments "
                 "exceeded the mandate by 150,000."),
           bad=("The payments exceeded the mandate. The retainer in force from "
                "July 2024 was 22,000 monthly [DOC-1012-P01], and the replacement "
                "at 64,000 took effect only from 1 June 2026, so the four payments "
                "exceeded the mandate by 150,000.")),
    ]
    cases = []
    for s in specs:
        cases.append({
            "id": s["id"], "scenario_ref": s["scen"], "control_type": s["ctrl"],
            "task": s["task"], "visibility_fixtures": s["vis"],
            "failure_mode": s["fm"],
            "oracle": {"type": "structured", "target_claims": s["targets"],
                       "required_elements": s["req"], "forbidden_elements": s["forb"],
                       "allowed_variants": s["var"],
                       "uncertainty_requirement": s["unc"],
                       "evidence_requirement": "passage level citation",
                       "human_review_protocol": None},
            "severity": "high", "discrimination_rationale": s["disc"],
            "corruption_ref": f"corruptions/{s['id']}.yaml",
            "mutation_target": s["mt"]})
        f[f"validation-cases/corruptions/{s['id']}.yaml"] = {
            "case_ref": s["id"], "mutation_class": MUTATION_CLASS[s["id"]],
            "synthetic": dict(M),
            "known_good_answer": s["good"], "corrupted_answer": s["bad"],
            "mutation_target": s["mt"],
            "defect_description": ("Exactly one semantic defect, plausible in "
                                   "isolation: " + s["mt"] + " is altered while "
                                   "the surrounding answer stays correct.")}
    f["validation-cases/cases-b3.yaml"] = {"synthetic": dict(M), "cases": cases}
    return f


BUILDERS = [build_s08, build_s09, build_s10, build_cases_b3]
