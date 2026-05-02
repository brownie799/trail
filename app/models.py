from typing import List, Optional
from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    text: str


class Evidence(BaseModel):
    title: str
    source: str
    snippet: str
    score: float


class ClaimResult(BaseModel):
    claim: str
    classifier_label: str
    classifier_confidence: float
    routed_to_verifier: bool
    final_verdict: str
    explanation: str
    evidence: List[Evidence]


class AnalyzeResponse(BaseModel):
    overall_label: str
    confidence: float
    claims: List[ClaimResult]


class KBAddRequest(BaseModel):
    title: str
    source: str
    content: str
    tags: Optional[list[str]] = None
