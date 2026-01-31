from pydantic import BaseModel
from typing import List

class ImageResponse(BaseModel):
    image_url: str
    provider: str
    model: str

class TestGenerateResponse(BaseModel):
    images: List[ImageResponse]