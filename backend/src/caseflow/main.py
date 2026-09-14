from fastapi import FastAPI

from caseflow.api.router import api_router
from caseflow.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )
    app.include_router(api_router, prefix="/api")

    return app


app = create_app()
