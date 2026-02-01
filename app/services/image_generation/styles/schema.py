from pydantic import BaseModel
from typing import List, Optional

class StyleDefinition(BaseModel):
    id: str
    name: str
    description: str

    preview_image_url: str

    style_reference_images: List[str]
    style_type: str

    base_prompt: Optional[str] = None
    negative_prompt: Optional[str] = None

    supported_providers: List[str]
    recommended_models: Optional[List[str]] = None

    default_strength: float = 0.75