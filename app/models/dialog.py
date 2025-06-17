from pydantic import BaseModel, Field


class MessageInput(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


class MessageOutput(BaseModel):
    response: str
