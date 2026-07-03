from pydantic import BaseModel

from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY
from app.state import AgentState


class SupportResponse(BaseModel):
    resolution: str
    confidence: float
    escalate: bool
    sources: list[str]


llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0,
).with_structured_output(SupportResponse)


SYSTEM_PROMPT = """
You are an expert customer support assistant.

Your responsibilities:

1. Answer ONLY using the provided conversation, knowledge base, and tool results.
2. Never invent information.
3. If the required information is missing, clearly state that you don't know.
4. If tool results conflict with the knowledge base, trust the tool results.
5. Respond professionally and concisely.
6. If the issue requires a human agent, set escalate=True.

Return only the structured response.
"""


def support_node(state: AgentState):

    # ----------------------------
    # Knowledge Base Context
    # ----------------------------
    retrieved_docs = state.get("retrieved_docs", [])

    kb_context = ""

    sources = []

    for doc in retrieved_docs:
        kb_context += (
            f"Source: {doc['source']}\n"
            f"{doc['content']}\n\n"
        )
        sources.append(doc["source"])

    # ----------------------------
    # Tool Results
    # ----------------------------
    tool_results = state.get("tool_results", [])

    tool_context = ""

    for tool_result in tool_results:
        tool_context += (
            f"Tool: {tool_result['tool']}\n"
            f"Arguments: {tool_result['arguments']}\n"
            f"Result: {tool_result.get('result', tool_result.get('error'))}\n\n"
        )

    # ----------------------------
    # Build Messages
    # ----------------------------
    messages = [
        ("system", SYSTEM_PROMPT),
        *state["messages"],
    ]

    if kb_context:
        messages.append(
            (
                "system",
                f"Knowledge Base Context:\n\n{kb_context}",
            )
        )

    if tool_context:
        messages.append(
            (
                "system",
                f"Tool Results:\n\n{tool_context}",
            )
        )

    # ----------------------------
    # Generate Response
    # ----------------------------
        # ----------------------------
    # Generate Response
    # ----------------------------
    result = llm.invoke(messages)

    output = result.model_dump()

    output["sources"] = sources

    output["tools_used"] = [
        tool["tool"] for tool in tool_results
    ]

    return {
        "final_response": output
    }

    