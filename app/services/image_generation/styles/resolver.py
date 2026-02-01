from app.providers.schemas import ImageGenerationInput
from app.services.image_generation.styles.registry import STYLES

class StyleNotFoundError(Exception):
    pass

class StyleValidationError(Exception):
    pass

def resolve_style_input(
        *, 
        style_id: str, 
        provider: str,
        product_image_url: str | None,
        user_prompt: str | None,
):
    
    style = STYLES[style_id]

    if provider not in style.supported_providers:
        raise StyleValidationError(
            f"Style '{style_id}' not supported by provider '{provider}'"
        )
    
    final_prompt = style.base_prompt or ""
    if user_prompt:
        final_prompt = f"{final_prompt}, {user_prompt}"

    return ImageGenerationInput(
        prompt=final_prompt,
        negative_prompt=style.negative_prompt,

        reference_image_url=product_image_url,

        style_reference_images=style.style_reference_images,
        style_type=style.style_type,

        strength=style.default_strength,
    )
