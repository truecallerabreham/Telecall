"""FastAPI application entry point."""

from fastapi import FastAPI

from telecomcall.api.routes.voice import router as voice_router

app = FastAPI(
    title="TelecomCall API",
    description="AI Voice Mobile Carrier Assistant",
    version="0.1.0",
)

app.include_router(voice_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "TelecomCall API is running"}
