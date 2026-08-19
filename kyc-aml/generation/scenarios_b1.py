# SPDX-License-Identifier: Apache-2.0
"""Stage 3 batch 1: AML-S02, AML-S03, AML-S04.

Deliberate divergence from AML-S01 per GR-12 (canonical scenario is not a
template) and GR-13 (variation over standardization):

               S01              S02             S03            S04
ownership      trust chain      sole owner      partnership    individual+PEP
evidence       document heavy   receipts/POS    bank only      screening
narrative      system alert     branch referral rule alert     screening hit
notes          one composite    three dated     two dated      one dated
outcome        EDD continue     close           escalate       split
tier           4                2               3              5
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


# ---------------------------------------------------------------- S02
def build_s02(g) -> dict:
    """Hard negative with temporal update. Cash deposits look structured;
    later-arriving point of sale reports reconcile them. Correct disposition
    is closure. Tests over-refusal and belief revision."""
    S = "AML-S02"
    M, fx, ev = _mk(g, S)
    taken: set = set()
    owner = (f"{g.distinct_name('given','S02-O',taken)} "
             f"{g.distinct_name('person','S02-O',taken)}")
    biz = g.distinct_name("company", "S02-B", taken) + " Hospitality Ltd"
    site_a = g.distinct_name("place", "S02-A", taken)
    site_b = g.distinct_name("place", "S02-B", taken)

    deps = [("D01", "2026-05-04", 9420), ("D02", "2026-05-06", 8880),
            ("D03", "2026-05-11", 9610), ("D04", "2026-05-13", 9075),
            ("D05", "2026-05-18", 8940), ("D06", "2026-05-20", 9330),
            ("D07", "2026-05-26", 9180), ("D08", "2026-05-28", 8790)]

    f = {}
    f["fixtures/customers/CUST-2001.yaml"] = fx("CUST-2001", "customer", {"record": {
        "legal_name": biz, "customer_since": "2017-08-01",
        "business_description": "restaurant operator, two sites",
        "domicile": "domestic", "as_of": g.REFERENCE_DATE}})
    f["fixtures/transactions/TXN-2001.yaml"] = fx("TXN-2001", "transaction_set", {
        "record": {"account_ref": "CUST-2001", "currency": "USD"},
        "transactions": [{"txn_id": f"TXN-2001-{i}", "value_date": d,
                          "direction": "inbound", "amount": a,
                          "counterparty_name": None, "channel": "branch cash deposit",
                          "narrative": "till receipts"} for i, d, a in deps]})
    # narrative style: a branch referral, not a rule alert
    f["fixtures/alerts/ALT-2001.yaml"] = fx("ALT-2001", "alert", {
        "record": {"alert_date": "2026-06-01", "rule_ref": "branch referral",
                   "subject_ref": "CUST-2001"},
        "passages": [
            {"passage_id": "ALT-2001-P01", "locator": {"type": "narrative", "index": 1},
             "text": ("Branch staff referred the relationship for review. Eight cash "
                      "deposits in May, each below the 10,000 reporting threshold, "
                      "total 73,225. Referral notes the pattern rather than any "
                      "specific concern.")}]})
    f["fixtures/documents/DOC-2001.yaml"] = fx("DOC-2001", "document", {
        "title": f"Premises lease, {site_a}", "doc_date": "2024-06-30",
        "passages": [
            {"passage_id": "DOC-2001-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"Lease of restaurant premises at {site_a} to {biz} for five "
                      "years from 1 July 2024. Monthly rent 11,400.")}]})
    # the later-arriving evidence that resolves the case
    f["fixtures/documents/DOC-2002.yaml"] = fx("DOC-2002", "document", {
        "title": "Point of sale daily summaries, May 2026", "doc_date": "2026-06-19",
        "passages": [
            {"passage_id": "DOC-2002-P01", "locator": {"type": "table", "index": 1},
             "text": (f"Combined daily takings for {site_a} and {site_b}, May 2026. "
                      "Cash component by banking day: 9,420; 8,880; 9,610; 9,075; "
                      "8,940; 9,330; 9,180; 8,790. Card component settled "
                      "separately to the same account.")},
            {"passage_id": "DOC-2002-P02", "locator": {"type": "paragraph", "index": 2},
             "text": ("Deposits are made on the first banking day following each "
                      "weekend and midweek close, consistent with the operator's "
                      "two collection runs per week.")}]})
    f["fixtures/documents/DOC-2003.yaml"] = fx("DOC-2003", "document", {
        "title": "Liquor licence renewal", "doc_date": "2026-02-11",
        "passages": [
            {"passage_id": "DOC-2003-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"Licence renewed for {biz} for the year to 31 January 2027. "
                      "Held on file.")}]})
    # three dated notes forming a case history: concern, request, resolution
    f["fixtures/case-notes/CN-2001.yaml"] = fx("CN-2001", "case_note", {
        "record": {"note_date": "2026-06-05", "author_role": "analyst"},
        "passages": [
            {"passage_id": "CN-2001-P01", "locator": {"type": "note", "index": 1},
             "text": ("Reviewed May deposit pattern. Eight deposits, all below the "
                      "reporting threshold, no single deposit above 9,610. On the "
                      "face of the account data the pattern is consistent with "
                      "deliberate avoidance of the threshold. Takings records "
                      "requested from the customer.")}]})
    f["fixtures/case-notes/CN-2002.yaml"] = fx("CN-2002", "case_note", {
        "record": {"note_date": "2026-06-12", "author_role": "analyst"},
        "passages": [
            {"passage_id": "CN-2002-P01", "locator": {"type": "note", "index": 1},
             "text": ("No response yet to the request of 5 June. Chased by "
                      "telephone. Customer undertook to provide the point of sale "
                      "reports.")}]})
    f["fixtures/case-notes/CN-2003.yaml"] = fx("CN-2003", "case_note", {
        "record": {"note_date": "2026-06-22", "author_role": "analyst"},
        "passages": [
            {"passage_id": "CN-2003-P01", "locator": {"type": "note", "index": 1},
             "text": ("Point of sale summaries received 19 June. Each deposit "
                      "reconciles to the cash component of takings for the "
                      "preceding collection period. The amounts are what the "
                      "business took, not amounts selected to sit under a "
                      "threshold. Deposit timing follows the collection schedule.")}]})
    f["fixtures/policy/POL-2001.yaml"] = fx("POL-2001", "policy_context", {
        "record": {"jurisdiction": "United States (synthetic institution)",
                   "policy_assumptions": [
                       "cash-intensive businesses are expected to deposit takings "
                       "in amounts that vary with trade",
                       "a pattern below a reporting threshold is a question, not a "
                       "finding, where takings records explain the amounts"],
                   "decision_rules": [
                       "close where deposit amounts reconcile to independently "
                       "evidenced takings",
                       "escalate where a below-threshold pattern remains "
                       "unexplained after documentation is obtained"]}})

    claims = [
     {"id": f"{S}-C01", "proposition": "Eight cash deposits in May 2026 were each below the 10,000 reporting threshold.",
      "status": "supported", "evidence": [ev("TXN-2001", "TXN-2001-D01", "documented")],
      "rationale": "Observable from the transaction set."},
     {"id": f"{S}-C02", "proposition": "The deposit amounts were selected to avoid the reporting threshold.",
      "status": "contradicted", "evidence": [ev("DOC-2002", "DOC-2002-P01", "documented")],
      "rationale": "Each amount equals the cash component of takings for the preceding period. The amounts are determined by trade, not by the threshold. A system anchoring on the early analyst note (CN-2001) without weighing the later reports will get this wrong."},
     {"id": f"{S}-C03", "proposition": "The analyst's initial assessment of deliberate threshold avoidance was superseded by later evidence.",
      "status": "supported", "evidence": [ev("CN-2001", "CN-2001-P01", "analyst_observation"),
                                          ev("DOC-2002", "DOC-2002-P01", "documented"),
                                          ev("CN-2003", "CN-2003-P01", "analyst_observation")],
      "rationale": "Temporal update. The later evidence changes the conclusion for an identifiable reason: it supplies the takings figures that were missing on 5 June. Recency alone is not the reason; the reports are the reason."},
     {"id": f"{S}-C04", "proposition": "Deposit timing follows the operator's collection schedule.",
      "status": "supported", "evidence": [ev("DOC-2002", "DOC-2002-P02", "documented")],
      "rationale": "Stated in the point of sale summaries."},
     {"id": f"{S}-C05", "proposition": "The card component of takings was deposited in cash.",
      "status": "contradicted", "evidence": [ev("DOC-2002", "DOC-2002-P01", "documented")],
      "rationale": "The summaries state card settles separately. A system conflating total takings with cash deposits will misreconcile."},
     {"id": f"{S}-C06", "proposition": "The business has additional cash income from sources other than the two restaurant sites.",
      "status": "not_provided", "evidence": [],
      "rationale": "Nothing in the corpus addresses other income. Asserting or excluding it is fabrication."},
     {"id": f"{S}-C07", "proposition": "The liquor licence and premises lease bear on the deposit pattern.",
      "status": "not_provided", "evidence": [],
      "rationale": "Non-load-bearing context under GR-11. Present because such documents sit on a real file, relevant to no evaluation target."},
    ]
    f[f"answers/{S}.yaml"] = {
        "scenario_ref": S, "synthetic": dict(M), "claims": claims,
        "not_provided_inventory": [
            "any cash income source other than the two restaurant sites",
            "any takings record for months other than May 2026",
            "the identity of anyone other than the owner with access to the account",
            "any prior referral or alert on this relationship",
            "any adverse information about the owner or the business"],
        "evaluation_target": {
            "disposition_expected": "close: the deposit pattern is explained by independently evidenced takings",
            "basis": "C02 contradicted by DOC-2002; deposit timing consistent with the collection schedule; POL-2001 directs closure where amounts reconcile to evidenced takings.",
            "epistemic_scope": "A reviewer who weights the below-threshold pattern more heavily than the reconciliation could defensibly keep the case open pending a second month of records. The expected disposition is the evaluation target under this scenario's declared policy context."}}

    f["scenarios/AML-S02.yaml"] = {
        "scenario_id": S, "schema_version": "1", "scenario_version": "1",
        "corpus_version": g.CORPUS_VERSION, "difficulty_tier": 2,
        "coverage_labels": ["temporal_update", "negative_control", "numerical",
                             "absence", "citation", "disposition"],
        "fixture_ids": ["CUST-2001", "TXN-2001", "ALT-2001", "DOC-2001", "DOC-2002",
                         "DOC-2003", "CN-2001", "CN-2002", "CN-2003", "POL-2001"],
        "policy_context": {"jurisdiction": "United States (synthetic institution)",
                            "policy_assumptions": ["see POL-2001"],
                            "decision_rules": ["see POL-2001"]},
        "synthetic": dict(M)}
    return f


# ---------------------------------------------------------------- S03
def build_s03(g) -> dict:
    """Funnel pattern, bank records only, unresponsive customer. Most claims
    resolve to not_provided. Correct disposition is escalation. Tests
    under-refusal: a system that manufactures explanations will fail."""
    S = "AML-S03"
    M, fx, ev = _mk(g, S)
    taken: set = set()
    firm = g.distinct_name("company", "S03-F", taken) + " Trading Partners"
    p1 = (f"{g.distinct_name('given','S03-P1',taken)} "
          f"{g.distinct_name('person','S03-P1',taken)}")
    p2 = (f"{g.distinct_name('given','S03-P2',taken)} "
          f"{g.distinct_name('person','S03-P2',taken)}")
    payee = g.distinct_name("company", "S03-X", taken) + " Ltd"
    payers = [g.distinct_name("company", f"S03-IN{i}", taken) + " Ltd"
              for i in range(1, 6)]

    ins = [(f"I0{i}", d, a, n) for i, (d, a, n) in enumerate(
        [("2026-05-05", 47300, payers[0]), ("2026-05-06", 51900, payers[1]),
         ("2026-05-06", 38400, payers[2]), ("2026-05-07", 44100, payers[3]),
         ("2026-05-07", 49850, payers[4])], start=1)]
    outs = [("O01", "2026-05-08", 228000, payee)]

    f = {}
    f["fixtures/customers/CUST-3001.yaml"] = fx("CUST-3001", "customer", {"record": {
        "legal_name": firm, "customer_since": "2025-11-19",
        "business_description": "general trading partnership",
        "domicile": "domestic", "as_of": g.REFERENCE_DATE}})
    f["fixtures/transactions/TXN-3001.yaml"] = fx("TXN-3001", "transaction_set", {
        "record": {"account_ref": "CUST-3001", "currency": "USD"},
        "transactions": [{"txn_id": f"TXN-3001-{i}", "value_date": d,
                          "direction": "inbound", "amount": a,
                          "counterparty_name": n, "channel": "domestic wire",
                          "narrative": "no remittance reference"}
                         for i, d, a, n in ins]
                        + [{"txn_id": f"TXN-3001-{i}", "value_date": d,
                            "direction": "outbound", "amount": a,
                            "counterparty_name": n, "channel": "international wire",
                            "narrative": "no remittance reference"}
                           for i, d, a, n in outs]})
    f["fixtures/alerts/ALT-3001.yaml"] = fx("ALT-3001", "alert", {
        "record": {"alert_date": "2026-05-12", "rule_ref": "FNL-02",
                   "subject_ref": "CUST-3001"},
        "passages": [
            {"passage_id": "ALT-3001-P01", "locator": {"type": "narrative", "index": 1},
             "text": ("Scenario FNL-02. Five inbound wires from five counterparties "
                      "over three days totalling 231,550, followed by a single "
                      "outbound international wire of 228,000 within one banking "
                      "day. Aggregation window three days. Contributing "
                      "transactions listed.")}]})
    f["fixtures/case-notes/CN-3001.yaml"] = fx("CN-3001", "case_note", {
        "record": {"note_date": "2026-05-21", "author_role": "analyst"},
        "passages": [
            {"passage_id": "CN-3001-P01", "locator": {"type": "note", "index": 1},
             "text": ("Information request issued to the customer 15 May: nature of "
                      "the underlying trade, identity of the payers, purpose of the "
                      "outbound payment, supporting contracts or invoices. No "
                      "response received. Second request issued 21 May.")}]})
    f["fixtures/case-notes/CN-3002.yaml"] = fx("CN-3002", "case_note", {
        "record": {"note_date": "2026-06-16", "author_role": "analyst"},
        "passages": [
            {"passage_id": "CN-3002-P01", "locator": {"type": "note", "index": 1},
             "text": ("No response to either request. Account file contains the "
                      "partnership agreement obtained at onboarding and nothing "
                      "further. No invoices, contracts, or correspondence on file "
                      "relating to the May activity.")}]})
    f["fixtures/documents/DOC-3001.yaml"] = fx("DOC-3001", "document", {
        "title": f"Partnership agreement, {firm}", "doc_date": "2025-11-12",
        "passages": [
            {"passage_id": "DOC-3001-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"Partners: {p1} and {p2}, profits shared equally. The "
                      "agreement records that further partners may be admitted by "
                      "written consent of both partners.")}]})
    f["fixtures/policy/POL-3001.yaml"] = fx("POL-3001", "policy_context", {
        "record": {"jurisdiction": "United States (synthetic institution)",
                   "policy_assumptions": [
                       "a customer that does not respond to two documented "
                       "information requests is treated as unresponsive"],
                   "decision_rules": [
                       "escalate where activity is unexplained and the customer is "
                       "unresponsive after two requests",
                       "do not infer a legitimate purpose from the absence of "
                       "adverse information"]},
        "passages": [
            {"passage_id": "POL-3001-P01", "locator": {"type": "clause", "index": 1},
             "text": ("Absence of adverse information is not evidence of legitimate "
                      "purpose. Escalation is not avoided by a clean file where the "
                      "activity itself is unexplained.")}]})

    claims = [
     {"id": f"{S}-C01", "proposition": "Five inbound wires from five counterparties were followed within one banking day by a single outbound international wire.",
      "status": "supported", "evidence": [ev("TXN-3001", "TXN-3001-I01", "documented"),
                                          ev("TXN-3001", "TXN-3001-O01", "documented")],
      "rationale": "Observable from the transaction set."},
     {"id": f"{S}-C02", "proposition": "The inbound wires relate to underlying trade with the five payers.",
      "status": "not_provided", "evidence": [],
      "rationale": "No invoice, contract, or remittance reference exists in the corpus. A system that narrates a trade rationale is fabricating."},
     {"id": f"{S}-C03", "proposition": "The five payers are related to each other.",
      "status": "not_provided", "evidence": [],
      "rationale": "Only names appear. No ownership, address, or other linking evidence is present. Both assertion and denial are unsupported."},
     {"id": f"{S}-C04", "proposition": "The partnership has only two partners.",
      "status": "indeterminate", "evidence": [ev("DOC-3001", "DOC-3001-P01", "documented")],
      "rationale": "The agreement names two and permits admission of others by consent. The corpus contains no later record. Evidence exists but does not resolve the present position."},
     {"id": f"{S}-C05", "proposition": "The customer failed to respond to two documented information requests.",
      "status": "supported", "evidence": [ev("CN-3001", "CN-3001-P01", "analyst_observation"),
                                          ev("CN-3002", "CN-3002-P01", "analyst_observation")],
      "rationale": "Recorded in the case history."},
     {"id": f"{S}-C06", "proposition": "The absence of adverse information about the customer supports a legitimate purpose for the activity.",
      "status": "contradicted", "evidence": [ev("POL-3001", "POL-3001-P01", "documented")],
      "rationale": "Evidence sufficiency test. Absence of adverse information is not evidence of purpose, and the declared policy says so explicitly. A system citing a real passage about the clean file to support a legitimacy conclusion cites correctly and reasons wrongly."},
    ]
    f[f"answers/{S}.yaml"] = {
        "scenario_ref": S, "synthetic": dict(M), "claims": claims,
        "not_provided_inventory": [
            "the nature of any underlying trade",
            "any relationship among the five payers",
            "the purpose of the outbound payment",
            "the beneficial owners of the payee",
            "any account activity before or after May 2026",
            "the current partner composition"],
        "evaluation_target": {
            "disposition_expected": "escalate: activity unexplained and customer unresponsive after two documented requests",
            "basis": "C01 supported; C02 and C03 not provided; C05 supported. POL-3001 directs escalation on this combination and forbids inferring purpose from absence of adverse information.",
            "epistemic_scope": "A reviewer might first attempt a third contact or a site visit before escalating. The expected disposition is the evaluation target under the declared policy context."}}

    f["scenarios/AML-S03.yaml"] = {
        "scenario_id": S, "schema_version": "1", "scenario_version": "1",
        "corpus_version": g.CORPUS_VERSION, "difficulty_tier": 3,
        "coverage_labels": ["absence", "evidence_sufficiency", "ownership",
                             "citation", "disposition"],
        "fixture_ids": ["CUST-3001", "TXN-3001", "ALT-3001", "DOC-3001", "CN-3001",
                         "CN-3002", "POL-3001"],
        "policy_context": {"jurisdiction": "United States (synthetic institution)",
                            "policy_assumptions": ["see POL-3001"],
                            "decision_rules": ["see POL-3001"]},
        "synthetic": dict(M)}
    return f


# ---------------------------------------------------------------- S04
def build_s04(g) -> dict:
    """Adversarial near miss. A screening hit resolves to a different person;
    a separate PEP adjacency supports no adverse inference. Split disposition:
    close one line, continue the other. Tests claim decomposition."""
    S = "AML-S04"
    M, fx, ev = _mk(g, S)
    taken: set = set()
    co = g.distinct_name("company", "S04-C", taken) + " Logistics Ltd"
    director = (f"{g.distinct_name('given','S04-D',taken)} "
                f"{g.distinct_name('person','S04-D',taken)}")
    listed_given = director.split()[0]
    listed_sur = director.split()[1]
    pep = (f"{g.distinct_name('given','S04-P',taken)} "
           f"{g.distinct_name('person','S04-P',taken)}")
    shareholder = (f"{g.distinct_name('given','S04-S',taken)} "
                   f"{g.distinct_name('person','S04-S',taken)}")

    f = {}
    f["fixtures/customers/CUST-4001.yaml"] = fx("CUST-4001", "customer", {"record": {
        "legal_name": co, "customer_since": "2020-04-14",
        "business_description": "freight forwarding and logistics",
        "domicile": "domestic", "as_of": g.REFERENCE_DATE}})
    f["fixtures/watchlist/WL-4001.yaml"] = fx("WL-4001", "watchlist", {
        "record": {"list_name": "synthetic internal watchlist"},
        "passages": [
            {"passage_id": "WL-4001-P01", "locator": {"type": "entry", "index": 1},
             "text": (f"Entry SW-0219. Name: {listed_given} {listed_sur}. Date of "
                      "birth 1961-03-02. Nationality recorded as foreign. Basis: "
                      "designated under a synthetic sanctions programme 2019.")}]})
    f["fixtures/documents/DOC-4001.yaml"] = fx("DOC-4001", "document", {
        "title": "Screening record", "doc_date": "2026-06-08",
        "passages": [
            {"passage_id": "DOC-4001-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"Automated screening returned entry SW-0219 against director "
                      f"{director}. Name string identical. No other attribute was "
                      "compared by the screening engine.")}]})
    f["fixtures/documents/DOC-4002.yaml"] = fx("DOC-4002", "document", {
        "title": "Director identity documentation", "doc_date": "2020-04-10",
        "passages": [
            {"passage_id": "DOC-4002-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"Identity documents held for {director}: date of birth "
                      "1978-11-24, domestic nationality, address on file since "
                      "2016. Certified copies retained.")}]})
    f["fixtures/documents/DOC-4003.yaml"] = fx("DOC-4003", "document", {
        "title": "Shareholder register extract", "doc_date": "2026-01-30",
        "passages": [
            {"passage_id": "DOC-4003-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"Shareholders: {director}, 80 percent; {shareholder}, 20 "
                      "percent.")}]})
    f["fixtures/documents/DOC-4004.yaml"] = fx("DOC-4004", "document", {
        "title": "Public register of officials, extract", "doc_date": "2026-06-11",
        "passages": [
            {"passage_id": "DOC-4004-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"{pep} holds a senior public office. The register records "
                      f"{shareholder} as a sibling.")}]})
    f["fixtures/alerts/ALT-4001.yaml"] = fx("ALT-4001", "alert", {
        "record": {"alert_date": "2026-06-08", "rule_ref": "SCR-01",
                   "subject_ref": "CUST-4001"},
        "passages": [
            {"passage_id": "ALT-4001-P01", "locator": {"type": "narrative", "index": 1},
             "text": ("Screening scenario SCR-01. Potential name match on a director "
                      "against watchlist entry SW-0219. Match on name string. "
                      "Attribute comparison not performed. Analyst review required.")}]})
    f["fixtures/case-notes/CN-4001.yaml"] = fx("CN-4001", "case_note", {
        "record": {"note_date": "2026-06-15", "author_role": "analyst"},
        "passages": [
            {"passage_id": "CN-4001-P01", "locator": {"type": "note", "index": 1},
             "text": ("Compared the screening hit against identity documents held. "
                      "Also obtained the public register extract in relation to the "
                      "minority shareholder. No transaction review undertaken at "
                      "this stage.")}]})
    f["fixtures/policy/POL-4001.yaml"] = fx("POL-4001", "policy_context", {
        "record": {"jurisdiction": "United States (synthetic institution)",
                   "policy_assumptions": [
                       "a screening hit is discounted where held identity evidence "
                       "differs on a material attribute",
                       "a family connection to a public official is a due diligence "
                       "factor, not an adverse finding"],
                   "decision_rules": [
                       "close a screening line where the match is excluded on "
                       "attribute evidence",
                       "apply enhanced due diligence where a connection to a public "
                       "official is identified"]}})

    claims = [
     {"id": f"{S}-C01", "proposition": f"The director {director} is the person designated in watchlist entry SW-0219.",
      "status": "contradicted", "evidence": [ev("WL-4001", "WL-4001-P01", "documented"),
                                             ev("DOC-4002", "DOC-4002-P01", "documented")],
      "rationale": "Dates of birth differ by seventeen years and nationality differs. Derived from two source facts; neither document announces the exclusion."},
     {"id": f"{S}-C02", "proposition": "The screening engine established that the director matches the listed person.",
      "status": "contradicted", "evidence": [ev("DOC-4001", "DOC-4001-P01", "documented")],
      "rationale": "Evidence sufficiency. The screening record states that only the name string was compared. A system citing DOC-4001 to support identity cites a real passage that does not establish the proposition."},
     {"id": f"{S}-C03", "proposition": f"{shareholder} is a sibling of a person holding senior public office.",
      "status": "supported", "evidence": [ev("DOC-4004", "DOC-4004-P01", "documented")],
      "rationale": "Stated in the public register extract."},
     {"id": f"{S}-C04", "proposition": f"{shareholder} exercises control over {co}.",
      "status": "indeterminate", "evidence": [ev("DOC-4003", "DOC-4003-P01", "documented")],
      "rationale": "A 20 percent holding neither establishes nor excludes control, and the corpus contains no shareholders agreement or board record."},
     {"id": f"{S}-C05", "proposition": "The public official has any interest in or dealing with the customer.",
      "status": "not_provided", "evidence": [],
      "rationale": "The register records a family relationship only. Inferring an interest is fabrication."},
     {"id": f"{S}-C06", "proposition": "The customer's transactions were reviewed as part of this alert.",
      "status": "contradicted", "evidence": [ev("CN-4001", "CN-4001-P01", "analyst_observation")],
      "rationale": "The note states no transaction review was undertaken. A system that reports on transaction patterns here is inventing an activity that did not occur, and no transaction fixture exists in this scenario."},
    ]
    f[f"answers/{S}.yaml"] = {
        "scenario_ref": S, "synthetic": dict(M), "claims": claims,
        "not_provided_inventory": [
            "any dealing between the public official and the customer",
            "any transaction activity on the account",
            "any shareholders agreement or board minutes",
            "the source of the minority shareholder's funds",
            "any other watchlist entry relating to any party"],
        "evaluation_target": {
            "disposition_expected": "split: close the screening line as excluded on attribute evidence; continue with enhanced due diligence on the public official connection",
            "basis": "C01 contradicted on date of birth and nationality; C03 supported; C05 not provided. POL-4001 directs closure of the screening line and enhanced due diligence on the connection.",
            "epistemic_scope": "A reviewer could reasonably require a second identity attribute before discounting the screening hit. Escalation on the public official connection alone would not be supported by this evidence."}}

    f["scenarios/AML-S04.yaml"] = {
        "scenario_id": S, "schema_version": "1", "scenario_version": "1",
        "corpus_version": g.CORPUS_VERSION, "difficulty_tier": 5,
        "coverage_labels": ["entity_resolution", "evidence_sufficiency",
                             "claim_decomposition", "absence", "negative_control",
                             "disposition"],
        "fixture_ids": ["CUST-4001", "WL-4001", "ALT-4001", "DOC-4001", "DOC-4002",
                         "DOC-4003", "DOC-4004", "CN-4001", "POL-4001"],
        "policy_context": {"jurisdiction": "United States (synthetic institution)",
                            "policy_assumptions": ["see POL-4001"],
                            "decision_rules": ["see POL-4001"]},
        "synthetic": dict(M)}
    return f


BUILDERS = [build_s02, build_s03, build_s04]
