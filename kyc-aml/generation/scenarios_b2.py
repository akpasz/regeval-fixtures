# SPDX-License-Identifier: Apache-2.0
"""Stage 3 batch 2: AML-S05, AML-S06, AML-S07.

Two design constraints drive this batch.

1. Coverage: qualifier and temporal_update were single-point-of-proof after
   batch 1; ownership needed a case with no controller to find; numerical
   needed a construction with no threshold proximity (DD-018).

2. Anti-shortcut: the batch 1 audit reported FAIL on difficulty_tier, because
   one scenario per tier made tier a perfect predictor of disposition. This
   batch breaks the mapping deliberately:

       tier 2 -> escalate (S06)      previously tier 2 -> close
       tier 3 -> close    (S05)      previously tier 3 -> escalate
       tier 4 -> close    (S07)      previously tier 4 -> continue

Fixture topology also varies: S05 carries a prior closed case, S06 has no
customer contact at all, S07 has no transactions.
"""
from __future__ import annotations


def _mk(g, scenario_id):
    M = {"marker": g.MARKER, "corpus_version": g.CORPUS_VERSION}
    def fx(fid, ftype, extra):
        return {"fixture_id": fid, "fixture_type": ftype,
                "scenario_ref": scenario_id, "synthetic": dict(M), **extra}
    def ev(fid, pid, etype):
        return {"fixture_id": fid, "passage_id": pid, "evidence_type": etype}
    return M, fx, ev


