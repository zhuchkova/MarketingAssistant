from chroma_seed_utils import seed_collection


count = seed_collection("cta_conversion_knowledge", "cta_conversion_knowledge.json")
print(f"cta_conversion_knowledge: upserted {count} documents")
