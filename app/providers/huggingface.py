import base64
import time
import io
from typing import List
from huggingface_hub import AsyncInferenceClient

from app.core.config import settings
from app.providers.base import BaseImageProvider
from app.providers.schemas import ImageGenerationInput, ImageResult


class HuggingFaceProvider(BaseImageProvider):
    provider_name = "huggingface"

    def __init__(self, model: str = "stabilityai/stable-diffusion-2-1-base"):
        if not settings.HUGGINGFACE_API_TOKEN:
            raise RuntimeError("Hugging Face API token not set")

        self.model = model
        self.client = AsyncInferenceClient(
            model=model,
            token=settings.HUGGINGFACE_API_TOKEN,
            timeout=180
        )

    async def generate(self, data: ImageGenerationInput) -> List[ImageResult]:
        start_time = time.perf_counter()

        try:
            image = await self.client.text_to_image(
                prompt=data.prompt
            )

            if image is None:
                raise RuntimeError(
                    "HuggingFace returned no image (model loading / rate-limited / unavailable)"
                )

            if not hasattr(image, "save"):
                raise RuntimeError(
                    f"Unexpected HuggingFace response type: {type(image)}"
                )

            buffered = io.BytesIO()
            image.save(buffered, format="PNG")

            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            image_url = f"data:image/png;base64,{img_str}"

            latency = time.perf_counter() - start_time

            return [
                ImageResult(
                    image_url=image_url,
                    provider=self.provider_name,
                    model=self.model,
                    latency=latency
                )
            ]

        except StopIteration:
            raise RuntimeError(
                "HuggingFace model did not return an image (StopIteration). "
                "Likely model cold start or free-tier limitation."
            )

        except Exception as e:
            raise RuntimeError(f"HuggingFace SDK Error: {str(e)}")
