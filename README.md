# Hybrid Retrieval-Augmented Multi-Agent Misinformation Detection System

A complete full-stack application for misinformation detection with:

- **Fast path**: BERT-style classifier interface (with pluggable local/remote models)
- **Confidence routing**: low-confidence claims are escalated
- **RAG verification**: FAISS retrieval over curated evidence + LLM reasoning
- **Multi-agent pipeline**: claim extraction, retrieval, verification, reporting
- **FastAPI backend** + **high-quality frontend**

## Architecture

1. **Claim Extraction Agent**: identifies one or more verifiable claims from user input.
2. **Classifier Agent**: predicts `true / false / uncertain` + confidence.
3. **Router Agent**: if confidence < threshold, trigger retrieval + LLM verification.
4. **Retrieval Agent**: embeds claims and fetches top evidence from FAISS.
5. **Verification Agent**: uses LLM with retrieved evidence to produce verdict and rationale.
6. **Report Agent**: composes transparent final report with source snippets.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/build_kb.py
uvicorn app.main:app --reload
```

Open: `http://127.0.0.1:8000`

## Environment variables

- `OPENAI_API_KEY` - optional, enables GPT verification agent.
- `OPENAI_MODEL` - defaults to `gpt-4o-mini`.
- `CONFIDENCE_THRESHOLD` - defaults to `0.78`.
- `USE_OPENAI` - `true/false`.

## API

- `POST /api/analyze`
- `POST /api/kb/add`
- `GET /api/health`

## Notes

- The classifier is provided as a **production-ready interface** with a heuristic fallback, so you can plug in a fine-tuned BERT checkpoint immediately.
- `scripts/train_classifier.py` shows how to train and export a transformer model for drop-in use.
