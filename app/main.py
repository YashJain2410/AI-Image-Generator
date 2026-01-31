from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.test_generate import router as test_generate_router

def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
    )

    app.include_router(
        health_router,
        prefix=settings.API_V1_PREFIX,
        tags = ["Health"],
    )

    app.include_router(
        test_generate_router,
        prefix=settings.API_V1_PREFIX,
        tags = ["Testing Generate"]
    )

    return app

app = create_app()