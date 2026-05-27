#python scripts/seed_chroma_positioning.py
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="positioning_knowledge"
)

documents = [
    "Formula: I help [specific audience] achieve [desired outcome] through [method or expertise].",
    "Formula: For [target customer] who [need], [product/service] is a [category] that delivers [key benefit]. Unlike [alternative], it [unique differentiation].",
    "Strong positioning should clearly define who you serve, what problem you solve, what outcome you create, and why your approach is different.",
    "Expert positioning example: I help early-stage founders replace chaotic marketing with simple AI workflows that generate consistent content and leads.",
    "Expert positioning example: I help busy coaches turn their expertise into clear content systems that attract qualified clients.",
    "Expert positioning example: I help freelancers build authority on LinkedIn through practical storytelling and niche-specific content.",
    "Positioning angle: Be known for one clear transformation, not many unrelated skills.",
    "Positioning angle: A strong expert brand should connect audience pain, creator expertise, and a memorable point of view.",
    "Audience analysis pattern: identify pains, desires, objections, current alternatives, and emotional triggers before generating content.",
    "Differentiation pattern: Instead of saying you use AI, explain what AI allows your audience to do faster, easier, or better.",
]

metadatas = [
    {"type": "formula", "agent": "audience_agent", "topic": "personal_positioning"},
    {"type": "formula", "agent": "audience_agent", "topic": "product_positioning"},
    {"type": "principle", "agent": "audience_agent", "topic": "positioning_clarity"},
    {"type": "example", "agent": "audience_agent", "niche": "ai_automation", "audience": "founders"},
    {"type": "example", "agent": "audience_agent", "niche": "coaching", "audience": "coaches"},
    {"type": "example", "agent": "audience_agent", "niche": "personal_branding", "audience": "freelancers"},
    {"type": "principle", "agent": "audience_agent", "topic": "known_for"},
    {"type": "principle", "agent": "audience_agent", "topic": "expert_brand"},
    {"type": "framework", "agent": "audience_agent", "topic": "audience_analysis"},
    {"type": "principle", "agent": "audience_agent", "topic": "differentiation"},
]

ids = [f"positioning_{i}" for i in range(len(documents))]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids,
)

print("Positioning_knowledge collection seeded")