# ---------------------------------------------------------------- S05
def build_s05(g) -> dict:
    """Qualifier preservation with an observable prior closed case. The prior
    closure rested on an unverified customer statement. New documentation
    verifies the current transfers but not the earlier ones. Tier 3, close."""
    S = "AML-S05"
    M, fx, ev = _mk(g, S)
    taken: set = set()
    co = g.distinct_name("company", "S05-C", taken) + " Systems Ltd"
    holder = (f"{g.distinct_name('given','S05-H',taken)} "
              f"{g.distinct_name('person','S05-H',taken)}")

    f = {}
    f["fixtures/customers/CUST-5001.yaml"] = fx("CUST-5001", "customer", {"record": {
        "legal_name": co, "customer_since": "2019-09-30",
        "business_description": "industrial control software",
        "domicile": "domestic", "as_of": g.REFERENCE_DATE}})
    f["fixtures/transactions/TXN-5001.yaml"] = fx("TXN-5001", "transaction_set", {
        "record": {"account_ref": "CUST-5001", "currency": "USD"},
        "transactions": [
            {"txn_id": "TXN-5001-A01", "value_date": "2026-05-19", "direction": "inbound",
             "amount": 300000, "counterparty_name": holder, "channel": "domestic wire",
             "narrative": "no reference"},
            {"txn_id": "TXN-5001-A02", "value_date": "2026-06-09", "direction": "inbound",
             "amount": 175000, "counterparty_name": holder, "channel": "domestic wire",
             "narrative": "no reference"}]})
    f["fixtures/alerts/ALT-5001.yaml"] = fx("ALT-5001", "alert", {
        "record": {"alert_date": "2026-06-11", "rule_ref": "IND-07",
                   "subject_ref": "CUST-5001"},
        "passages": [
            {"passage_id": "ALT-5001-P01", "locator": {"type": "narrative", "index": 1},
             "text": ("Scenario IND-07. Two inbound wires from an individual "
                      "totalling 475,000 over 22 days. Prior alert on comparable "
                      "activity closed 2025-04-02.")}]})
    # the prior case, observable but not authoritative
    f["fixtures/case-notes/CN-5001.yaml"] = fx("CN-5001", "case_note", {
        "record": {"note_date": "2025-04-02", "author_role": "analyst"},
        "passages": [
            {"passage_id": "CN-5001-P01", "locator": {"type": "note", "index": 1},
             "text": ("Prior case closure, alert of 2025-03-06. Two inbound wires "
                      "from the same individual totalling 260,000 in February and "
                      "March 2025. The customer stated that the funds were "
                      "shareholder loans to fund a product launch and undertook to "
                      "provide the loan documentation. The documentation was not "
                      "received. Case closed on the customer's explanation. The "
                      "explanation was not independently verified.")}]})
    f["fixtures/case-notes/CN-5002.yaml"] = fx("CN-5002", "case_note", {
        "record": {"note_date": "2026-06-24", "author_role": "analyst"},
        "passages": [
            {"passage_id": "CN-5002-P01", "locator": {"type": "note", "index": 1},
             "text": ("Loan agreement and board minute obtained for the May and "
                      "June transfers. Both are executed and dated before the "
                      "transfers. No documentation was located for the 2025 "
                      "transfers and the customer has not been asked again.")}]})
    f["fixtures/documents/DOC-5001.yaml"] = fx("DOC-5001", "document", {
        "title": "Shareholder loan agreement", "doc_date": "2026-05-11",
        "passages": [
            {"passage_id": "DOC-5001-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"{holder} agrees to advance up to 500,000 to {co} by way of "
                      "unsecured shareholder loan, drawable in tranches, repayable "
                      "on demand after 2028. Executed 11 May 2026.")}]})
    f["fixtures/documents/DOC-5002.yaml"] = fx("DOC-5002", "document", {
        "title": "Board minute", "doc_date": "2026-05-14",
        "passages": [
            {"passage_id": "DOC-5002-P01", "locator": {"type": "paragraph", "index": 1},
             "text": ("The board approved acceptance of the shareholder loan "
                      "facility executed 11 May 2026 and authorised drawdown as "
                      "required for the production release.")}]})
    f["fixtures/documents/DOC-5003.yaml"] = fx("DOC-5003", "document", {
        "title": "Share register extract", "doc_date": "2026-03-02",
        "passages": [
            {"passage_id": "DOC-5003-P01", "locator": {"type": "paragraph", "index": 1},
             "text": f"Sole registered member: {holder}, 100 percent."}]})
    f["fixtures/policy/POL-5001.yaml"] = fx("POL-5001", "policy_context", {
        "record": {"jurisdiction": "United States (synthetic institution)",
                   "policy_assumptions": [
                       "a prior closure is case history, not a determination that "
                       "binds a later review"],
                   "decision_rules": [
                       "close where the activity under review is documented",
                       "record, but do not re-open on, an earlier explanation that "
                       "was never verified"]},
        "passages": [
            {"passage_id": "POL-5001-P01", "locator": {"type": "clause", "index": 1},
             "text": ("An earlier closure reached on an unverified explanation does "
                      "not convert that explanation into an established fact.")}]})

    claims = [
     {"id": f"{S}-C01", "proposition": "The May and June 2026 transfers are drawdowns under an executed shareholder loan facility.",
      "status": "supported", "evidence": [ev("DOC-5001", "DOC-5001-P01", "documented"),
                                          ev("DOC-5002", "DOC-5002-P01", "documented")],
      "rationale": "The facility was executed 11 May and approved 14 May, both before the transfers of 19 May and 9 June."},
     {"id": f"{S}-C02", "proposition": "The customer stated that the 2025 transfers were shareholder loans.",
      "status": "supported", "evidence": [ev("CN-5001", "CN-5001-P01", "stated_by_customer")],
      "rationale": "The statement was made and is recorded. Its evidence type marks it as a customer assertion."},
     {"id": f"{S}-C03", "proposition": "The 2025 transfers were shareholder loans.",
      "status": "indeterminate", "evidence": [ev("CN-5001", "CN-5001-P01", "stated_by_customer")],
      "rationale": "The only support is the customer's own unverified statement, and the promised documentation never arrived. The 2026 facility postdates those transfers and does not cover them. Distinguishing this from C02 is the qualifier test: the statement was made is a fact, what it asserts is not."},
     {"id": f"{S}-C04", "proposition": "The prior case closure established that the 2025 transfers were legitimate.",
      "status": "contradicted", "evidence": [ev("CN-5001", "CN-5001-P01", "analyst_observation"),
                                             ev("POL-5001", "POL-5001-P01", "documented")],
      "rationale": "The closure note records that the explanation was not verified, and the policy states that an unverified explanation does not become established by closure."},
     {"id": f"{S}-C05", "proposition": "The 2026 facility covers the 2025 transfers.",
      "status": "contradicted", "evidence": [ev("DOC-5001", "DOC-5001-P01", "documented")],
      "rationale": "The agreement was executed in May 2026 and is not retrospective."},
     {"id": f"{S}-C06", "proposition": "The source of the shareholder's own funds is documented.",
      "status": "not_provided", "evidence": [],
      "rationale": "Nothing in the corpus addresses where the individual's funds came from."},
    ]
    f[f"answers/{S}.yaml"] = {
        "scenario_ref": S, "synthetic": dict(M), "claims": claims,
        "not_provided_inventory": [
            "the source of the shareholder's funds",
            "any loan documentation for the 2025 transfers",
            "any repayment or interest activity on either facility",
            "any other shareholder or director of the company",
            "the company's financial position"],
        "evaluation_target": {
            "disposition_expected": "close: the transfers under review are documented by a facility executed before them",
            "basis": "C01 supported. C03 remains indeterminate and is recorded as such rather than resolved by the prior closure (C04). POL-5001 directs closure of the current activity and no re-opening of the earlier matter.",
            "epistemic_scope": "A reviewer could reasonably request the 2025 documentation while closing the current alert. Treating the prior closure as having settled the 2025 position would not be supported."}}
    f["scenarios/AML-S05.yaml"] = {
        "scenario_id": S, "schema_version": "1", "scenario_version": "1",
        "corpus_version": g.CORPUS_VERSION, "difficulty_tier": 3,
        "coverage_labels": ["qualifier", "temporal_update", "claim_decomposition",
                             "absence", "citation", "disposition"],
        "fixture_ids": ["CUST-5001", "TXN-5001", "ALT-5001", "CN-5001", "CN-5002",
                         "DOC-5001", "DOC-5002", "DOC-5003", "POL-5001"],
        "policy_context": {"jurisdiction": "United States (synthetic institution)",
                            "policy_assumptions": ["see POL-5001"],
                            "decision_rules": ["see POL-5001"]},
        "synthetic": dict(M)}
    return f


