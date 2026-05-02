from __future__ import annotations

import re
from statistics import mean

from app.config import settings
from app.models import AnalyzeResponse, ClaimResult, Evidence
from app.services.classifier import BertClassifierService
from app.services.retriever import RetrieverService
from app.services.verifier import VerifierService


class MisinformationPipeline:
    def __init__(self):
        self.classifier = BertClassifierService()
        self.retriever = RetrieverService()
        self.verifier = VerifierService()

    def extract_claims(self, text: str) -> list[str]:
        chunks = re.split(r"[\n\.!?]+", text)
        claims = [c.strip() for c in chunks if len(c.strip()) > 25]
        return claims[:5] or [text.strip()]

    def analyze(self, text: str) -> AnalyzeResponse:
        claims = self.extract_claims(text)
        outputs = []
        confidences = []

        for claim in claims:
            c = self.classifier.predict(claim)
            routed = c.confidence < settings.confidence_threshold
            evidence = self.retriever.retrieve(claim, k=4) if routed else []

            if routed:
                verdict, explanation = self.verifier.verify(claim, evidence)
            else:
                verdict = "supported" if c.label == "likely_true" else "refuted" if c.label == "likely_false" else "inconclusive"
                explanation = "High-confidence classifier verdict; verification not required by router."

            outputs.append(
                ClaimResult(
                    claim=claim,
                    classifier_label=c.label,
                    classifier_confidence=round(c.confidence, 3),
                    routed_to_verifier=routed,
                    final_verdict=verdict,
                    explanation=explanation,
                    evidence=[Evidence(**e) for e in evidence],
                )
            )
            confidences.append(c.confidence)

        overall = "inconclusive"
        labels = [o.final_verdict for o in outputs]
        if labels.count("refuted") > labels.count("supported"):
            overall = "likely_misinformation"
        elif labels.count("supported") > labels.count("refuted"):
            overall = "likely_factual"

        return AnalyzeResponse(overall_label=overall, confidence=round(mean(confidences), 3), claims=outputs)
