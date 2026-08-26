"""Test voice agent in Gradio - Milestone 3.12: Browser voice chat works."""

import asyncio

from telecomcall.agent.fastrtc_agent import FastRTCAgent


async def test_voice():
    """Create FastRTC agent and launch Gradio UI."""
    agent = FastRTCAgent(
        thread_id="gradio-test",
        tool_use_message="Let me look for that in the system",
        sound_effect_seconds=3.0,
        fallback_message="I'm sorry, I couldn't find anything useful in the system.",
    )

    # Launch the Gradio Stream
    stream = agent.stream
    stream.ui.launch(server_port=7860, share=True)


if __name__ == "__main__":
    asyncio.run(test_voice())
