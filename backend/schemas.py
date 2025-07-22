from pydantic import BaseModel

__all__ = ["ChatRequest", "ChatResponse"]


class ChatRequest(BaseModel):
    """Incoming chat request payload sent from the frontend."""

    message: str
    isCodeMode: bool = False  # True = analyse code, False = normal chat


class ChatResponse(BaseModel):
    """Standardised chat response envelope returned to the frontend."""

    response: str 