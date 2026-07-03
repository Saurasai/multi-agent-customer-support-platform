from langchain_core.messages import HumanMessage

from app.agents.planner import planner_node
from app.agents.researcher import researcher_node

state = {
    "messages": [
        HumanMessage(
            content="Where is my order ORD004?"
        )
    ]
}

print(planner_node(state))
state = {
    "messages": [
        HumanMessage(content="Where is my order ORD002?")
    ]
}

print(researcher_node(state))


from langchain_core.messages import HumanMessage

from app.agents.retriever import retriever_node

state = {
    "messages": [
        HumanMessage(content="How do I get a refund?")
    ]
}

result = retriever_node(state)

print(result)