from pydantic import BaseModel
from typing import Optional

class GenerateImageCommand(BaseModel):
    style_id: str
    provider: str

    product_image_url: Optional[str] = None

    user_prompt: Optional[str] = None

    image_size: str = "1024x1024"
    num_images: int = 1