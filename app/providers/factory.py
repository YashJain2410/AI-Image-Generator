from app.providers.base import BaseImageProvider
from app.providers.huggingface import HuggingFaceProvider
from app.providers.replicate import ReplicateProvider
from app.providers.fal import FalProvider

def get_provider(provider_name: str) -> BaseImageProvider:
    if provider_name == "huggingface":
        return HuggingFaceProvider()
    
    if provider_name == "fal":
        return FalProvider()
    
    if provider_name == "replicate":
        return ReplicateProvider()
    
    raise ValueError(f"Unsupported Provider: {provider_name}")