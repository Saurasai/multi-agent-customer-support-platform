from langchain_groq import ChatGroq
from pydantic import BaseModel

from app.config import GROQ_API_KEY
from app.state import AgentState


class PlannerOutput(BaseModel):
    """
    Output produced by the Planner Agent.
    """

    plan: list[str]

    use_retriever: bool

    use_researcher: bool


llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0,
).with_structured_output(PlannerOutput)


SYSTEM_PROMPT = """
You are the Planner Agent for a customer support platform.

Your job is NOT to answer the user.

Your job is to decide which capabilities are required.

Rules:

1. If company policies, FAQs or documentation are needed,
   set use_retriever = true.

2. If external information like order lookup,
   ticket creation or shipping status is needed,
   set use_researcher = true.

3. If both are required,
   set both values to true.

4. If neither is required,
   set both values to false.

Return only structured output.
"""


def planner_node(state: AgentState):

    result = llm.invoke(
        [
            ("system", SYSTEM_PROMPT),
            *state["messages"],
        ]
    )

    return {
        "plan": result.plan,
        "use_retriever": result.use_retriever,
        "use_researcher": result.use_researcher,
    }
    