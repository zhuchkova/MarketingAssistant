#python scripts/seed_chroma_cta_conversion.py
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="cta_conversion_knowledge")

documents = [
    "CTA pattern: Comment [keyword] and I will send you [resource]. Best for lead magnets and Instagram/LinkedIn engagement.",
    "CTA pattern: DM me [keyword] if you want the checklist/template/framework.",
    "CTA pattern: Save this post if you want to implement it later.",
    "CTA pattern: Comment with your biggest challenge and I will suggest the next step.",
    "CTA pattern: If you want the full workflow, comment [keyword].",
    "Conversion principle: A good CTA should be specific, low-friction, and directly connected to the post promise.",
    "Conversion principle: The trigger keyword should be short, memorable, and related to the topic.",
]

metadatas = [
    {"type": "cta_pattern", "goal": "comment"},
    {"type": "cta_pattern", "goal": "dm_keyword"},
    {"type": "cta_pattern", "goal": "save"},
    {"type": "cta_pattern", "goal": "comment"},
    {"type": "cta_pattern", "goal": "download"},
    {"type": "principle", "goal": "conversion"},
    {"type": "principle", "goal": "manychat"},
]

ids = [f"cta_{i}" for i in range(len(documents))]

collection.add(documents=documents, metadatas=metadatas, ids=ids)

print("cta_conversion_knowledge seeded")