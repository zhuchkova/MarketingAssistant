from chroma_seed_utils import seed_collection


count = seed_collection("content_frameworks", "content_frameworks.json")
print(f"content_frameworks: upserted {count} documents")
