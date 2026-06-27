from chroma_seed_utils import seed_collection


count = seed_collection("comment_automation_templates", "comment_automation_templates.json")
print(f"comment_automation_templates: upserted {count} documents")
