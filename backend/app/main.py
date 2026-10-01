from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import delivery_points, health, routes
from app.core.config import settings
from app.services.exceptions import DomainError


def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name, version=settings.app_version)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(health.router)
    application.include_router(delivery_points.router, prefix=settings.api_v1_prefix)
    application.include_router(routes.router, prefix=settings.api_v1_prefix)

    @application.exception_handler(DomainError)
    async def domain_error_handler(_request: Request, exc: DomainError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    @application.exception_handler(RequestValidationError)
    async def validation_error_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        details = exc.errors()
        messages = []
        for error in details:
            fields = " -> ".join(str(loc) for loc in error.get("loc", []))
            messages.append(f"{fields}: {error.get('msg', 'valor no válido')}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": " ".join(messages)},
        )

    return application


app = create_app()
