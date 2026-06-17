from chroma_seed_utils import seed_collection


COLLECTIONS = [
    ("positioning_knowledge", "positioning_knowledge"),
    ("idea_knowledge", "idea_knowledge.json"),
    ("content_frameworks", "content_frameworks.json"),
    ("cta_conversion_knowledge", "cta_conversion_knowledge.json"),
    ("manychat_funnel_templates", "manychat_funnel_templates.json"),
]


for collection_name, data_file in COLLECTIONS:
    count = seed_collection(collection_name, data_file)
    print(f"{collection_name}: upserted {count} documents")
