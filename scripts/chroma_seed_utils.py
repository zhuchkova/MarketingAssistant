import json
from pathlib import Path
from typing import Dict, List

import chromadb


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "rag_seed_data"
CHROMA_PATH = ROOT / "chroma_db"


def load_records(data_path: str) -> List[Dict]:
    path = DATA_DIR / data_path
    files = sorted(path.glob("*.json")) if path.is_dir() else [path]

    records = []
    for file in files:
        records.extend(json.loads(file.read_text(encoding="utf-8")))

    return records


def seed_collection(collection_name: str, data_path: str) -> int:
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(name=collection_name)

    records = load_records(data_path)
    ids = [record["id"] for record in records]
    documents = [record["document"] for record in records]
    metadatas = [record.get("metadata", {}) for record in records]

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

    return len(records)
