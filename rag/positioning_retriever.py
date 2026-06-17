import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="positioning_knowledge"
)

def retrieve_positioning_knowledge(profile: dict, n_results: int = 5) -> str:
    query = f"""
    Niche: {profile.get("niche")}
    Offer: {profile.get("offer")}
    Target audience: {profile.get("target_audience")}
    Expertise: {profile.get("expertise")}
    Personal touch: {profile.get("personal_touch")}
    Market scope: {profile.get("market_scope")}
    Primary market: {profile.get("primary_market")}
    Currency: {profile.get("currency")}
    Locale notes: {profile.get("locale_notes")}
    Goal: {profile.get("goal")}
    """

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
    )

    docs = results.get("documents", [[]])[0]

    return "\n".join(f"- {doc}" for doc in docs)
