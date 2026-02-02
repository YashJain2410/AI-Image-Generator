from pydantic import BaseModel
from typing import Optional

class GenerateResponse(BaseModel):
    images: list[dict]