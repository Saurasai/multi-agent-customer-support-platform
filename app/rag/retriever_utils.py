from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


vectorstore = Chroma(
    persist_directory="./db/chromadb",
    collection_name="support_kb",
    embedding_function=embeddings
)


def retrieve_documents(query: str, k: int = 3):
    """
    Retrieve the top-k most relevant documents for a query.
    """
    return vectorstore.similarity_search(query, k=k)