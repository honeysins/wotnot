from pydantic import BaseModel
from typing import Optional

class MessageGenerationRequest(BaseModel):
    prompt: str

class MessageGenerationResponse(BaseModel):
    generated_message: str
    success: bool
    error: Optional[str] = None
