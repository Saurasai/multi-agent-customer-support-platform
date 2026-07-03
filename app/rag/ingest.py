from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_chroma import Chroma




# -------------------------
# Load Markdown Files
# -------------------------

loader = DirectoryLoader(
    "docs",
    glob="*.md",
    loader_cls=TextLoader
)

documents = loader.load()

print(f"Loaded {len(documents)} documents")


# -------------------------
# Split into Chunks
# -------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)
from pathlib import Path

for chunk in chunks:
    chunk.metadata["source"] = Path(
        chunk.metadata["source"]
    ).name

print(f"Created {len(chunks)} chunks")


# -------------------------
# Embedding Model
# -------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


# -------------------------
# Store in ChromaDB
# -------------------------

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./db/chromadb",
    collection_name="support_kb"
)

print("Knowledge Base Created Successfully!")