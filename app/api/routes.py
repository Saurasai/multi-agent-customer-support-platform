from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage

from app.graph import support_graph
from app.schemas import ChatRequest, ChatResponse
from app.utils.logger import logger

router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with the customer support agent",
)
async def chat(request: ChatRequest):

    logger.info(
        "Incoming request | thread_id=%s | message=%s",
        request.thread_id,
        request.message,
    )

    state = {
        "messages": [
            HumanMessage(content=request.message)
        ]
    }

    try:

        result = support_graph.invoke(
            state,
            config={
                "configurable": {
                    "thread_id": request.thread_id
                }
            }
        )

        logger.info(
            "Request completed | thread_id=%s",
            request.thread_id,
        )

        return ChatResponse(**result["final_response"])

    except Exception as e:

        logger.exception("Error while processing request")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )