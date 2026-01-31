import asyncio
import httpx
from typing import List

from app.core.config import settings
from app.providers.base import BaseImageProvider
from app.providers.schemas import ImageGenerationInput, ImageResult

class ReplicateProvider(BaseImageProvider):
    provider_name = "replicate"

    def __init__(self, model: str = "black-forest-labs/flux-2-pro"):
        if not settings.REPLICATE_API_TOKEN:
            raise RuntimeError("Replicate API token not set")
        
        self.model = model
        self.headers = {
            "Authorization": f"Token {settings.REPLICATE_API_TOKEN}",
            "Content-Type": "application/json",
        }

    async def generate(self, data: ImageGenerationInput) -> List[ImageResult]:
        payload = {
            "version": self.model,
            "input": {
                "prompt": data.prompt,
                "num_outputs": data.num_images
            }
        }

        if data.reference_image_url:
            payload["input"]["image"] = data.reference_image_url
            payload["input"]["strength"] = data.strength

        async with httpx.AsyncClient(timeout=120) as client:
            create_resp = await client.post(
                "https://api.replicate.com/v1/predictions",
                headers=self.headers,
                json = payload,
            )

            if create_resp.status_code != 201:
                raise RuntimeError(create_resp.text)
            
            prediction = create_resp.json()
            prediction_url = prediction["urls"]["get"]

            while True:
                await asyncio.sleep(2)

                poll_resp = await client.get(
                    prediction_url,
                    headers=self.headers,
                )

                result = poll_resp.json()

                if result["status"] == "succeeded":
                    break

                if result["status"] == "failed":
                    raise RuntimeError("Replicate generation failed")
                
        images: List[ImageResult] = []

        for url in result["output"]:
            images.append(
                ImageResult(
                    image_url=url,
                    provider=self.provider_name,
                    model=self.model
                )
            )

        return images