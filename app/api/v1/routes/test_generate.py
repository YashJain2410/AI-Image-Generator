from fastapi import APIRouter, HTTPException

from app.api.v1.schemas.request import TestGenerateRequest
from app.api.v1.schemas.response import TestGenerateResponse
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

        return TestGenerateResponse(images=results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))