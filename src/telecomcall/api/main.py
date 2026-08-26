"""FastAPI application for TelecomCall voice agent."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from telecomcall.api.routes.voice import router as voice_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="TelecomCall API",
        description="AI Voice Mobile Carrier Assistant API",
        version="0.1.0",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include voice routes
    app.include_router(voice_router)

    @app.get("/")
    async def root():
        return {"message": "TelecomCall API is running"}

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    return app


app = create_app()
