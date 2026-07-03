from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY
from app.state import AgentState

from app.tools.support_tools import (
    lookup_order,
    refund_policy,
    shipping_policy,
    create_ticket,
)

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0,
)

TOOLS = {
    "lookup_order": lookup_order,
    "refund_policy": refund_policy,
    "shipping_policy": shipping_policy,
    "create_ticket": create_ticket,
}

llm = llm.bind_tools(list(TOOLS.values()))


def researcher_node(state: AgentState) -> dict:
    """
    Executes tool calls requested by the LLM and stores
    structured tool results in the graph state.
    """

    response = llm.invoke(state["messages"])

    tool_results = []

    for tool_call in getattr(response, "tool_calls", []):

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        tool = TOOLS.get(tool_name)

        if tool is None:
            continue

        try:
            result = tool.invoke(tool_args)

            tool_results.append(
                {
                    "tool": tool_name,
                    "arguments": tool_args,
                    "result": result,
                }
            )

        except Exception as e:

            tool_results.append(
                {
                    "tool": tool_name,
                    "arguments": tool_args,
                    "error": str(e),
                }
            )

    return {
        "tool_results": tool_results
    }