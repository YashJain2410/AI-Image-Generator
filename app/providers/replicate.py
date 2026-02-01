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

        # Base input (text -> image)
        model_input: dict = {
            "prompt": data.prompt,
            "num_outputs": data.num_images,
        }

        # img2img (product image)
        if data.reference_image_url:
            model_input["image"] = data.reference_image_url
            model_input["strength"] = data.strength

        # Style image (IP-Adapter-like support) | Replicate models differ, we pass this only if provided
        if(data.style_type == "ip_adapter" and data.style_reference_images and len(data.style_reference_images) > 0):
            model_input["style_image"] = data.style_reference_images[0]     # Common naming used by replicate models

        if data.negative_prompt:
            model_input["negative_prompt"] = data.negative_prompt

        payload = {
            "version": self.model,
            "input": model_input,
        }

        async with httpx.AsyncClient(timeout=120) as client:
            create_resp = await client.post(
                "https://api.replicate.com/v1/predictions",
                headers=self.headers,
                json = payload,
            )

            if create_resp.status_code != 201:
                raise RuntimeError(
                    f"Replicate create failed: {create_resp.text}"
                )
            
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
                    raise RuntimeError(
                        f"Replicate generation failed: {result.get('error')}"
                    )
                
        output = result["output"]

        if isinstance(output, str):
            output = [output]
                
        images: List[ImageResult] = []

        for url in output:
            images.append(
                ImageResult(
                    image_url=url,
                    provider=self.provider_name,
                    model=self.model
                )
            )

        return images