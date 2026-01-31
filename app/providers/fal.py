import httpx
from typing import List

from app.core.config import settings
from app.providers.base import BaseImageProvider
from app.providers.schemas import ImageGenerationInput, ImageResult

class FalProvider(BaseImageProvider):
    provider_name = "fal"

    def __init__(self, model: str = "fal-ai/fast-sdxl"):
        if not settings.FAL_API_KEY:
            raise RuntimeError("FAL API key not set")
        
        self.model = model
        self.api_url = f"https://fal.run/{model}"
        self.headers = {
            "Authorization": f"Key {settings.FAL_API_KEY}",
            "Content-Type": "application/json"
        }

    async def generate(self, data: ImageGenerationInput) -> List[ImageResult]:
        payload = {
            "prompt": data.prompt,
            "image_size": data.image_size,
            "num_images": data.num_images
        }

        if data.reference_image_url:
            payload["image_url"] = data.reference_image_url
            payload["strength"] = data.strength

        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                self.api_url,
                headers=self.headers,
                json = payload,
            )

        if response.status_code != 200:
            raise RuntimeError(f"FAL error: {response.text}")
        
        output = response.json()

        images: List[ImageResult] = []

        for img in output["images"]:
            images.append(
                ImageResult(
                    image_url=img["url"],
                    provider=self.provider_name,
                    model=self.model
                )
            )

        return images