from chroma_seed_utils import seed_collection


count = seed_collection("cta_patterns", "cta_patterns.json")
print(f"cta_patterns: upserted {count} documents")
