from __future__ import annotations

from typing import Tuple

from openai import OpenAI

from app.config import settings


class VerifierService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def verify(self, claim: str, evidence: list[dict]) -> Tuple[str, str]:
        if not settings.use_openai or not self.client:
            return self._fallback_verify(claim, evidence)

        ev_block = "\n\n".join([f"- {e['title']} ({e['source']}): {e['snippet']}" for e in evidence])
        prompt = (
            "You are a fact-checking assistant. Given claim and evidence, produce a verdict "
            "(supported, refuted, or inconclusive) and concise explanation.\n"
            f"Claim: {claim}\nEvidence:\n{ev_block}"
        )
        resp = self.client.responses.create(model=settings.openai_model, input=prompt)
        text = resp.output_text.strip()
        lower = text.lower()
        verdict = "inconclusive"
        if "supported" in lower:
            verdict = "supported"
        elif "refuted" in lower:
            verdict = "refuted"
        return verdict, text

    def _fallback_verify(self, claim: str, evidence: list[dict]) -> Tuple[str, str]:
        if not evidence:
            return "inconclusive", "No evidence found in local knowledge base."
        c = claim.lower()
        score = 0
        for e in evidence:
            s = e["snippet"].lower()
            for tok in c.split()[:8]:
                if len(tok) > 4 and tok in s:
                    score += 1
        if score >= 4:
            return "supported", "Retrieved sources substantially overlap with key claim terms."
        if score <= 1:
            return "refuted", "Retrieved sources do not align with claim phrasing and context."
        return "inconclusive", "Available evidence is mixed; manual review recommended."
