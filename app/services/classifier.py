from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Classification:
    label: str
    confidence: float


class BertClassifierService:
    """Drop-in interface for a fine-tuned BERT classifier.

    Replace `predict` internals with your exported transformer pipeline.
    """

    suspicious_terms = {"hoax", "secret", "cover-up", "miracle", "cure", "fake"}
    trust_terms = {"according to", "official", "report", "study", "data"}

    def predict(self, claim: str) -> Classification:
        text = claim.lower()
        sus = sum(1 for t in self.suspicious_terms if t in text)
        trust = sum(1 for t in self.trust_terms if t in text)

        if sus > trust:
            return Classification(label="likely_false", confidence=min(0.65 + 0.08 * sus, 0.93))
        if trust > sus:
            return Classification(label="likely_true", confidence=min(0.62 + 0.08 * trust, 0.91))
        return Classification(label="uncertain", confidence=0.52)
