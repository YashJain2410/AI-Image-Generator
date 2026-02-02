from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.image_generation.service import ImageGenerationService
from app.services.image_generation.schemas import GenerateImageCommand
from app.utils.s3 import S3Client

router = APIRouter()
service = ImageGenerationService()
s3 = S3Client()

@router.post("/generate")
async def generate_image(
    style_id: str = Form(...),
    provider: str = Form(...),
    prompt: str | None = Form(None),
    image_size: str = Form("1024x1024"),
    num_images: int = Form(1),
    product_image: UploadFile | None = File(None),
):
    try:
        product_image_url = None

        if product_image:
            file_bytes = await product_image.read()
            product_image_url = s3.upload_file(
                file_bytes=file_bytes,
                content_type=product_image.content_type,
            )

            command = GenerateImageCommand(
                style_id=style_id,
                provider=provider,
                product_image_url=product_image_url,
                user_prompt=prompt,
                image_size=image_size,
                num_images=num_images,
            )

            images = await service.generate(command)

            return {
                "images": [
                    {
                        "image_url": img.image_url,
                        "provider": img.provider,
                        "model": img.model
                    }
                    for img in images
                ]
            }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))