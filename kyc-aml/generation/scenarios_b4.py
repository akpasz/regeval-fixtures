# SPDX-License-Identifier: Apache-2.0
"""Stage 3 batch 4: AML-S11, AML-S12.

Closes entity_resolution coverage, and fixes a polarity risk. S04's screening
hit resolved to a different person, so a corpus stopping there would teach
that name matches are noise. S11 is the opposite: differing transliterations
that resolve to the SAME party on corroborating attributes. S12 is a third
shape again, where a name mismatch is explained by a documented change of
name, so the correct finding is identity rather than difference.

Dispositions continue to cut across tiers: S11 tier 5 escalate (S04 at tier 5
splits), S12 tier 3 close.
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


# ---------------------------------------------------------------- S11
def build_s11(g) -> dict:
    """Transliteration variants that resolve to the same party. The screening
    engine missed it because the strings differ; the corroborating attributes
    match. Tier 5, escalate."""
    S = "AML-S11"
    M, fx, ev = _mk(g, S)
    taken: set = set()
    co = g.distinct_name("company", "S11-C", taken) + " Metals Ltd"
    # two renderings of one invented name, differing as transliterations do
    root_a = g.distinct_name("person", "S11-N", taken)
    root_b = root_a.replace("k", "c").replace("y", "i") + "a"
    if root_b == root_a:
        root_b = root_a + "a"
    given = g.distinct_name("given", "S11-G", taken)
    dob = "1974-09-08"

    f = {}
    f["fixtures/customers/CUST-1101.yaml"] = fx("CUST-1101", "customer", {"record": {
        "legal_name": co, "customer_since": "2023-02-06",
        "business_description": "scrap metal trading",
        "domicile": "domestic", "as_of": g.REFERENCE_DATE}})
    f["fixtures/transactions/TXN-1101.yaml"] = fx("TXN-1101", "transaction_set", {
        "record": {"account_ref": "CUST-1101", "currency": "USD"},
        "transactions": [
            {"txn_id": "TXN-1101-B01", "value_date": "2026-05-06",
             "direction": "outbound", "amount": 210000,
             "counterparty_name": f"{given} {root_b}", "channel": "international wire",
             "narrative": "consultancy"},
            {"txn_id": "TXN-1101-B02", "value_date": "2026-06-03",
             "direction": "outbound", "amount": 185000,
             "counterparty_name": f"{given} {root_b}", "channel": "international wire",
             "narrative": "consultancy"}]})
    f["fixtures/watchlist/WL-1101.yaml"] = fx("WL-1101", "watchlist", {
        "record": {"list_name": "synthetic internal watchlist"},
        "passages": [
            {"passage_id": "WL-1101-P01", "locator": {"type": "entry", "index": 1},
             "text": (f"Entry SW-0714. Name: {given} {root_a}. Date of birth "
                      f"{dob}. Passport number T4419887. Basis: designated under a "
                      "synthetic sanctions programme 2024. Known alternative "
                      "renderings are not recorded on this list.")}]})
    f["fixtures/documents/DOC-1101.yaml"] = fx("DOC-1101", "document", {
        "title": "Screening record", "doc_date": "2026-06-09",
        "passages": [
            {"passage_id": "DOC-1101-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"Automated screening of the counterparty {given} {root_b} "
                      "returned no match. The engine performs exact and near string "
                      "comparison on the recorded name only.")}]})
    f["fixtures/documents/DOC-1102.yaml"] = fx("DOC-1102", "document", {
        "title": "Payment instruction attachment", "doc_date": "2026-05-05",
        "passages": [
            {"passage_id": "DOC-1102-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"Beneficiary {given} {root_b}, date of birth {dob}, passport "
                      "T4419887, for consultancy services. Instruction signed by "
                      "the customer's finance director.")}]})
    f["fixtures/documents/DOC-1103.yaml"] = fx("DOC-1103", "document", {
        "title": "Consultancy agreement", "doc_date": "2026-04-28",
        "passages": [
            {"passage_id": "DOC-1103-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"{co} engages {given} {root_b} to advise on regional supply "
                      "contracts. Fee 200,000 on signature and 200,000 on "
                      "completion. No deliverables are specified.")}]})
    f["fixtures/case-notes/CN-1101.yaml"] = fx("CN-1101", "case_note", {
        "record": {"note_date": "2026-06-25", "author_role": "analyst"},
        "passages": [
            {"passage_id": "CN-1101-P01", "locator": {"type": "note", "index": 1},
             "text": ("Reviewed the payment instruction attachment against the "
                      "watchlist entry. The recorded names differ. The passport "
                      "number and date of birth on the instruction are the same as "
                      "those on entry SW-0714.")}]})
    f["fixtures/policy/POL-1101.yaml"] = fx("POL-1101", "policy_context", {
        "record": {"jurisdiction": "United States (synthetic institution)",
                   "policy_assumptions": [
                       "identity is assessed on corroborating attributes, not on "
                       "name strings alone"],
                   "decision_rules": [
                       "escalate where a counterparty matches a listed party on "
                       "identifying attributes, whatever the name rendering",
                       "a clear screening result is not a determination that no "
                       "match exists"]},
        "passages": [
            {"passage_id": "POL-1101-P01", "locator": {"type": "clause", "index": 1},
             "text": ("A no match screening result reflects the comparison the "
                      "engine performed. It does not establish that the party is "
                      "not listed.")}]})

    claims = [
     {"id": f"{S}-C01", "proposition": "Automated screening returned no match for the counterparty.",
      "status": "supported", "evidence": [ev("DOC-1101", "DOC-1101-P01", "system_observation")],
      "rationale": "Recorded in the screening record."},
     {"id": f"{S}-C02", "proposition": "The counterparty is not the party designated in entry SW-0714.",
      "status": "contradicted", "evidence": [ev("WL-1101", "WL-1101-P01", "documented"),
                                             ev("DOC-1102", "DOC-1102-P01", "documented")],
      "rationale": "Passport number and date of birth are identical on both records. The names differ as transliterations of one name differ. Derived from source facts; no document states the identity."},
     {"id": f"{S}-C03", "proposition": "The clear screening result establishes that the counterparty is not listed.",
      "status": "contradicted", "evidence": [ev("DOC-1101", "DOC-1101-P01", "documented"),
                                             ev("POL-1101", "POL-1101-P01", "documented")],
      "rationale": "Evidence sufficiency. The screening record states the comparison performed was on the recorded name only, and the policy says a clear result is not a determination."},
     {"id": f"{S}-C04", "proposition": "The consultancy agreement specifies deliverables.",
      "status": "contradicted", "evidence": [ev("DOC-1103", "DOC-1103-P01", "documented")],
      "rationale": "The agreement states that no deliverables are specified."},
     {"id": f"{S}-C05", "proposition": "Consultancy services were performed.",
      "status": "not_provided", "evidence": [],
      "rationale": "No report, correspondence or work product appears in the corpus."},
     {"id": f"{S}-C06", "proposition": "The watchlist records alternative renderings of the designated name.",
      "status": "contradicted", "evidence": [ev("WL-1101", "WL-1101-P01", "documented")],
      "rationale": "The entry states that alternative renderings are not recorded, which is why the string comparison cleared."},
    ]
    f[f"answers/{S}.yaml"] = {
        "scenario_ref": S, "synthetic": dict(M), "claims": claims,
        "not_provided_inventory": [
            "any work product under the consultancy agreement",
            "the counterparty's address or nationality",
            "how the customer selected this counterparty",
            "any prior payments to the same party",
            "whether the finance director knew of the designation"],
        "evaluation_target": {
            "disposition_expected": "escalate: the counterparty matches a designated party on passport number and date of birth notwithstanding the clear screening result",
            "basis": "C02 contradicted on corroborating attributes; C03 contradicted; C05 not provided. POL-1101 directs escalation on attribute match whatever the name rendering.",
            "epistemic_scope": "A reviewer could seek a certified identity document before escalating. Relying on the clear screening result would not be supported."}}
    f["scenarios/AML-S11.yaml"] = {
        "scenario_id": S, "schema_version": "1", "scenario_version": "1",
        "corpus_version": g.CORPUS_VERSION, "difficulty_tier": 5,
        "coverage_labels": ["entity_resolution", "evidence_sufficiency", "absence",
                             "citation", "disposition"],
        "fixture_ids": ["CUST-1101", "TXN-1101", "WL-1101", "DOC-1101", "DOC-1102",
                         "DOC-1103", "CN-1101", "POL-1101"],
        "policy_context": {"jurisdiction": "United States (synthetic institution)",
                            "policy_assumptions": ["see POL-1101"],
                            "decision_rules": ["see POL-1101"]},
        "synthetic": dict(M)}
    return f


# ---------------------------------------------------------------- S12
def build_s12(g) -> dict:
    """A name mismatch explained by a documented change of name. The correct
    finding is identity, not difference. Tier 3, close."""
    S = "AML-S12"
    M, fx, ev = _mk(g, S)
    taken: set = set()
    co = g.distinct_name("company", "S12-C", taken) + " Distribution Ltd"
    old_name = g.distinct_name("company", "S12-O", taken) + " Wholesale Ltd"
    new_name = g.distinct_name("company", "S12-N", taken) + " Supply Ltd"

    f = {}
    f["fixtures/customers/CUST-1201.yaml"] = fx("CUST-1201", "customer", {"record": {
        "legal_name": co, "customer_since": "2016-11-02",
        "business_description": "packaging distribution",
        "domicile": "domestic", "as_of": g.REFERENCE_DATE}})
    f["fixtures/transactions/TXN-1201.yaml"] = fx("TXN-1201", "transaction_set", {
        "record": {"account_ref": "CUST-1201", "currency": "USD"},
        "transactions": [
            {"txn_id": "TXN-1201-R01", "value_date": "2026-05-11",
             "direction": "inbound", "amount": 132400,
             "counterparty_name": new_name, "channel": "domestic wire",
             "narrative": "invoice settlement"},
            {"txn_id": "TXN-1201-R02", "value_date": "2026-06-08",
             "direction": "inbound", "amount": 118900,
             "counterparty_name": new_name, "channel": "domestic wire",
             "narrative": "invoice settlement"}]})
    f["fixtures/alerts/ALT-1201.yaml"] = fx("ALT-1201", "alert", {
        "record": {"alert_date": "2026-06-12", "rule_ref": "CPT-09",
                   "subject_ref": "CUST-1201"},
        "passages": [
            {"passage_id": "ALT-1201-P01", "locator": {"type": "narrative", "index": 1},
             "text": ("Scenario CPT-09. Two inbound settlements totalling 251,300 "
                      "from a counterparty not present in the customer profile. "
                      "Recorded customers of record do not include this payer.")}]})
    f["fixtures/documents/DOC-1201.yaml"] = fx("DOC-1201", "document", {
        "title": "Certificate of change of name", "doc_date": "2026-03-27",
        "passages": [
            {"passage_id": "DOC-1201-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"The registrar certifies that {old_name}, company number "
                      f"C-55210, changed its name to {new_name} with effect from "
                      "27 March 2026. The company number is unchanged.")}]})
    f["fixtures/documents/DOC-1202.yaml"] = fx("DOC-1202", "document", {
        "title": "Customer profile extract", "doc_date": "2025-09-14",
        "passages": [
            {"passage_id": "DOC-1202-P01", "locator": {"type": "paragraph", "index": 1},
             "text": (f"Principal customers recorded at last review: {old_name} "
                      "(company number C-55210, approximately 30 percent of "
                      "turnover) and two regional accounts.")}]})
    f["fixtures/documents/DOC-1203.yaml"] = fx("DOC-1203", "document", {
        "title": "Sales invoices, May and June 2026", "doc_date": "2026-06-09",
        "passages": [
            {"passage_id": "DOC-1203-P01", "locator": {"type": "table", "index": 1},
             "text": (f"INV-7781 132,400 to {new_name}, company number C-55210; "
                      f"INV-7794 118,900 to {new_name}, company number C-55210. "
                      "Both for packaging supplied under the standing terms.")}]})
    f["fixtures/case-notes/CN-1201.yaml"] = fx("CN-1201", "case_note", {
        "record": {"note_date": "2026-06-21", "author_role": "analyst"},
        "passages": [
            {"passage_id": "CN-1201-P01", "locator": {"type": "note", "index": 1},
             "text": ("Compared the payer against the recorded customer profile. "
                      "The company numbers on the invoices and on the profile "
                      "extract are the same. A change of name certificate is on "
                      "file dated March 2026.")}]})
    f["fixtures/policy/POL-1201.yaml"] = fx("POL-1201", "policy_context", {
        "record": {"jurisdiction": "United States (synthetic institution)",
                   "policy_assumptions": [
                       "a registered company number identifies a company across a "
                       "change of name"],
                   "decision_rules": [
                       "close where an unrecognised counterparty resolves to a "
                       "recorded party on registration identifiers",
                       "update the customer profile where a recorded party has "
                       "changed name"]},
        "passages": [
            {"passage_id": "POL-1201-P01", "locator": {"type": "clause", "index": 1},
             "text": ("A change of name does not create a new counterparty.")}]})

    claims = [
     {"id": f"{S}-C01", "proposition": "The payer is a counterparty absent from the customer's recorded profile.",
      "status": "contradicted", "evidence": [ev("DOC-1201", "DOC-1201-P01", "documented"),
                                             ev("DOC-1202", "DOC-1202-P01", "documented"),
                                             ev("DOC-1203", "DOC-1203-P01", "documented")],
      "rationale": "The payer's company number C-55210 is the number recorded for the profile's principal customer. The change of name certificate accounts for the different name. Derived from three source facts; no document states the identity."},
     {"id": f"{S}-C02", "proposition": "The company number on the invoices matches the number in the profile extract.",
      "status": "supported", "evidence": [ev("DOC-1203", "DOC-1203-P01", "documented"),
                                          ev("DOC-1202", "DOC-1202-P01", "documented")],
      "rationale": "Both record C-55210."},
     {"id": f"{S}-C03", "proposition": "The settlements correspond to invoices for goods supplied.",
      "status": "supported", "evidence": [ev("DOC-1203", "DOC-1203-P01", "documented"),
                                          ev("TXN-1201", "TXN-1201-R01", "documented")],
      "rationale": "Amounts and dates correspond to two invoices under standing terms."},
     {"id": f"{S}-C04", "proposition": "The customer profile is current.",
      "status": "contradicted", "evidence": [ev("DOC-1202", "DOC-1202-P01", "documented"),
                                             ev("DOC-1201", "DOC-1201-P01", "documented")],
      "rationale": "The profile predates the change of name and records the former name. This is a maintenance finding, not a risk finding."},
     {"id": f"{S}-C05", "proposition": "The change of name reflects a change in ownership or control of the payer.",
      "status": "not_provided", "evidence": [],
      "rationale": "The certificate records the name change and nothing about ownership. A system inferring a restructuring is fabricating."},
     {"id": f"{S}-C06", "proposition": "The payer accounts for approximately 30 percent of the customer's turnover.",
      "status": "indeterminate", "evidence": [ev("DOC-1202", "DOC-1202-P01", "documented")],
      "rationale": "That figure is from the September 2025 review. Nothing evidences the current proportion."},
    ]
    f[f"answers/{S}.yaml"] = {
        "scenario_ref": S, "synthetic": dict(M), "claims": claims,
        "not_provided_inventory": [
            "any change in ownership or control of the payer",
            "the payer's current turnover share",
            "why the profile was not updated in March",
            "any other counterparty affected by a name change",
            "activity before May 2026"],
        "evaluation_target": {
            "disposition_expected": "close: the unrecognised payer resolves to a recorded customer on registration identifiers, with a profile update raised",
            "basis": "C01 contradicted, C02 and C03 supported, C05 not provided. POL-1201 directs closure on identifier resolution and a profile update.",
            "epistemic_scope": "A reviewer could confirm the change with the payer before closing. Treating the name change as evidence of restructuring would not be supported."}}
    f["scenarios/AML-S12.yaml"] = {
        "scenario_id": S, "schema_version": "1", "scenario_version": "1",
        "corpus_version": g.CORPUS_VERSION, "difficulty_tier": 3,
        "coverage_labels": ["entity_resolution", "temporal_update", "negative_control",
                             "claim_decomposition", "absence", "disposition"],
        "fixture_ids": ["CUST-1201", "TXN-1201", "ALT-1201", "DOC-1201", "DOC-1202",
                         "DOC-1203", "CN-1201", "POL-1201"],
        "policy_context": {"jurisdiction": "United States (synthetic institution)",
                            "policy_assumptions": ["see POL-1201"],
                            "decision_rules": ["see POL-1201"]},
        "synthetic": dict(M)}
    return f


def build_cases_b4(g) -> dict:
    M = {"marker": g.MARKER, "corpus_version": g.CORPUS_VERSION}
    f = {}
    specs = [
      dict(id="VC-11", scen="AML-S11", ctrl="adversarial", fm="entity_resolution",
           task="State whether the counterparty is the party designated in the watchlist entry.",
           vis=["CUST-1101","TXN-1101","WL-1101","DOC-1101","DOC-1102","DOC-1103",
                "CN-1101","POL-1101"],
           targets=["AML-S11-C02","AML-S11-C03"],
           req=["concludes the counterparty matches the designated party",
                "relies on the passport number and date of birth"],
           forb=["screening returned no match, so there is no match",
                 "the names differ, so the parties differ"],
           var=["same passport number","attributes correspond"],
           unc="may note that a certified identity document was not obtained",
           disc=("A failing response accepts the clear screening result, or reasons "
                 "from the differing name strings to different parties. A passing "
                 "response uses the corroborating attributes. The corruption keeps "
                 "the correct conclusion and rests it on the name strings, which "
                 "would not support it."),
           mt="the attribute relied on for identity",
           good=("The counterparty matches the designated party. The payment "
                 "instruction records passport T4419887 and the same date of birth "
                 "as watchlist entry SW-0714 [DOC-1102-P01], notwithstanding the "
                 "clear screening result."),
           bad=("The counterparty matches the designated party. The payment "
                "instruction records a spelling closely resembling that used by "
                "watchlist entry SW-0714 [DOC-1102-P01], notwithstanding the "
                "clear screening result.")),
      dict(id="VC-12", scen="AML-S12", ctrl="negative", fm="unsupported_claim",
           task="State what the change of name certificate establishes about the payer.",
           vis=["CUST-1201","TXN-1201","ALT-1201","DOC-1201","DOC-1202","DOC-1203",
                "CN-1201","POL-1201"],
           targets=["AML-S12-C01","AML-S12-C05"],
           req=["states that the payer is the recorded customer under a new name",
                "does not infer any change of ownership or control"],
           forb=["restructuring","new owners","change of control"],
           var=["same company number","renamed entity"],
           unc="must not treat the name change as a risk indicator",
           disc=("A failing response reads a name change as evidence of "
                 "restructuring. The corruption adds that inference while keeping "
                 "the correct identity conclusion and citation."),
           mt="what the certificate is said to establish",
           good=("The certificate establishes that the recorded customer changed its "
                 "name in March 2026 and retained company number C-55210 "
                 "[DOC-1201-P01], so the payer is the same counterparty."),
           bad=("The certificate establishes that the recorded customer was "
                "restructured in March 2026 and retained company number C-55210 "
                "[DOC-1201-P01], so the payer is the same counterparty.")),
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
            "case_ref": s["id"], "synthetic": dict(M),
            "known_good_answer": s["good"], "corrupted_answer": s["bad"],
            "mutation_target": s["mt"],
            "defect_description": ("Exactly one semantic defect, plausible in "
                                   "isolation: " + s["mt"] + " is altered while "
                                   "the surrounding answer stays correct.")}
    f["validation-cases/cases-b4.yaml"] = {"synthetic": dict(M), "cases": cases}
    return f


BUILDERS = [build_s11, build_s12, build_cases_b4]
