from app.state import AgentState
from app.rag.retriever_utils import retrieve_documents


def retriever_node(state: AgentState):

    question = state["messages"][-1].content

    docs = retrieve_documents(question)

    retrieved_docs = []

    for doc in docs:

        retrieved_docs.append(
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source", "Unknown")
            }
        )
    return {
    "retrieved_docs": retrieved_docs
}
   