from __future__ import annotations

import json
import os
from typing import List, Dict

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import settings


class RetrieverService:
    def __init__(self) -> None:
        self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.index_path = settings.kb_index_path
        self.meta_path = settings.kb_meta_path
        self.dim = 384
        self.index = self._load_or_create_index()
        self.meta = self._load_meta()

    def _load_or_create_index(self):
        if os.path.exists(self.index_path):
            return faiss.read_index(self.index_path)
        return faiss.IndexFlatIP(self.dim)

    def _load_meta(self) -> List[Dict]:
        if os.path.exists(self.meta_path):
            with open(self.meta_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, ensure_ascii=False, indent=2)

    def add_document(self, title: str, source: str, content: str, tags=None):
        emb = self.embedder.encode([content], normalize_embeddings=True)
        self.index.add(np.array(emb, dtype=np.float32))
        self.meta.append({"title": title, "source": source, "content": content, "tags": tags or []})
        self._save()

    def retrieve(self, query: str, k: int = 4):
        if self.index.ntotal == 0:
            return []
        q = self.embedder.encode([query], normalize_embeddings=True)
        scores, ids = self.index.search(np.array(q, dtype=np.float32), k)
        out = []
        for score, idx in zip(scores[0], ids[0]):
            if idx < 0 or idx >= len(self.meta):
                continue
            row = self.meta[idx]
            out.append({
                "title": row["title"],
                "source": row["source"],
                "snippet": row["content"][:350],
                "score": float(score),
            })
        return out
