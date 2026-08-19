# SPDX-License-Identifier: Apache-2.0
"""Pydantic models are the single source of truth for corpus artifact shapes.
schemas/*.schema.json are generated from these models by gen_schemas.py, so
the published JSON Schemas and the runtime validator cannot drift apart.
Tradeoff (DD-011): a hand-written JSON Schema could express a few constraints
pydantic cannot, but two normative sources would eventually disagree, and a
corpus about evidence discipline should not carry that risk."""
from __future__ import annotations
from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict

MARKER = "REGEVAL_SYNTHETIC"

EpistemicStatus = Literal["supported", "contradicted", "not_provided", "indeterminate"]
EvidenceType = Literal["documented", "stated_by_customer", "system_observation",
                       "analyst_observation", "derived", "unverified"]
FailureMode = Literal["citation_fabrication", "unsupported_claim", "qualifier_loss",
                      "numerical_error", "entity_resolution", "ownership_error",
                      "evidence_insufficiency", "over_refusal", "under_refusal"]
ControlType = Literal["positive", "negative", "adversarial"]
OracleType = Literal["exact", "set_membership", "structured", "semantic", "human_review"]
Severity = Literal["low", "medium", "high"]

class Base(BaseModel):
    model_config = ConfigDict(extra="forbid")

class SyntheticMark(Base):
    marker: Literal["REGEVAL_SYNTHETIC"]
    corpus_version: str

class FixtureHeader(Base):
    """Every observable fixture carries exactly these identity fields.
    Isolation rule: no field in any fixture model may carry evaluation-world
    content; test_isolation.py enforces the forbidden-field list."""
    fixture_id: str
    fixture_type: Literal["customer", "transaction_set", "alert", "document",
                          "case_note", "watchlist", "policy_context"]
    scenario_ref: str
    synthetic: SyntheticMark

class Passage(Base):
    passage_id: str
    locator: dict
    text: str

class DocumentFixture(FixtureHeader):
    title: str
    doc_date: str            # within the synthetic reference-date frame
    passages: list[Passage]

class EvidenceRef(Base):
    fixture_id: str
    passage_id: str
    evidence_type: EvidenceType

class Claim(Base):
    id: str
    proposition: str          # atomic: decompose whenever portions could differ in status
    status: EpistemicStatus
    evidence: list[EvidenceRef] = Field(default_factory=list)
    rationale: str

class OwnershipEdge(Base):
    from_entity: str
    to_entity: str
    relationship: str
    percentage: Optional[float] = None
    evidence: list[EvidenceRef]

class OwnershipModel(Base):
    documentary_facts: list[OwnershipEdge]
    derived_relationships: list[dict]
    control_conclusions: list[Claim]

class PolicyContext(Base):
    jurisdiction: str
    policy_assumptions: list[str]
    decision_rules: list[str]

class EvaluationTarget(Base):
    disposition_expected: str
    basis: str
    epistemic_scope: str

class Scenario(Base):
    scenario_id: str
    schema_version: str
    scenario_version: str
    corpus_version: str
    difficulty_tier: int = Field(ge=1, le=5)
    coverage_labels: list[str]
    fixture_ids: list[str]
    policy_context: PolicyContext
    synthetic: SyntheticMark

class AnswerKey(Base):
    scenario_ref: str
    claims: list[Claim]
    not_provided_inventory: list[str]
    ownership: Optional[OwnershipModel] = None
    evaluation_target: EvaluationTarget

class Oracle(Base):
    type: OracleType
    target_claims: list[str]
    required_elements: list[str]
    forbidden_elements: list[str]
    allowed_variants: list[str]
    uncertainty_requirement: Optional[str] = None
    evidence_requirement: Optional[str] = None
    human_review_protocol: Optional[dict] = None

class ValidationCase(Base):
    id: str
    scenario_ref: str
    control_type: ControlType
    task: str
    visibility_fixtures: list[str]
    failure_mode: FailureMode
    oracle: Oracle
    severity: Severity
    discrimination_rationale: str
    corruption_ref: str
    mutation_target: str

class Corruption(Base):
    case_ref: str
    known_good_answer: str
    corrupted_answer: str
    mutation_target: str
    defect_description: str   # exactly one semantic defect; plausible in isolation

class ManifestEntry(Base):
    path: str
    sha256: str
    bytes: int

class Manifest(Base):
    corpus_id: str
    corpus_version: str
    generator_version: str
    schema_version: str
    seed: int
    environment: dict
    files: list[ManifestEntry]   # canonical artifact set; never includes the manifest itself

SCHEMAS = {"scenario": Scenario, "claim": Claim, "evidence": EvidenceRef,
           "ownership": OwnershipModel, "validation-case": ValidationCase,
           "corruption": Corruption, "manifest": Manifest,
           "fixture-document": DocumentFixture, "fixture-header": FixtureHeader,
           "answer-key": AnswerKey}


def canonical_schema(model) -> dict:
    """Emit a JSON Schema that is stable across pydantic minor versions.

    Pydantic changed Literal rendering between releases: some versions emit
    `const` alone, others emit `const` plus a single-value `enum`. Committing
    raw output made the checked-in schema reproducible only under one exact
    library build, so a reviewer on a different pydantic saw a false drift
    failure (DD-021). Normalizing removes the redundancy in both directions.
    """
    def norm(node):
        if isinstance(node, dict):
            out = {k: norm(v) for k, v in node.items()}
            if "const" in out and out.get("enum") == [out["const"]]:
                out.pop("enum")
            return out
        if isinstance(node, list):
            return [norm(v) for v in node]
        return node
    return norm(model.model_json_schema())
