# SPDX-License-Identifier: Apache-2.0
"""AML-S01, the canonical scenario. Authored content with generator-derived
names and IDs so regeneration is byte-identical. Every required canonical
dimension has a causal role in one coherent case:

straightforward supported fact . direct 33 percent shareholder
numerical derivation ........... 12 direct + 22 indirect = 34, crosses the
                                 illustrative 25 only when paths are summed
indeterminate fact ............. trust settlor undisclosed, control unresolvable
not_provided fact .............. wire W6 has no trade documentation
cross-document contradiction ... alert narrative asserts payee jurisdiction A,
                                 corporate extract shows B
qualifier whose loss matters ... customer STATES payee unrelated, unverified
entity-resolution trap ......... shareholder <Base> Holdings Ltd versus payee
                                 <Base> Holding S.A., distinct registrations
numerical trap ................. 148,500 insurance value adjacent to the
                                 184,500 wire amount in the same invoice
innocent explanation ........... five of six wires match documented trade
alternative disposition ........ escalation defensible on the indeterminate
                                 trust; expected target is EDD continuation
"""
from __future__ import annotations

SCENARIO_ID = "AML-S01"

def build(g) -> dict:
    """g = generator module (names, constants). Returns {relpath: obj}."""
    M = {"marker": g.MARKER, "corpus_version": g.CORPUS_VERSION}
    taken: set = set()
    base = g.distinct_name("company", "S01-QHL", taken)   # the ONE deliberate shared token
    cust_co = g.distinct_name("company", "S01-CUST", taken) + " Components Ltd"
    hold_ltd = f"{base} Holdings Ltd"
    payee_sa = f"{base} Holding S.A."
    trust = g.distinct_name("company", "S01-TRUST", taken) + " Trust"
    p_darv = (f"{g.distinct_name('given','S01-P1',taken)} "
              f"{g.distinct_name('person','S01-P1',taken)}")
    p_tosk = (f"{g.distinct_name('given','S01-P2',taken)} "
              f"{g.distinct_name('person','S01-P2',taken)}")
    jur_a = g.distinct_name("jurisdiction", "S01-JA", taken)
    jur_b = g.distinct_name("jurisdiction", "S01-JB", taken)

    def fx(fid, ftype, extra):
        return {"fixture_id": fid, "fixture_type": ftype,
                "scenario_ref": SCENARIO_ID, "synthetic": dict(M), **extra}

    wires = [("T01", "2026-04-08", 184500), ("T02", "2026-04-21", 121300),
             ("T03", "2026-05-02", 96700), ("T04", "2026-05-15", 143800),
             ("T05", "2026-05-29", 97700), ("T06", "2026-06-12", 98000)]

    files = {}
    files["fixtures/customers/CUST-1001.yaml"] = fx("CUST-1001", "customer", {"record": {
        "legal_name": cust_co, "customer_since": "2021-02-17",
        "business_description": "import and wholesale of industrial machine components",
        "domicile": jur_a, "as_of": g.REFERENCE_DATE}})

    files["fixtures/transactions/TXN-1001.yaml"] = fx("TXN-1001", "transaction_set", {
        "record": {"account_ref": "CUST-1001", "currency": "USD"},
        "transactions": [{"txn_id": f"TXN-1001-{t}", "value_date": d,
                          "direction": "outbound", "amount": a,
                          "counterparty_name": payee_sa,
                          "channel": "international wire"} for t, d, a in wires]})

    files["fixtures/alerts/ALT-1001.yaml"] = fx("ALT-1001", "alert", {
        "record": {"alert_date": "2026-06-14", "rule_ref": "TM-114 related-party outflow",
                   "subject_ref": "CUST-1001"},
        "passages": [
            {"passage_id": "ALT-1001-P01", "locator": {"type": "narrative", "index": 1},
             "text": (f"RULE TM-114 FIRED 2026-06-14. SUBJECT CUST-1001 {cust_co}. "
                      f"OUTBOUND WIRES 90D TOTAL USD 742,000 TO {payee_sa}. PAYEE NAME "
                      f"MATCHES REGISTERED SHAREHOLDER {hold_ltd}. POSSIBLE RELATED "
                      "PARTY LAYERING.")},
            {"passage_id": "ALT-1001-P02", "locator": {"type": "narrative", "index": 2},
             "text": (f"SYSTEM NOTE: PAYEE REGISTERED IN {jur_a.upper()}, CONSISTENT "
                      "WITH SHAREHOLDER REGISTRATION. REVIEW REQUIRED.")}]})

    files["fixtures/documents/DOC-1001.yaml"] = fx("DOC-1001", "document", {
        "title": f"Share register extract, {cust_co}", "doc_date": "2024-11-03",
        "passages": [
            {"passage_id": "DOC-1001-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"Registered members of {cust_co} as at 3 November 2024: "
                      f"{hold_ltd}, 55 percent; {p_tosk}, 33 percent; "
                      f"{p_darv}, 12 percent.")}]})

    files["fixtures/documents/DOC-1002.yaml"] = fx("DOC-1002", "document", {
        "title": f"Share register extract, {hold_ltd}", "doc_date": "2025-01-20",
        "passages": [
            {"passage_id": "DOC-1002-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"Registered members of {hold_ltd} ({jur_a} company number "
                      f"H-88231) as at 20 January 2025: {trust}, 60 percent; "
                      f"{p_darv}, 40 percent.")}]})

    files["fixtures/documents/DOC-1003.yaml"] = fx("DOC-1003", "document", {
        "title": f"Trustee correspondence regarding {trust}", "doc_date": "2026-05-20",
        "passages": [
            {"passage_id": "DOC-1003-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"We confirm that {trust} is a validly constituted trust. The "
                      "identities of the settlor and beneficiaries are not disclosed, "
                      "in accordance with the trust's governing law.")}]})

    files["fixtures/documents/DOC-1004.yaml"] = fx("DOC-1004", "document", {
        "title": f"Commercial invoice bundle, {payee_sa} to {cust_co}",
        "doc_date": "2026-06-02",
        "passages": [
            {"passage_id": "DOC-1004-P01", "locator": {"type": "table", "index": 1},
             "text": ("Invoice INV-2101 dated 2026-04-05, machine spindle assemblies, "
                      "total USD 184,500. Declared insurance value USD 148,500. "
                      "Shipment ref SHP-4411.")},
            {"passage_id": "DOC-1004-P02", "locator": {"type": "table", "index": 2},
             "text": ("Invoices INV-2102 through INV-2105: USD 121,300; USD 96,700; "
                      "USD 143,800; USD 97,700. Each references a bill of lading in "
                      "the shipment schedule.")}]})

    files["fixtures/documents/DOC-1005.yaml"] = fx("DOC-1005", "document", {
        "title": f"Corporate registry extract, {payee_sa}", "doc_date": "2026-06-20",
        "passages": [
            {"passage_id": "DOC-1005-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"{payee_sa} is registered in {jur_b}, registration number "
                      f"S-40917, incorporated 2016. Principal activity: distribution "
                      "of industrial components.")},
            {"passage_id": "DOC-1005-P02", "locator": {"type": "paragraph", "index": 2},
             "text": (f"The registry records no shareholding relationship between "
                      f"{payee_sa} ({jur_b}, S-40917) and {hold_ltd} ({jur_a}, "
                      "H-88231). The entities hold distinct registrations in "
                      "distinct jurisdictions.")}]})

    files["fixtures/case-notes/CN-1001.yaml"] = fx("CN-1001", "case_note", {
        "record": {"note_date": "2026-06-18", "author_role": "analyst"},
        "passages": [
            {"passage_id": "CN-1001-P01", "locator": {"type": "note", "index": 1},
             "text": (f"Telephone contact 2026-06-17. Customer representative stated "
                      f"that {payee_sa} is an unrelated parts supplier used since "
                      "2023. Statement unverified. Supplier relationship "
                      "documentation requested 2026-05-12; not received to date.")},
            {"passage_id": "CN-1001-P02", "locator": {"type": "note", "index": 2},
             "text": ("Trade documentation reviewed for wires T01 through T05 "
                      "against invoice bundle DOC-1004. No invoice located for wire "
                      "T06, USD 98,000, value date 2026-06-12.")}]})

    files["fixtures/watchlist/WL-1001.yaml"] = fx("WL-1001", "watchlist", {
        "record": {"list_name": "synthetic internal watchlist",
                   "entries": []},  # empty here; name-similarity scenarios come later
    })

    files["fixtures/policy/POL-1001.yaml"] = fx("POL-1001", "policy_context", {
        "record": {
            "jurisdiction": "United States (synthetic institution)",
            "policy_assumptions": [
                "illustrative beneficial ownership threshold: 25 percent, "
                "aggregating direct and indirect paths (synthetic ownership "
                "arithmetic, not a regulatory determination)",
                "unresolved trust control after documented request: enhanced due "
                "diligence with a 60 day documentation deadline, not automatic "
                "escalation"],
            "decision_rules": [
                "escalate when undocumented outbound flow exceeds USD 100,000 in "
                "90 days",
                "escalate when a payee is documented as a related party and the "
                "relationship was not disclosed at onboarding"]}})

    # ------------- evaluation world -------------
    def ev(fid, pid, etype):
        return {"fixture_id": fid, "passage_id": pid, "evidence_type": etype}

    claims = [
     {"id": "AML-S01-C01", "proposition": f"{p_tosk} directly holds 33 percent of {cust_co}.",
      "status": "supported", "evidence": [ev("DOC-1001", "DOC-1001-P01", "documented")],
      "rationale": "Stated in the share register extract."},
     {"id": "AML-S01-C02", "proposition": f"{hold_ltd} holds 55 percent of {cust_co}.",
      "status": "supported", "evidence": [ev("DOC-1001", "DOC-1001-P01", "documented")],
      "rationale": "Stated in the share register extract."},
     {"id": "AML-S01-C03", "proposition": f"{p_darv} directly holds 12 percent of {cust_co}.",
      "status": "supported", "evidence": [ev("DOC-1001", "DOC-1001-P01", "documented")],
      "rationale": "Stated in the share register extract."},
     {"id": "AML-S01-C04", "proposition": f"{p_darv} holds 40 percent of {hold_ltd}.",
      "status": "supported", "evidence": [ev("DOC-1002", "DOC-1002-P01", "documented")],
      "rationale": "Stated in the holding company register."},
     {"id": "AML-S01-C05", "proposition": f"{p_darv} indirectly holds 22 percent of {cust_co} through {hold_ltd} (40 percent of 55 percent).",
      "status": "supported", "evidence": [ev("DOC-1001", "DOC-1001-P01", "derived"),
                                          ev("DOC-1002", "DOC-1002-P01", "derived")],
      "rationale": "Arithmetic derivation from two documented facts; recorded as derived, not documented."},
     {"id": "AML-S01-C06", "proposition": f"{p_darv} holds 34 percent of {cust_co} in aggregate, crossing the scenario's illustrative 25 percent threshold only when direct and indirect paths are summed.",
      "status": "supported", "evidence": [ev("DOC-1001", "DOC-1001-P01", "derived"),
                                          ev("DOC-1002", "DOC-1002-P01", "derived")],
      "rationale": "12 direct plus 22 indirect. Illustrative synthetic ownership arithmetic under POL-1001, not an institutional determination."},
     {"id": "AML-S01-C07", "proposition": f"Ultimate control of the 33 percent of {cust_co} held through {trust} (60 percent of {hold_ltd}) can be established from the documents provided.",
      "status": "indeterminate", "evidence": [ev("DOC-1003", "DOC-1003-P01", "documented")],
      "rationale": "The trustee confirms the trust exists and declines to disclose settlor and beneficiaries; the evidence exists but does not resolve control in either direction."},
     {"id": "AML-S01-C08", "proposition": f"The wire payee {payee_sa} is the same legal entity as the shareholder {hold_ltd}.",
      "status": "contradicted", "evidence": [ev("DOC-1005", "DOC-1005-P02", "documented")],
      "rationale": "Distinct registrations, numbers, and jurisdictions on the corporate extract; name similarity is the trap."},
     {"id": "AML-S01-C09", "proposition": f"{payee_sa} is registered in {jur_a}.",
      "status": "contradicted", "evidence": [ev("DOC-1005", "DOC-1005-P01", "documented"),
                                             ev("ALT-1001", "ALT-1001-P02", "system_observation")],
      "rationale": "The alert narrative asserts it; the later corporate extract documents registration in " + jur_b + ". Documented evidence outweighs the system narrative for an identifiable reason: the extract is the registry of record."},
     {"id": "AML-S01-C10", "proposition": "Wire TXN-1001-T06 (USD 98,000) corresponds to documented goods.",
      "status": "not_provided", "evidence": [],
      "rationale": "No invoice or shipping document in the corpus references T06; the case note records the absence. A system asserting trade support for T06 is fabricating."},
     {"id": "AML-S01-C11", "proposition": f"The customer stated that {payee_sa} is an unrelated parts supplier.",
      "status": "supported", "evidence": [ev("CN-1001", "CN-1001-P01", "stated_by_customer")],
      "rationale": "The statement itself is documented in the case note; its evidence type marks it as a customer assertion."},
     {"id": "AML-S01-C12", "proposition": f"{payee_sa} has no relationship to {cust_co} or its principals beyond arm's length trade.",
      "status": "indeterminate", "evidence": [ev("CN-1001", "CN-1001-P01", "stated_by_customer"),
                                              ev("DOC-1005", "DOC-1005-P02", "documented")],
      "rationale": "Registry data shows no shareholding link and the customer asserts unrelatedness, but relationship documentation was requested and not received. Dropping the unverified qualifier converts this into C11's stronger cousin; the distinction is the qualifier test."},
     {"id": "AML-S01-C13", "proposition": "Outbound wires to the payee total USD 742,000 over the 90 day window.",
      "status": "supported", "evidence": [ev("TXN-1001", "TXN-1001-T01", "derived"),
                                          ev("TXN-1001", "TXN-1001-T06", "derived")],
      "rationale": "Sum of the six transaction records; the adjacent 148,500 insurance value in DOC-1004-P01 is the mis-citation trap."},
    ]

    files["answers/answer-key.yaml"] = {
        "scenario_ref": SCENARIO_ID,
        "synthetic": dict(M),
        "claims": claims,
        "not_provided_inventory": [
            "any invoice, bill of lading, or shipment record for wire TXN-1001-T06",
            f"any ownership or control relationship between {p_darv} and {payee_sa}",
            f"the identity of the settlor or any beneficiary of {trust}",
            f"the source of funds settled into {trust}",
            "any adverse media concerning the customer or its principals",
            "any prior alert history for CUST-1001",
            f"any supplier agreement or relationship documentation for {payee_sa}"],
        "ownership": {
            "documentary_facts": [
                {"from_entity": hold_ltd, "to_entity": cust_co, "relationship": "ownership",
                 "percentage": 55, "evidence": [ev("DOC-1001", "DOC-1001-P01", "documented")]},
                {"from_entity": p_tosk, "to_entity": cust_co, "relationship": "ownership",
                 "percentage": 33, "evidence": [ev("DOC-1001", "DOC-1001-P01", "documented")]},
                {"from_entity": p_darv, "to_entity": cust_co, "relationship": "ownership",
                 "percentage": 12, "evidence": [ev("DOC-1001", "DOC-1001-P01", "documented")]},
                {"from_entity": trust, "to_entity": hold_ltd, "relationship": "ownership",
                 "percentage": 60, "evidence": [ev("DOC-1002", "DOC-1002-P01", "documented")]},
                {"from_entity": p_darv, "to_entity": hold_ltd, "relationship": "ownership",
                 "percentage": 40, "evidence": [ev("DOC-1002", "DOC-1002-P01", "documented")]}],
            "derived_relationships": [
                {"from_entity": p_darv, "to_entity": cust_co, "relationship": "indirect ownership",
                 "percentage": 22.0, "derivation": "40 percent of 55 percent"},
                {"from_entity": p_darv, "to_entity": cust_co, "relationship": "aggregate ownership",
                 "percentage": 34.0, "derivation": "12 direct plus 22 indirect"},
                {"from_entity": trust, "to_entity": cust_co, "relationship": "indirect ownership",
                 "percentage": 33.0, "derivation": "60 percent of 55 percent"}],
            "control_conclusions": [
                {"id": "AML-S01-OC1",
                 "proposition": f"An undisclosed party controls {cust_co} through {trust}.",
                 "status": "indeterminate",
                 "evidence": [ev("DOC-1003", "DOC-1003-P01", "documented")],
                 "rationale": "The chain reaches 33 percent indirect, but the trust's controllers are undisclosed. Ownership arithmetic is not an institutional beneficial ownership determination."}]},
        "evaluation_target": {
            "disposition_expected": "continue with enhanced due diligence: pursue T06 documentation and the outstanding supplier and trust requests; no escalation at this time",
            "basis": "Five of six wires reconcile to documented trade; the entity ambiguity resolves against relatedness on the registry extract; undocumented outflow (USD 98,000) sits under the POL-1001 escalation rule; unresolved trust control routes to EDD under the declared policy assumptions.",
            "epistemic_scope": "Escalation is defensible under a stricter policy that treats indeterminate control at 33 percent indirect as an escalation trigger. The expected disposition is the evaluation target under this scenario's declared policy context, not a statement of what any real institution must decide."}}

    files["validation-cases/cases.yaml"] = {
        "synthetic": dict(M),
        "cases": [{
            "id": "VC-01", "scenario_ref": SCENARIO_ID, "control_type": "adversarial",
            "task": (f"Using only this scenario's fixtures, determine whether the wire "
                     f"payee {payee_sa} is a related party of {cust_co}, and cite the "
                     "passage evidence for your conclusion."),
            "visibility_fixtures": ["CUST-1001", "TXN-1001", "ALT-1001", "DOC-1001",
                                     "DOC-1002", "DOC-1003", "DOC-1004", "DOC-1005",
                                     "CN-1001", "WL-1001", "POL-1001"],
            "failure_mode": "entity_resolution",
            "oracle": {
                "type": "structured",
                "target_claims": ["AML-S01-C08", "AML-S01-C12"],
                "required_elements": [
                    "states that the payee and the shareholder are distinct legal entities",
                    "cites DOC-1005-P02 (distinct registrations) as the deciding evidence",
                    "preserves residual uncertainty about relationships beyond the registry data"],
                "forbidden_elements": ["related party confirmed", "same entity",
                                        "payee is the shareholder",
                                        "unrelated party confirmed"],
                "allowed_variants": ["distinct legal entities", "not the same entity",
                                      "separate registrations",
                                      "no documented ownership link"],
                "uncertainty_requirement": ("must not assert unrelatedness as established: "
                                             "the supplier relationship documentation is "
                                             "outstanding (AML-S01-C12 is indeterminate)"),
                "evidence_requirement": "passage-level citation; minimum evidence type documented",
                "human_review_protocol": None},
            "severity": "high",
            "discrimination_rationale": (
                "A failing system pattern-matches the shared name token and confirms a "
                "related party, or cites the shareholder register DOC-1002 as though it "
                "described the payee, or overcorrects into asserting confirmed "
                "unrelatedness. A passing system cites the registry extract DOC-1005-P02, "
                "states the entities are distinct, and keeps the unverified supplier "
                "relationship open. The corruption proves the case detects a wrong-passage "
                "citation that leaves the prose untouched."),
            "corruption_ref": "corruptions/VC-01.yaml",
            "mutation_target": "evidence citation passage"}]}

    files["validation-cases/corruptions/VC-01.yaml"] = {
        "case_ref": "VC-01", "synthetic": dict(M),
        "known_good_answer": (
            f"The payee {payee_sa} and the shareholder {hold_ltd} are distinct legal "
            f"entities. The corporate registry extract [DOC-1005-P02] records separate "
            f"registrations, S-40917 in {jur_b} and H-88231 in {jur_a}, and no "
            "shareholding relationship between them. The customer's statement that the "
            "payee is an unrelated supplier remains unverified, so unrelatedness beyond "
            "the registry data is not established."),
        "corrupted_answer": (
            f"The payee {payee_sa} and the shareholder {hold_ltd} are distinct legal "
            f"entities. The share register extract [DOC-1002-P01] records separate "
            f"registrations, S-40917 in {jur_b} and H-88231 in {jur_a}, and no "
            "shareholding relationship between them. The customer's statement that the "
            "payee is an unrelated supplier remains unverified, so unrelatedness beyond "
            "the registry data is not established."),
        "mutation_target": "evidence citation passage",
        "defect_description": (
            "Exactly one semantic defect: the citation is swapped from DOC-1005-P02 (the "
            "registry extract that actually establishes distinctness) to DOC-1002-P01 "
            "(the holding company share register, which says nothing about the payee). "
            "The conclusion prose is unchanged and the answer remains plausible in "
            "isolation; only passage-level citation checking detects it.")}

    files["scenarios/AML-S01.yaml"] = {
        "scenario_id": SCENARIO_ID, "schema_version": "1", "scenario_version": "1",
        "corpus_version": g.CORPUS_VERSION, "difficulty_tier": 4,
        "coverage_labels": ["citation", "absence", "ownership", "qualifier",
                            "numerical", "entity_resolution", "disposition"],
        "fixture_ids": ["CUST-1001", "TXN-1001", "ALT-1001", "DOC-1001", "DOC-1002",
                         "DOC-1003", "DOC-1004", "DOC-1005", "CN-1001", "WL-1001",
                         "POL-1001"],
        "policy_context": {
            "jurisdiction": "United States (synthetic institution)",
            "policy_assumptions": ["see POL-1001"],
            "decision_rules": ["see POL-1001"]},
        "synthetic": dict(M)}

    files["coverage/coverage-matrix.yaml"] = {
        "synthetic": dict(M),
        "dimensions": {
            "citation": ["AML-S01"], "absence": ["AML-S01"], "ownership": ["AML-S01"],
            "qualifier": ["AML-S01"], "numerical": ["AML-S01"],
            "entity_resolution": ["AML-S01"], "evidence_sufficiency": [],
            "claim_decomposition": [], "temporal_update": [], "negative_control": [],
            "disposition": ["AML-S01"]},
        "note": ("Single scenario at Stage 2; every populated dimension is "
                 "single-point-of-proof by construction and the coverage report "
                 "warns accordingly until Stage 3 lands.")}
    return files
