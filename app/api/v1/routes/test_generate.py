from fastapi import APIRouter, HTTPException

from app.api.v1.schemas.request import TestGenerateRequest
from app.api.v1.schemas.response import TestGenerateResponse, ImageResponse
from app.providers.factory import get_provider
from app.providers.schemas import ImageGenerationInput

router = APIRouter()

@router.post("/test-generate", response_model=TestGenerateResponse)
async def test_generate(request: TestGenerateRequest):
    try:
        provider = get_provider(request.provider)

        input_data = ImageGenerationInput(
            prompt=request.prompt,
            num_images=1
        )

        results = await provider.generate(input_data)

        images = [
            ImageResponse(
                image_url=img.image_url,
                provider=img.provider,
                model=img.model
            )
            for img in results
        ]

        return TestGenerateResponse(images=images)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))