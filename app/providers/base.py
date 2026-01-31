from abc import ABC, abstractmethod
from typing import List

from app.providers.schemas import ImageGenerationInput, ImageResult

class BaseImageProvider(ABC):
    provider_name: str

    @abstractmethod
    async def generate(self, data: ImageGenerationInput) -> List[ImageResult]:
        """
        Generate images based on normalized input. Must return a list of ImageResult.
        """
        pass