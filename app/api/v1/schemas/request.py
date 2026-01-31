from pydantic import BaseModel
from typing import Optional

class TestGenerateRequest(BaseModel):
    prompt: str
    provider: str = "huggingface"
    model: Optional[str] = None