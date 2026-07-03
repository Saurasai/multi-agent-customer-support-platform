from typing import TypedDict, Annotated, Optional

from langgraph.graph.message import add_messages
from operator import add
from typing import Annotated

class AgentState(TypedDict):
    """
    Shared state used by every node in the graph.
    """

    messages: Annotated[list, add_messages]

    plan: Optional[list[str]]

    use_retriever: Optional[bool]

    use_researcher: Optional[bool]

    retrieved_docs: Optional[list[dict]]

    tool_results: Optional[list[dict]]

    final_response: Optional[dict]
    agents_used: Annotated[list[str], add]
