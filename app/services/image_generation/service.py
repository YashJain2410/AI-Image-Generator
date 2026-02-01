from typing import List
from app.providers.factory import get_provider
from app.providers.schemas import ImageResult
from app.services.image_generation.schemas import GenerateImageCommand
from app.services.image_generation.styles.resolver import resolve_style_input

class ImageGenerationService:
    async def generate(self, command: GenerateImageCommand) -> List[ImageResult]:

        generation_input = resolve_style_input(
            style_id=command.style_id,
            provider=command.provider,
            product_image_url=command.product_image_url,
            user_prompt=command.user_prompt
        )

        provider = get_provider(command.provider)

        generation_input.image_size = command.image_size
        generation_input.num_images = command.num_images

        images = await provider.generate(generation_input)
        return images