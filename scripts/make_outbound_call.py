"""Make outbound calls via Twilio - Milestone 4.10: Outbound call works."""

from twilio.rest import Client

from telecomcall.config import settings


def make_outbound_call(to_number: str, ngrok_url: str) -> dict:
    """Make an outbound call to the given phone number.

    Args:
        to_number: The phone number to call (e.g., +1234567890)
        ngrok_url: The ngrok URL for the webhook (e.g., https://xxxx.ngrok.io)

    Returns:
        Call SID and status.
    """
    client = Client(settings.twilio.account_sid, settings.twilio.auth_token)

    call = client.calls.create(
        to=to_number,
        from_=settings.twilio.phone_number,
        url=f"{ngrok_url}/voice/incoming",
        status_callback=f"{ngrok_url}/voice/status",
        status_callback_event=["initiated", "ringing", "answered", "completed"],
    )

    print(f"Outbound call created: {call.sid}")
    print(f"Status: {call.status}")

    return {"call_sid": call.sid, "status": call.status}


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python scripts/make_outbound_call.py <to_number> <ngrok_url>")
        print("Example: python scripts/make_outbound_call.py +1234567890 https://xxxx.ngrok.io")
        sys.exit(1)

    to_number = sys.argv[1]
    ngrok_url = sys.argv[2]
    make_outbound_call(to_number, ngrok_url)
