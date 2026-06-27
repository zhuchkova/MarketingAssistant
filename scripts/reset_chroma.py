import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

client.delete_collection("cta_conversion_knowledge")

print("collection deleted")