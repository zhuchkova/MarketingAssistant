from chroma_seed_utils import seed_collection


count = seed_collection("manychat_funnel_templates", "manychat_funnel_templates.json")
print(f"manychat_funnel_templates: upserted {count} documents")
