import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="idea_knowledge"
)

def retrieve_idea_knowledge(profile: dict, audience_analysis: dict, n_results: int = 6) -> str:
    query = f"""
    Niche: {profile.get("niche")}
    Offer: {profile.get("offer")}
    Target audience: {profile.get("target_audience")}
    Goal: {profile.get("goal")}
    Audience profile: {audience_analysis.get("audience_profile")}
    Pains: {audience_analysis.get("pains")}
    Desires: {audience_analysis.get("desires")}
    Objections: {audience_analysis.get("objections")}
    Content angles: {audience_analysis.get("content_angles")}
    """

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
    )

    docs = results.get("documents", [[]])[0]

    return "\n".join(f"- {doc}" for doc in docs)