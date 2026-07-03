from app.rag.retriever_utils import retrieve_documents

results = retrieve_documents(
    "How do I get a refund?"
)

for i, doc in enumerate(results, start=1):
    print("=" * 40)
    print(f"Result {i}")
    print(doc.page_content)
    print(doc.metadata)