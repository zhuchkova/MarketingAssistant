#python scripts/seed_chroma_idea.py
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="idea_knowledge"
)

documents = [
    "Hook pattern: Most people think [common belief], but actually [contrarian truth].",
    "Hook pattern: You do not need [expensive solution]. You need [simpler mechanism].",
    "Hook pattern: The biggest mistake [audience] makes with [topic] is [mistake].",
    "Hook pattern: 3 ways to [desired outcome] without [painful action].",
    "Hook pattern: I tested [method] so you do not have to.",
    "Content angle: contrarian posts work well when the audience has a strong false belief.",
    "Content angle: mistake-based posts work well when the audience feels stuck and needs clarity.",
    "Content angle: how-to posts work well when the audience wants practical implementation.",
    "Content angle: behind-the-scenes posts build authority and trust.",
    "Content angle: before-after posts show transformation and make the value concrete.",
]

metadatas = [
    {"type": "hook_pattern", "angle": "contrarian", "agent": "idea_agent"},
    {"type": "hook_pattern", "angle": "simplification", "agent": "idea_agent"},
    {"type": "hook_pattern", "angle": "mistake", "agent": "idea_agent"},
    {"type": "hook_pattern", "angle": "how_to", "agent": "idea_agent"},
    {"type": "hook_pattern", "angle": "experiment", "agent": "idea_agent"},
    {"type": "content_angle", "angle": "contrarian", "agent": "idea_agent"},
    {"type": "content_angle", "angle": "mistake", "agent": "idea_agent"},
    {"type": "content_angle", "angle": "how_to", "agent": "idea_agent"},
    {"type": "content_angle", "angle": "behind_the_scenes", "agent": "idea_agent"},
    {"type": "content_angle", "angle": "before_after", "agent": "idea_agent"},
]

ids = [f"idea_{i}" for i in range(len(documents))]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids,
)

print("✅ idea_knowledge collection seeded")