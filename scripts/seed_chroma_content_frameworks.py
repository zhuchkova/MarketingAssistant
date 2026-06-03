#python scripts/seed_chroma_content_frameworks.py
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="content_frameworks"
)

documents = [
    "Framework: Problem -> Agitation -> Solution -> CTA",
    "Framework: Contrarian claim -> Explanation -> Example -> CTA",
    "Framework: Personal story -> Lesson learned -> Practical takeaway -> CTA",
    "Framework: Mistake -> Consequence -> Better approach -> CTA",
    "Framework: Hook -> Value -> Proof -> CTA",
    "Framework: Before -> After -> How -> CTA",
    "Framework: 3 mistakes -> Why they happen -> Fixes -> CTA",
    "Framework: Question -> Insight -> Actionable advice -> CTA",
    "Framework: Myth -> Reality -> Example -> CTA",
    "Framework: Step-by-step tutorial -> CTA"
]

metadatas = [
    {"type": "framework", "format": "educational"},
    {"type": "framework", "format": "contrarian"},
    {"type": "framework", "format": "story"},
    {"type": "framework", "format": "mistake"},
    {"type": "framework", "format": "authority"},
    {"type": "framework", "format": "transformation"},
    {"type": "framework", "format": "list"},
    {"type": "framework", "format": "question"},
    {"type": "framework", "format": "myth_busting"},
    {"type": "framework", "format": "how_to"},
]

ids = [f"framework_{i}" for i in range(len(documents))]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids,
)

print("Content_frameworks seeded")