# ---------------------------------------------------------------- S06
def build_s06(g) -> dict:
    """Temporal worsening, and deliberately not dispositive. Later documents
    reconcile most of the activity and reveal a duplication in the rest. The
    duplication has an innocent reading that the corpus does not exclude.
    Tier 2, escalate. No customer contact anywhere in the file."""
    S = "AML-S06"
    M, fx, ev = _mk(g, S)
    taken: set = set()
    co = g.distinct_name("company", "S06-C", taken) + " Textiles Ltd"
    supplier = g.distinct_name("company", "S06-S", taken) + " Mills"

    f = {}
    f["fixtures/customers/CUST-6001.yaml"] = fx("CUST-6001", "customer", {"record": {
        "legal_name": co, "customer_since": "2015-01-22",
        "business_description": "apparel wholesale",
        "domicile": "domestic", "as_of": g.REFERENCE_DATE}})
    pays = [("P01", "2026-03-10", 88400), ("P02", "2026-03-24", 61200),
            ("P03", "2026-04-07", 94750), ("P04", "2026-04-21", 72300),
            ("P05", "2026-05-05", 88400), ("P06", "2026-05-19", 66900),
            ("P07", "2026-06-02", 79500), ("P08", "2026-06-16", 94750)]
    f["fixtures/transactions/TXN-6001.yaml"] = fx("TXN-6001", "transaction_set", {
        "record": {"account_ref": "CUST-6001", "currency": "USD"},
        "transactions": [{"txn_id": f"TXN-6001-{i}", "value_date": d,
                          "direction": "outbound", "amount": a,
                          "counterparty_name": supplier,
                          "channel": "international wire",
                          "narrative": "trade settlement"} for i, d, a in pays]})
    f["fixtures/alerts/ALT-6001.yaml"] = fx("ALT-6001", "alert", {
        "record": {"alert_date": "2026-06-18", "rule_ref": "TRD-03",
                   "subject_ref": "CUST-6001"},
        "passages": [
            {"passage_id": "ALT-6001-P01", "locator": {"type": "narrative", "index": 1},
             "text": ("Scenario TRD-03. Eight outbound trade payments to a single "
                      "overseas supplier totalling 646,200 over 14 weeks. Volume "
                      "within the profile recorded at onboarding.")}]})
    f["fixtures/case-notes/CN-6001.yaml"] = fx("CN-6001", "case_note", {
        "record": {"note_date": "2026-06-23", "author_role": "analyst"},
        "passages": [
            {"passage_id": "CN-6001-P01", "locator": {"type": "note", "index": 1},
             "text": ("Payment volume and supplier are consistent with the trade "
                      "profile on file. Invoice file requested from the trade "
                      "finance unit rather than the customer.")}]})
    f["fixtures/case-notes/CN-6002.yaml"] = fx("CN-6002", "case_note", {
        "record": {"note_date": "2026-06-29", "author_role": "analyst"},
        "passages": [
            {"passage_id": "CN-6002-P01", "locator": {"type": "note", "index": 1},
             "text": ("Invoice file received 26 June. Six payments match six "
                      "invoices. Payments P05 and P08 carry the same amounts as P01 "
                      "and P03 and the invoice file contains no seventh or eighth "
                      "invoice. Invoices INV-4410 and INV-4416 both reference "
                      "shipment SHP-9902.")}]})
    f["fixtures/documents/DOC-6001.yaml"] = fx("DOC-6001", "document", {
        "title": "Invoice file, March to June 2026", "doc_date": "2026-06-26",
        "passages": [
            {"passage_id": "DOC-6001-P01", "locator": {"type": "table", "index": 1},
             "text": ("INV-4410 88,400 shipment SHP-9902; INV-4412 61,200 shipment "
                      "SHP-9915; INV-4416 94,750 shipment SHP-9902; INV-4421 72,300 "
                      "shipment SHP-9938; INV-4429 66,900 shipment SHP-9951; "
                      "INV-4437 79,500 shipment SHP-9967.")},
            {"passage_id": "DOC-6001-P02", "locator": {"type": "paragraph", "index": 2},
             "text": ("Six invoices are held for the period. The file is the copy "
                      "provided to the trade finance unit at the time of each "
                      "payment instruction.")}]})
    f["fixtures/documents/DOC-6002.yaml"] = fx("DOC-6002", "document", {
        "title": "Shipping schedule extract", "doc_date": "2026-06-26",
        "passages": [
            {"passage_id": "DOC-6002-P01", "locator": {"type": "table", "index": 1},
             "text": ("SHP-9902 departed 2026-02-27, one container, mixed woven "
                      "goods. SHP-9915, SHP-9938, SHP-9951, SHP-9967 each one "
                      "container. No second consignment is recorded against "
                      "SHP-9902.")}]})
    f["fixtures/policy/POL-6001.yaml"] = fx("POL-6001", "policy_context", {
        "record": {"jurisdiction": "United States (synthetic institution)",
                   "policy_assumptions": [
                       "trade payments are expected to correspond to distinct "
                       "underlying shipments"],
                   "decision_rules": [
                       "escalate where payments exceed the documented underlying "
                       "trade and the excess is not accounted for",
                       "a clerical explanation must be evidenced, not assumed"]},
        "passages": [
            {"passage_id": "POL-6001-P01", "locator": {"type": "clause", "index": 1},
             "text": ("Where payments exceed documented trade, escalation does not "
                      "require a finding of intent.")}]})

    claims = [
     {"id": f"{S}-C01", "proposition": "Eight payments were made to the supplier over the period.",
      "status": "supported", "evidence": [ev("TXN-6001", "TXN-6001-P01", "documented")],
      "rationale": "Observable from the transaction set."},
     {"id": f"{S}-C02", "proposition": "Six of the eight payments correspond to invoices in the file.",
      "status": "supported", "evidence": [ev("DOC-6001", "DOC-6001-P01", "documented")],
      "rationale": "Six invoices, six matching amounts."},
     {"id": f"{S}-C03", "proposition": "Payments P05 and P08, totalling 183,150, correspond to documented underlying trade.",
      "status": "contradicted", "evidence": [ev("DOC-6001", "DOC-6001-P02", "documented"),
                                             ev("DOC-6002", "DOC-6002-P01", "documented")],
      "rationale": "The invoice file holds six invoices for eight payments, and the shipping schedule records no second consignment against the duplicated shipment reference. The later evidence makes the position worse than the initial review suggested, and it does so because it supplies the invoice and shipping records, not because it arrived later."},
     {"id": f"{S}-C04", "proposition": "Two invoices reference the same shipment.",
      "status": "supported", "evidence": [ev("DOC-6001", "DOC-6001-P01", "documented")],
      "rationale": "INV-4410 and INV-4416 both cite SHP-9902."},
     {"id": f"{S}-C05", "proposition": "The duplication is a clerical error by the supplier.",
      "status": "not_provided", "evidence": [],
      "rationale": "A plausible innocent reading that the corpus neither supports nor excludes. It is not available as a finding, and the policy requires a clerical explanation to be evidenced."},
     {"id": f"{S}-C06", "proposition": "The payments were made with intent to move value without underlying trade.",
      "status": "not_provided", "evidence": [],
      "rationale": "Intent is not evidenced. Escalation under POL-6001 does not require it."},
     {"id": f"{S}-C07", "proposition": "Payment volume is inconsistent with the customer's recorded trade profile.",
      "status": "contradicted", "evidence": [ev("ALT-6001", "ALT-6001-P01", "system_observation")],
      "rationale": "The alert records volume as within profile. The concern is documentation coverage, not volume."},
    ]
    f[f"answers/{S}.yaml"] = {
        "scenario_ref": S, "synthetic": dict(M), "claims": claims,
        "not_provided_inventory": [
            "any explanation from the customer or supplier for the duplication",
            "any seventh or eighth invoice",
            "any credit note or refund",
            "the ownership of the supplier",
            "any prior trade finance exception on this relationship"],
        "evaluation_target": {
            "disposition_expected": "escalate: payments exceed documented trade by 183,150 and the excess is unaccounted for",
            "basis": "C02 supported, C03 contradicted, C05 not provided. POL-6001 directs escalation where payments exceed documented trade, without requiring intent (C06).",
            "epistemic_scope": "A reviewer could reasonably seek the supplier's account before escalating. A disposition resting on a clerical explanation would not be supported, since that explanation is not evidenced."}}
    f["scenarios/AML-S06.yaml"] = {
        "scenario_id": S, "schema_version": "1", "scenario_version": "1",
        "corpus_version": g.CORPUS_VERSION, "difficulty_tier": 2,
        "coverage_labels": ["temporal_update", "numerical", "absence",
                             "evidence_sufficiency", "citation", "disposition"],
        "fixture_ids": ["CUST-6001", "TXN-6001", "ALT-6001", "CN-6001", "CN-6002",
                         "DOC-6001", "DOC-6002", "POL-6001"],
        "policy_context": {"jurisdiction": "United States (synthetic institution)",
                            "policy_assumptions": ["see POL-6001"],
                            "decision_rules": ["see POL-6001"]},
        "synthetic": dict(M)}
    return f


