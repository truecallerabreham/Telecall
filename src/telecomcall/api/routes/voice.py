"""Voice routes for Twilio integration."""

from fastapi import APIRouter, Request
from twilio.twiml.voice_response import VoiceResponse

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/webhook")
async def voice_webhook(request: Request):
    """Handle incoming Twilio voice calls.

    This webhook receives the call and returns TwiML to connect
    the caller to the FastRTC media stream.
    """
    response = VoiceResponse()

    # Use connect with Stream for real-time bidirectional audio
    connect = response.connect()
    connect.stream(url="wss://your-server.com/media-stream")

    return {"content_type": "application/xml", "body": str(response)}


@router.post("/incoming")
async def incoming_call(request: Request):
    """Handle incoming call from Twilio.

    Returns TwiML to connect the call to the FastRTC stream.
    """
    response = VoiceResponse()

    # Greet the caller
    response.say("Welcome to TelecomCall. Connecting you now...")

    # Connect to the media stream
    connect = response.connect()
    connect.stream(url="wss://your-server.com/media-stream")

    return {"content_type": "application/xml", "body": str(response)}


@router.post("/status")
async def call_status(request: Request):
    """Handle call status updates from Twilio."""
    form_data = await request.form()
    call_status = form_data.get("CallStatus", "unknown")
    call_sid = form_data.get("CallSid", "unknown")
    print(f"Call {call_sid} status: {call_status}")
    return {"status": "ok"}
