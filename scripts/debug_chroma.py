import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

# show all collections
collections = client.list_collections()

print("\n=== COLLECTIONS ===")
for c in collections:
    print(c.name)

# # open collection
# collection = client.get_collection("positioning_knowledge")
#
# # get everything
# data = collection.get()
#
# print("\n=== IDS ===")
# print(data["ids"])
#
# print("\n=== DOCUMENTS ===")
# for doc in data["documents"]:
#     print("-", doc)
#
# print("\n=== METADATA ===")
# for meta in data["metadatas"]:
#     print(meta)
#
# print('The number of documents', collection.count())
# data = collection.get(include=["metadatas"])
# print('Metadata:', data)
#
# results = collection.query(
#     query_texts=["AI automation for founders"],
#     n_results=3
# )
#
# print('Testing semantic search manually', results["documents"])