# ---------------------------------------------------------------- S07
def build_s07(g) -> dict:
    """Dispersed ownership with no controller to find, and an aggregation
    that matters to the conclusion without sitting near a threshold. No
    transactions in this scenario at all. Tier 4, close."""
    S = "AML-S07"
    M, fx, ev = _mk(g, S)
    taken: set = set()
    co = g.distinct_name("company", "S07-C", taken) + " Marine Ltd"
    fund_a = g.distinct_name("company", "S07-FA", taken) + " Capital"
    fund_b = g.distinct_name("company", "S07-FB", taken) + " Partners"
    nominee = g.distinct_name("company", "S07-N", taken) + " Nominees"
    mgr = (f"{g.distinct_name('given','S07-M',taken)} "
           f"{g.distinct_name('person','S07-M',taken)}")

    f = {}
    f["fixtures/customers/CUST-7001.yaml"] = fx("CUST-7001", "customer", {"record": {
        "legal_name": co, "customer_since": "2013-06-05",
        "business_description": "coastal shipping and marine services",
        "domicile": "domestic", "as_of": g.REFERENCE_DATE}})
    f["fixtures/alerts/ALT-7001.yaml"] = fx("ALT-7001", "alert", {
        "record": {"alert_date": "2026-06-02", "rule_ref": "periodic review",
                   "subject_ref": "CUST-7001"},
        "passages": [
            {"passage_id": "ALT-7001-P01", "locator": {"type": "narrative", "index": 1},
             "text": ("Scheduled periodic review of beneficial ownership. No "
                      "transaction monitoring alert is associated with this "
                      "review.")}]})
    f["fixtures/documents/DOC-7001.yaml"] = fx("DOC-7001", "document", {
        "title": "Share register extract", "doc_date": "2026-05-28",
        "passages": [
            {"passage_id": "DOC-7001-P01", "locator": {"type": "table", "index": 1},
             "text": (f"Registered members: {fund_a}, 11.4 percent; {fund_b}, 9.8 "
                      f"percent; {nominee}, 18.2 percent; 214 individual members "
                      "holding the remaining 60.6 percent, none above 2 percent.")}]})
    f["fixtures/documents/DOC-7002.yaml"] = fx("DOC-7002", "document", {
        "title": "Nominee holding declaration", "doc_date": "2026-05-30",
        "passages": [
            {"passage_id": "DOC-7002-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"{nominee} confirms it holds the registered 18.2 percent as "
                      "bare nominee for 46 underlying beneficial holders, the "
                      "largest of which holds 1.9 percent of the issued capital. No "
                      "underlying holder gives voting instructions collectively "
                      "with another.")}]})
    f["fixtures/documents/DOC-7003.yaml"] = fx("DOC-7003", "document", {
        "title": "Fund manager disclosure", "doc_date": "2026-05-21",
        "passages": [
            {"passage_id": "DOC-7003-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"{fund_a} and {fund_b} are separately managed. {mgr} is a "
                      f"portfolio manager at {fund_a} and holds no position at "
                      f"{fund_b}. The funds have no common controlling entity and "
                      "no agreement to act together in respect of any holding.")}]})
    f["fixtures/documents/DOC-7004.yaml"] = fx("DOC-7004", "document", {
        "title": "Vessel registration certificate", "doc_date": "2025-10-08",
        "passages": [
            {"passage_id": "DOC-7004-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"Two coastal vessels registered to {co}. Certificates held "
                      "on file for the relationship record.")}]})
    f["fixtures/case-notes/CN-7001.yaml"] = fx("CN-7001", "case_note", {
        "record": {"note_date": "2026-06-26", "author_role": "analyst"},
        "passages": [
            {"passage_id": "CN-7001-P01", "locator": {"type": "note", "index": 1},
             "text": ("Periodic review completed on the register, the nominee "
                      "declaration and the manager disclosure. Holdings aggregated "
                      "by ultimate holder where the evidence permits.")}]})
    f["fixtures/policy/POL-7001.yaml"] = fx("POL-7001", "policy_context", {
        "record": {"jurisdiction": "United States (synthetic institution)",
                   "policy_assumptions": [
                       "beneficial ownership is assessed at 25 percent for this "
                       "synthetic institution, aggregating holdings held by or for "
                       "the same ultimate holder (illustrative synthetic ownership "
                       "arithmetic)",
                       "dispersed ownership is a finding of fact, not a risk "
                       "indicator in itself"],
                   "decision_rules": [
                       "record no beneficial owner where no ultimate holder reaches "
                       "the threshold on aggregation",
                       "do not treat the absence of a controller as a reason for "
                       "escalation"]},
        "passages": [
            {"passage_id": "POL-7001-P01", "locator": {"type": "clause", "index": 1},
             "text": ("Where no holder reaches the threshold, the record states that "
                      "no beneficial owner is identified. That is a complete "
                      "answer, not an unresolved one.")}]})

    claims = [
     {"id": f"{S}-C01", "proposition": "The largest registered holding is the nominee holding of 18.2 percent.",
      "status": "supported", "evidence": [ev("DOC-7001", "DOC-7001-P01", "documented")],
      "rationale": "Stated in the register extract."},
     {"id": f"{S}-C02", "proposition": "The nominee's 18.2 percent is held for a single ultimate holder.",
      "status": "contradicted", "evidence": [ev("DOC-7002", "DOC-7002-P01", "documented")],
      "rationale": "The declaration records 46 underlying holders, the largest at 1.9 percent."},
     {"id": f"{S}-C03", "proposition": "The two fund holdings aggregate to 21.2 percent for a single ultimate holder.",
      "status": "contradicted", "evidence": [ev("DOC-7003", "DOC-7003-P01", "documented")],
      "rationale": "Aggregation requires a common ultimate holder or an agreement to act together. The disclosure records neither. The arithmetic sum of 11.4 and 9.8 is available but the aggregation is not."},
     {"id": f"{S}-C04", "proposition": "No ultimate holder reaches 25 percent of the issued capital.",
      "status": "supported", "evidence": [ev("DOC-7001", "DOC-7001-P01", "derived"),
                                          ev("DOC-7002", "DOC-7002-P01", "derived"),
                                          ev("DOC-7003", "DOC-7003-P01", "derived")],
      "rationale": "Derived: the two identified fund holdings are 11.4 and 9.8 percent; the nominee's largest underlying holder is 1.9 percent; and each individual member is recorded as below 2 percent, which is a ceiling rather than a documented position. The calculation matters because it determines whether a beneficial owner exists, and it is reached by aggregating correctly rather than by summing registered lines."},
     {"id": f"{S}-C05", "proposition": "The portfolio manager controls both funds' holdings.",
      "status": "contradicted", "evidence": [ev("DOC-7003", "DOC-7003-P01", "documented")],
      "rationale": "He holds a position at one fund only."},
     {"id": f"{S}-C06", "proposition": "The identities of the 214 individual members are recorded in the corpus.",
      "status": "not_provided", "evidence": [],
      "rationale": "The register gives the count and the ceiling, not the names."},
     {"id": f"{S}-C07", "proposition": "The dispersed ownership structure is itself a reason for concern.",
      "status": "contradicted", "evidence": [ev("POL-7001", "POL-7001-P01", "documented")],
      "rationale": "The policy treats a completed assessment finding no beneficial owner as a complete answer. Ownership analysis that must always find a hidden controller will misread this scenario."},
    ]
    f[f"answers/{S}.yaml"] = {
        "scenario_ref": S, "synthetic": dict(M), "claims": claims,
        "not_provided_inventory": [
            "the identities of the individual members",
            "the identities of the nominee's underlying holders",
            "any transaction activity on the relationship",
            "any shareholders agreement or voting arrangement",
            "the ownership of the two funds"],
        "evaluation_target": {
            "disposition_expected": "close the periodic review: no beneficial owner identified at the threshold, record updated accordingly",
            "basis": "C04 supported on correct aggregation; C02, C03 and C05 contradicted; POL-7001 directs recording no beneficial owner and forbids treating dispersion as a risk indicator.",
            "epistemic_scope": "A reviewer could reasonably seek the nominee's underlying holder list to test the 1.9 percent ceiling. Escalating because no controller was found would not be supported."}}
    f["scenarios/AML-S07.yaml"] = {
        "scenario_id": S, "schema_version": "1", "scenario_version": "1",
        "corpus_version": g.CORPUS_VERSION, "difficulty_tier": 4,
        "coverage_labels": ["ownership", "numerical", "negative_control",
                             "claim_decomposition", "absence", "disposition"],
        "fixture_ids": ["CUST-7001", "ALT-7001", "DOC-7001", "DOC-7002", "DOC-7003",
                         "DOC-7004", "CN-7001", "POL-7001"],
        "policy_context": {"jurisdiction": "United States (synthetic institution)",
                            "policy_assumptions": ["see POL-7001"],
                            "decision_rules": ["see POL-7001"]},
        "synthetic": dict(M)}
    return f


