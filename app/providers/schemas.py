from pydantic import BaseModel
from typing import List, Optional

class ImageGenerationInput(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = None

    reference_image_url: Optional[str] = None
    strength: float = 0.75

    image_size: str = "1024x1024"
    num_images: int = 1
    quality: str = "standard"

class ImageResult(BaseModel):
    image_url: str
    provider: str
    model: str