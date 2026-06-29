import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="idea_knowledge"
)

def retrieve_idea_knowledge(
    profile: dict,
    audience_analysis: dict,
    n_results: int = 8,
    trend_context: str = ""
) -> str:
    query = f"""
    Niche: {profile.get("niche")}
    Offer: {profile.get("offer")}
    Target audience: {profile.get("target_audience")}
    Personal touch: {profile.get("personal_touch")}
    Market scope: {profile.get("market_scope")}
    Primary market: {profile.get("primary_market")}
    Currency: {profile.get("currency")}
    Locale notes: {profile.get("locale_notes")}
    Goal: {profile.get("goal")}
    Audience profile: {audience_analysis.get("audience_profile")}
    Pains: {audience_analysis.get("pains")}
    Desires: {audience_analysis.get("desires")}
    Objections: {audience_analysis.get("objections")}
    Trigger moments: {audience_analysis.get("trigger_moments")}
    Proof points: {audience_analysis.get("proof_points")}
    Audience language: {audience_analysis.get("audience_language")}
    Market context: {audience_analysis.get("market_context")}
    Content angles: {audience_analysis.get("content_angles")}
    Trend context: {trend_context}
    """

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
    )

    docs = results.get("documents", [[]])[0]
    psychology_docs = collection.query(
        query_texts=[query],
        n_results=5,
        where={"label": "psychology"},
    ).get("documents", [[]])[0]

    prioritized_docs = dedupe_docs(psychology_docs + docs)

    return "\n".join(f"- {doc}" for doc in prioritized_docs)


def dedupe_docs(docs: list[str]) -> list[str]:
    seen = set()
    unique_docs = []
    for doc in docs:
        if doc in seen:
            continue
        seen.add(doc)
        unique_docs.append(doc)
    return unique_docs