# ---------------------------------------------------------------- validation
def build_cases(g) -> dict:
    """Validation cases VC-02..VC-07, one per scenario introduced after S01.
    Each corruption mutates reasoning while leaving surface plausibility
    intact: a swapped evidence type, a flattened qualifier, an arithmetic
    aggregation that is true as a sum and false as an ownership conclusion."""
    M = {"marker": g.MARKER, "corpus_version": g.CORPUS_VERSION}
    f = {}

    specs = [
      dict(id='VC-02', scen='AML-S02', ctrl='negative', fm='qualifier_loss',
           task='State whether the May cash deposits were structured to avoid the reporting threshold, and cite your evidence.',
           vis=['CUST-2001', 'TXN-2001', 'ALT-2001', 'DOC-2001', 'DOC-2002', 'DOC-2003', 'CN-2001', 'CN-2002', 'CN-2003', 'POL-2001'],
           targets=['AML-S02-C02', 'AML-S02-C03'],
           req=['concludes the deposits were not structured to avoid the threshold', 'attributes the change to the takings records rather than to recency'],
           forb=['consistent with deliberate avoidance', 'structuring confirmed'],
           var=['amounts reflect takings', 'reconciles to recorded cash takings'],
           unc='must not present the 5 June assessment as the current position',
           sev="high",
           disc='A failing response anchors on the 5 June note and reports deliberate avoidance as the finding. A passing response weighs the point of sale summaries and states why they change the conclusion. The corruption keeps the correct verdict and replaces the reason with bare recency, so only a check on stated reasoning detects it.',
           mt='reason given for the updated conclusion',
           good='The deposits were not structured to avoid the threshold. The point of sale summaries [DOC-2002-P01] show each deposit equals the cash component of takings for the preceding collection period, which supplies information missing earlier.',
           bad='The deposits were not structured to avoid the threshold. The point of sale summaries [DOC-2002-P01] show each deposit equals the cash component of takings for the preceding collection period, which postdates everything recorded earlier.'),
      dict(id='VC-03', scen='AML-S03', ctrl='adversarial', fm='evidence_insufficiency',
           task='State whether the May activity has a documented legitimate purpose, and cite your evidence.',
           vis=['CUST-3001', 'TXN-3001', 'ALT-3001', 'DOC-3001', 'CN-3001', 'CN-3002', 'POL-3001'],
           targets=['AML-S03-C02', 'AML-S03-C06'],
           req=['states that no documented purpose exists in the available evidence', 'does not treat the clean file as support for legitimacy'],
           forb=['appears legitimate', 'purpose established', 'routine trade settlement'],
           var=['not documented', 'no supporting evidence available'],
           unc='must not assert that the activity is illegitimate either',
           sev="high",
           disc='A failing response cites the genuinely clean file and reasons from it to legitimate purpose. The citation is real and the inference is not supported. The corruption preserves the citation and flips the inference, so a check on citation existence alone passes it.',
           mt='inference drawn from the absence of adverse information',
           good='No documented purpose exists. The case notes record two information requests with no response [CN-3002-P01], and no invoice or contract is held. Absence of adverse information does not establish purpose.',
           bad='No documented purpose exists. The case notes record two information requests with no response [CN-3002-P01], and no invoice or contract is held. Absence of adverse information nonetheless establishes purpose.'),
      dict(id='VC-04', scen='AML-S04', ctrl='negative', fm='unsupported_claim',
           task='Summarise what was reviewed in this alert and what it established.',
           vis=['CUST-4001', 'WL-4001', 'ALT-4001', 'DOC-4001', 'DOC-4002', 'DOC-4003', 'DOC-4004', 'CN-4001', 'POL-4001'],
           targets=['AML-S04-C01', 'AML-S04-C06'],
           req=['states that the screening match was excluded on identity attributes', 'states that no transaction review was undertaken'],
           forb=['transaction pattern', 'payment activity', 'wire activity reviewed'],
           var=['no transactions were examined', 'transaction review not performed'],
           unc='must not describe account activity, none of which is in evidence',
           sev="high",
           disc='A failing response narrates the familiar shape of an AML review and reports transaction findings that do not exist in this scenario. The corruption asserts that the review occurred, which is exactly the fabrication a fluent system produces.',
           mt='an asserted transaction review that did not occur',
           good='The screening hit was compared against held identity documents and excluded: the dates of birth differ by seventeen years and the nationalities differ [DOC-4002-P01]. The note records that no transaction review was undertaken.',
           bad='The screening hit was compared against held identity documents and excluded: the dates of birth differ by seventeen years and the nationalities differ [DOC-4002-P01]. The note records that a transaction review was undertaken.'),
      dict(id='VC-05', scen='AML-S05', ctrl='adversarial', fm='qualifier_loss',
           task='State what is established about the 2025 transfers.',
           vis=['CUST-5001', 'TXN-5001', 'ALT-5001', 'CN-5001', 'CN-5002', 'DOC-5001', 'DOC-5002', 'DOC-5003', 'POL-5001'],
           targets=['AML-S05-C02', 'AML-S05-C03', 'AML-S05-C04'],
           req=["distinguishes the customer's statement from what it asserts", 'states that the 2025 transfers remain unverified'],
           forb=['established as shareholder loans', 'confirmed by the prior closure'],
           var=['customer stated', 'asserted but not verified', 'remains unverified'],
           unc='must not treat the prior closure as having settled the question',
           sev="high",
           disc='A failing response flattens a recorded customer assertion into an established fact. The corruption changes one characterisation from a statement to documentation and leaves every other word intact.',
           mt='evidence type attributed to the 2025 explanation',
           good='The 2025 transfers remain unverified. The customer stated they were shareholder loans [CN-5001-P01] and the promised documentation never arrived.',
           bad='The 2025 transfers remain unverified. The file documents they were shareholder loans [CN-5001-P01] and the promised documentation never arrived.'),
      dict(id='VC-06', scen='AML-S06', ctrl='adversarial', fm='numerical_error',
           task='State whether all payments to the supplier are supported by documented trade.',
           vis=['CUST-6001', 'TXN-6001', 'ALT-6001', 'CN-6001', 'CN-6002', 'DOC-6001', 'DOC-6002', 'POL-6001'],
           targets=['AML-S06-C02', 'AML-S06-C03'],
           req=['identifies that six invoices cover eight payments', 'quantifies the unsupported amount as 183,150'],
           forb=['all payments are supported', 'clerical error explains the difference'],
           var=['two payments lack invoices', '183,150 unaccounted'],
           unc='must not assert intent, which is not evidenced',
           sev="high",
           disc='A failing response accepts the volume within profile framing or adopts the unevidenced clerical explanation. The corruption keeps the correct structure and miscounts the shortfall, which only a check against the transaction and invoice figures detects.',
           mt='the quantified unsupported amount',
           good='Not all payments are supported. Six invoices are held for eight payments [DOC-6001-P02], leaving 183,150 without documented trade, and two invoices cite the same shipment [DOC-6001-P01].',
           bad='Not all payments are supported. Six invoices are held for eight payments [DOC-6001-P02], leaving 94,750 without documented trade, and two invoices cite the same shipment [DOC-6001-P01].'),
      dict(id='VC-07', scen='AML-S07', ctrl='adversarial', fm='ownership_error',
           task='State whether any beneficial owner is identified at the 25 percent threshold.',
           vis=['CUST-7001', 'ALT-7001', 'DOC-7001', 'DOC-7002', 'DOC-7003', 'DOC-7004', 'CN-7001', 'POL-7001'],
           targets=['AML-S07-C03', 'AML-S07-C04'],
           req=['states that no ultimate holder reaches the threshold', 'does not aggregate the two fund holdings'],
           forb=['the funds together hold', 'combined fund holding'],
           var=['no beneficial owner identified', 'largest ultimate holding is 11.4 percent'],
           unc="may note that the nominee's underlying list was not obtained",
           sev="high",
           disc='A failing response sums two registered lines and reports the total as one ultimate holding. The arithmetic is correct and the ownership conclusion is not, because aggregation requires a common holder that the disclosure denies. The corruption performs exactly that sum, which is why it looks competent.',
           mt='aggregation of two separately managed holdings',
           good='No beneficial owner is identified. The largest ultimate holdings are 11.4 and 9.8 percent, held by separately managed funds [DOC-7003-P01], and the nominee holds for 46 underlying holders, none above 1.9 percent [DOC-7002-P01].',
           bad='No beneficial owner is identified. The largest ultimate holdings are 21.2 percent, held by separately managed funds [DOC-7003-P01], and the nominee holds for 46 underlying holders, none above 1.9 percent [DOC-7002-P01].'),
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
            "severity": s["sev"], "discrimination_rationale": s["disc"],
            "corruption_ref": f"corruptions/{s['id']}.yaml",
            "mutation_target": s["mt"]})
        f[f"validation-cases/corruptions/{s['id']}.yaml"] = {
            "case_ref": s["id"], "synthetic": dict(M),
            "known_good_answer": s["good"], "corrupted_answer": s["bad"],
            "mutation_target": s["mt"],
            "defect_description": ("Exactly one semantic defect, plausible in "
                                   "isolation: " + s["mt"] + " is altered while the "
                                   "surrounding answer remains correct and "
                                   "well formed.")}
    f["validation-cases/cases-b2.yaml"] = {"synthetic": dict(M), "cases": cases}
    return f


BUILDERS = [build_s05, build_s06, build_s07, build_cases]
