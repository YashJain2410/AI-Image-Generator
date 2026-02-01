from fastapi import APIRouter, HTTPException

from app.api.v1.schemas.request import TestGenerateRequest
from app.api.v1.schemas.response import TestGenerateResponse
from app.services.image_generation.schemas import GenerateImageCommand
from app.services.image_generation.service import ImageGenerationService

router = APIRouter()
service = ImageGenerationService()

@router.post("/test-service-generate", response_model=TestGenerateResponse)
async def test_service_generate(request: TestGenerateRequest):
    try:
        command = GenerateImageCommand(
            style_id=request.style_id,
            provider = request.provider,
            product_image_url=request.product_imag_url,
            user_prompt=request.prompt,
            image_size=request.image_size,
            num_images=request.num_images,
        )

        images = await service.generate(command)

        return {"images": images}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail = str(e))