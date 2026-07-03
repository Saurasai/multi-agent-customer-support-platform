from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Incoming request from the client.
    """

    message: str = Field(
        description="User message"
    )

    thread_id: str = Field(
        default="default-thread",
        description="Conversation ID"
    )


class ChatResponse(BaseModel):
    """
    Response returned to the client.
    """

    resolution: str

    confidence: float

    escalate: bool

    sources: list[str]

    tools_used: list[str]