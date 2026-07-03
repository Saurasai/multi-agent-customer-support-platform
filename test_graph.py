from langchain_core.messages import HumanMessage

from app.graph import support_graph

state = {
    "messages": [
        HumanMessage(
            content="how do i get a refund?"
        )
    ]
}

result = support_graph.invoke(
    state,
    config={
        "configurable": {
            "thread_id": "thread-1"
        }
    },
)

print(result["final_response"])