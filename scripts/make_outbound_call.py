"""Make an outbound phone call via Twilio."""

from twilio.rest import Client

from telecomcall.config import settings


def make_call(to_number: str):
    """Make an outbound call to a phone number."""
    client = Client(settings.twilio.account_sid, settings.twilio.auth_token)

    call = client.calls.create(
        to=to_number,
        from_=settings.twilio.phone_number,
        url="https://your-server-url.com/voice/inbound",
    )

    print(f"Call initiated: {call.sid}")
    return call.sid


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python make_outbound_call.py +1234567890")
        sys.exit(1)

    make_call(sys.argv[1])
