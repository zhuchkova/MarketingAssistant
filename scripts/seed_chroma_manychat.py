#python scripts/seed_chroma_manychat.py
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="manychat_funnel_templates")

documents = [
    "ManyChat flow: User comments keyword -> send resource -> ask qualification question -> suggest next step.",
    "ManyChat first message: Hey! Here is the resource I mentioned. Quick question before you use it: are you building this for yourself or for clients?",
    "ManyChat qualification question: What best describes you right now: founder, freelancer, coach, or creator?",
    "ManyChat follow-up: Based on your answer, I would start with this simple version first.",
    "ManyChat follow-up: If you want help adapting this to your business, reply with HELP.",
    "ManyChat flow for lead magnet: deliver the resource first, then ask one short question, then offer a next step.",
]

metadatas = [
    {"type": "flow_template", "stage": "overview"},
    {"type": "message_template", "stage": "first_message"},
    {"type": "question_template", "stage": "qualification"},
    {"type": "message_template", "stage": "follow_up"},
    {"type": "message_template", "stage": "soft_offer"},
    {"type": "flow_template", "stage": "lead_magnet"},
]

ids = [f"manychat_{i}" for i in range(len(documents))]

collection.add(documents=documents, metadatas=metadatas, ids=ids)

print("Manychat_funnel_templates seeded")