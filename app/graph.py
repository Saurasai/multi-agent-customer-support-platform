from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.state import AgentState

from app.agents.planner import planner_node
from app.agents.retriever import retriever_node
from app.agents.researcher import researcher_node
from app.agents.support import support_node


def planner_router(state: AgentState) -> str:
    """
    Decide which node should execute after the planner.
    """

    use_retriever = state.get("use_retriever", False)
    use_researcher = state.get("use_researcher", False)

    # Temporary priority:
    # If both are requested, execute the researcher.
    # Later we'll upgrade this to execute both in parallel.
    if use_researcher:
        return "researcher"

    if use_retriever:
        return "retriever"

    return "support"


graph = StateGraph(AgentState)

# -----------------------------
# Register Nodes
# -----------------------------

graph.add_node("planner", planner_node)
graph.add_node("retriever", retriever_node)
graph.add_node("researcher", researcher_node)
graph.add_node("support", support_node)

# -----------------------------
# Entry Point
# -----------------------------

graph.add_edge(START, "planner")

# -----------------------------
# Planner Routing
# -----------------------------

graph.add_conditional_edges(
    "planner",
    planner_router,
    {
        "retriever": "retriever",
        "researcher": "researcher",
        "support": "support",
    },
)

# -----------------------------
# Fixed Flow
# -----------------------------

graph.add_edge("retriever", "support")
graph.add_edge("researcher", "support")
graph.add_edge("support", END)

# -----------------------------
# Compile Graph
# -----------------------------

memory = MemorySaver()

support_graph = graph.compile(
    checkpointer=memory
)