import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

client.delete_collection("positioning_knowledge")

print("collection deleted")