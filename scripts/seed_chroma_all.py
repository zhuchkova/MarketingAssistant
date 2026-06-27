from chroma_seed_utils import seed_collection


COLLECTIONS = [
    ("positioning_knowledge", "positioning_knowledge"),
    ("idea_knowledge", "idea_knowledge.json"),
    ("content_frameworks", "content_frameworks.json"),
    ("cta_patterns", "cta_patterns.json"),
    ("comment_automation_templates", "comment_automation_templates.json"),
]


for collection_name, data_file in COLLECTIONS:
    count = seed_collection(collection_name, data_file)
    print(f"{collection_name}: upserted {count} documents")
