from fastapi import APIRouter
from app.services.image_generation.styles.registry import STYLES

router = APIRouter()

@router.get("/styles")
async def list_styles():
    return[
        {
            "id": style.id,
            "name": style.name,
            "description": style.description,        }
        for style in STYLES.values()
    ]