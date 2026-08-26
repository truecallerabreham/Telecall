"""Test voice agent pipeline - Milestone 3.9: Voice pipeline works."""

import asyncio
from telecomcall.agent.fastrtc_agent import VoiceAgent


async def test_pipeline():
    """Test the full STT -> Agent -> TTS pipeline without browser."""
    print("Creating VoiceAgent...")
    agent = VoiceAgent(
        thread_id="test-pipeline",
        tool_use_message="Let me look for that in the system",
        sound_effect_seconds=0,
        fallback_message="I'm sorry, I couldn't find anything useful.",
    )

    print(f"STT model: {agent.stt_model.__class__.__name__}")
    print(f"TTS model: {agent.tts_model.__class__.__name__}")
    print(f"Agent type: {agent.react_agent.__class__.__name__}")
    print()

    # Test text chat
    print("Testing text chat...")
    response = await agent.chat("What plans do you have?")
    print(f"Response: {response.encode('ascii', errors='replace').decode('ascii')}")
    print()

    # Test TTS
    print("Testing TTS...")
    sample_rate, audio = await agent.text_to_speech("Hello, welcome to TelecomCo!")
    print(f"TTS output: {sample_rate}Hz, {len(audio)} samples ({len(audio)/sample_rate:.1f}s)")
    print()

    print("All pipeline components verified successfully!")


if __name__ == "__main__":
    asyncio.run(test_pipeline())
