from app.services.image_generation.styles.schema import StyleDefinition


STYLES: dict[str, StyleDefinition] = {
    "cinematic_portrait": StyleDefinition(
        id="cinematic_portrait",
        name="Cinematic Portrait",
        description="Dramatic lighting, shallow depth of field, cinematic look",

        preview_image_url="",

        style_reference_images=[
            "https://c.ndtvimg.com/2024-04/sg6j96k8_photos-anushka-sen-shares-perfect-sunkissed-pictures_625x300_17_April_24.jpg",
        ],

        style_type="ip_adapter",

        base_prompt=(
            "cinematic portrait, dramatic lighting, shallow depth of field, "
            "ultra-detailed, professional photography, 85mm lens"
        ),

        negative_prompt="blurry, low quality, distorted face, cartoon",

        supported_providers=["fal", "replicate", "huggingface"],
        recommended_models=["sdxl"],

        default_strength=0.8,
    ),

    "product_ad": StyleDefinition(
        id="product_ad",
        name="Product Advertisement",
        description="Clean studio lighting, sharp focus, commercial product photo",

        preview_image_url="",

        style_reference_images=[
            "",
            "",
        ],

        style_type="ip_adapter",

        base_prompt=(
            "cinematic portrait, dramatic lighting, shallow depth of field, "
            "ultra-detailed, professional photography, 85mm lens"
        ),

        negative_prompt="blurry, low quality, distorted face, cartoon",

        supported_providers=["fal", "replicate", "huggingface"],
        recommended_models=["sdxl"],

        default_strength=0.8,
    ),

    "candid_photo": StyleDefinition(
        id="candid_photo",
        name="Candid Photo",
        description="Natural light, casual, realistic photography",

        preview_image_url="",

        style_reference_images=[
            "",
            "",
        ],

        style_type="ip_adapter",

        base_prompt=(
            "cinematic portrait, dramatic lighting, shallow depth of field, "
            "ultra-detailed, professional photography, 85mm lens"
        ),

        negative_prompt="blurry, low quality, distorted face, cartoon",

        supported_providers=["fal", "replicate", "huggingface"],
        recommended_models=["sdxl"],

        default_strength=0.8,
    ),
}