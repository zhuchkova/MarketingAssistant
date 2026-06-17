import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="content_frameworks"
)


def retrieve_content_frameworks(
    profile: dict,
    audience_analysis: dict,
    content_idea: dict,
    n_results: int = 3
) -> str:
    query = f"""
    Niche: {profile.get("niche")}
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
    Topic: {content_idea.get("topic")}
    Idea framing: {content_idea.get("angle")}
    Hook: {content_idea.get("hook")}
    Post format: {content_idea.get("post_format") or content_idea.get("idea_post_format")}
    """

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
    )

    docs = results.get("documents", [[]])[0]

    return "\n".join(f"- {doc}" for doc in docs)
