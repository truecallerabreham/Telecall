"""Twilio voice webhook routes."""

from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.post("/voice/incoming")
async def handle_incoming_call(request: Request):
    """Handle incoming phone call from Twilio.

    Returns TwiML that connects the caller to a media stream.
    """
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Hello! Welcome to TelecomCo. I'm Lisa, your virtual assistant. How can I help you today?</Say>
    <Connect>
        <Stream url="wss://your-server-url.com/media-stream" />
    </Connect>
</Response>"""
    return PlainTextResponse(content=twiml, media_type="application/xml")


@router.post("/voice/outbound")
async def handle_outbound_call():
    """Handle outbound call status callbacks."""
    return {"status": "ok"}


@router.post("/media-stream")
async def handle_media_stream(request: Request):
    """Handle WebSocket media stream from Twilio.

    This endpoint receives raw audio from the phone call,
    processes it through the voice pipeline, and sends audio back.
    """
    # Will be implemented in Phase 7 (multi-turn memory)
    return PlainTextResponse(content="WebSocket endpoint", media_type="text/plain")
