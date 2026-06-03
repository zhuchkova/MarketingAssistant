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
    Goal: {profile.get("goal")}
    Audience profile: {audience_analysis.get("audience_profile")}
    Pains: {audience_analysis.get("pains")}
    Desires: {audience_analysis.get("desires")}
    Objections: {audience_analysis.get("objections")}
    Content angles: {audience_analysis.get("content_angles")}
    Topic: {content_idea.get("topic")}
    Angle: {content_idea.get("angle")}
    Hook: {content_idea.get("hook")}
    """

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
    )

    docs = results.get("documents", [[]])[0]

    return "\n".join(f"- {doc}" for doc in docs)