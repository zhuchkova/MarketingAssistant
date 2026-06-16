import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

cta_collection = client.get_or_create_collection(
    name="cta_conversion_knowledge"
)

manychat_collection = client.get_or_create_collection(
    name="manychat_funnel_templates"
)


def retrieve_conversion_knowledge(context: dict, n_results: int = 4) -> dict:
    query = f"""
    Niche: {context.get("niche")}
    Offer: {context.get("offer")}
    Target audience: {context.get("target_audience")}
    Goal: {context.get("goal")}

    Audience pains: {context.get("pains")}
    Audience desires: {context.get("desires")}
    Audience objections: {context.get("objections")}
    Trigger moments: {context.get("trigger_moments")}
    Proof points: {context.get("proof_points")}
    Audience language: {context.get("audience_language")}

    Post:
    Hook: {context.get("hook")}
    Body: {context.get("body")}
    CTA: {context.get("cta")}
    Platform: {context.get("platform")}
    Post goal: {context.get("post_goal")}
    """

    cta_results = cta_collection.query(
        query_texts=[query],
        n_results=n_results,
    )

    manychat_results = manychat_collection.query(
        query_texts=[query],
        n_results=n_results,
    )

    cta_docs = cta_results.get("documents", [[]])[0]
    manychat_docs = manychat_results.get("documents", [[]])[0]

    return {
        "cta_knowledge": "\n".join(f"- {doc}" for doc in cta_docs),
        "manychat_knowledge": "\n".join(f"- {doc}" for doc in manychat_docs),
    }
