import asyncio
from typing import AsyncIterator, List, Optional, Tuple

import numpy as np
from fastrtc import ReplyOnPause, Stream
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from loguru import logger

from telecomcall.agent.tools.plan_search import search_plan_mock_tool
from telecomcall.agent.utils import model_has_tool_calls
from telecomcall.config import settings
from telecomcall.voice import get_sound_effect

AudioChunk = Tuple[int, np.ndarray]

DEFAULT_SYSTEM_PROMPT = """
Your name is Lisa, and you work for TelecomCo mobile carrier company.
Your task is to provide information about mobile plans using the `search_plan_mock_tool`.
Don't use asterisks or emojis, as you are engaged in a phone call. Just return short and informative responses.
""".strip()


class FastRTCAgent:
    """
    Simplified FastRTC agent that encapsulates all dependencies and logic
    for processing audio through speech-to-text, agent reasoning, and text-to-speech.

    This class combines the React agent creation and FastRTC streaming into a single
    cohesive unit, optimized for mobile phone compatibility by avoiding gradio additional_inputs.
    """

    def __init__(
        self,
        tool_use_message: str = "Let me look for that in the system",
        sound_effect_seconds: float = 3.0,
        stt_model=None,
        tts_model=None,
        voice_effect=None,
        thread_id: str = "default",
        fallback_message: str = "I'm sorry, I couldn't find anything useful in the system.",
        system_prompt: str | None = None,
        tools: List | None = None,
    ):
        # Dependency injection with sensible defaults
        from telecomcall.stt.utils import get_stt_model
        from telecomcall.tts.utils import get_tts_model

        self._stt_model = stt_model or get_stt_model(settings.stt_model)
        self._tts_model = tts_model or get_tts_model(settings.tts_model)
        self._voice_effect = voice_effect or get_sound_effect()

        # Create the React agent directly inside the class
        self._react_agent = self._create_react_agent(
            system_prompt=system_prompt,
            tools=tools,
        )

        # Configuration
        self._thread_id = thread_id
        self._fallback_message = fallback_message
        self._tool_use_message = tool_use_message
        self._sound_effect_seconds = sound_effect_seconds

        # Build the FastRTC Stream with the handler
        self._stream = self._build_stream()

    def _create_react_agent(
        self,
        system_prompt: str | None = None,
        tools: List | None = None,
    ):
        """Create and return a LangChain agent with Groq + InMemorySaver + tools."""
        llm = ChatGroq(
            model=settings.groq.model,
            api_key=settings.groq.api_key,
        )

        system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        tools = tools or [search_plan_mock_tool]

        agent = create_agent(
            llm,
            checkpointer=InMemorySaver(),
            system_prompt=system_prompt,
            tools=tools,
        )
        return agent

    def _build_stream(self) -> Stream:
        """Build and configure the FastRTC Stream with the agent handler."""

        async def handler_wrapper(audio: AudioChunk) -> AsyncIterator[AudioChunk]:
            """Handler that uses instance variables directly."""
            async for chunk in self._process_audio(audio):
                yield chunk

        return Stream(
            handler=ReplyOnPause(handler_wrapper),
            modality="audio",
            mode="send-receive",
        )

    async def _process_audio(
        self,
        audio: AudioChunk,
    ) -> AsyncIterator[AudioChunk]:
        """
        Process audio input through the complete pipeline:
        STT -> Agent Reasoning -> TTS with effects.
        """
        # Step 1: Transcribe audio to text
        transcription = await self._transcribe(audio)
        logger.info(f"Transcription: {transcription}")

        # Step 2: Process with agent and stream responses
        async for audio_chunk in self._process_with_agent(transcription):
            if audio_chunk is not None:
                yield audio_chunk

        # Step 3: Speak final answer
        final_response = await self._get_final_response()
        logger.info(f"Final response: {final_response}")

        if final_response:
            async for audio_chunk in self._synthesize_speech(final_response):
                yield audio_chunk

    async def _transcribe(self, audio: AudioChunk) -> str:
        """Transcribe audio to text using STT model."""
        return self._stt_model.stt(audio)

    async def _process_with_agent(
        self,
        transcription: str,
    ) -> AsyncIterator[Optional[AudioChunk]]:
        """Process transcription through the agent and handle tool calls."""
        final_text: str | None = None

        for chunk in self._react_agent.stream(
            {"messages": [{"role": "user", "content": transcription}]},
            {"configurable": {"thread_id": self._thread_id}},
            stream_mode="updates",
        ):
            for step, data in chunk.items():
                # Handle tool calls
                if step == "model" and model_has_tool_calls(data):
                    async for audio_chunk in self._synthesize_speech(
                        self._tool_use_message
                    ):
                        yield audio_chunk

                    if self._sound_effect_seconds > 0:
                        async for effect_chunk in self._play_sound_effect():
                            yield effect_chunk

                    await asyncio.sleep(0)

                # Capture final text from model response
                if step == "model":
                    final_text = self._extract_final_text(data)

        self._last_final_text = final_text

    def _extract_final_text(self, model_step_data) -> Optional[str]:
        """Extract the final text response from model step data."""
        msgs = model_step_data.get("messages", [])
        if isinstance(msgs, list) and len(msgs) > 0:
            return getattr(msgs[0], "content", None)
        return None

    async def _get_final_response(self) -> str:
        """Get the final response text to speak to the user."""
        return getattr(self, "_last_final_text", None) or self._fallback_message

    async def _synthesize_speech(self, text: str) -> AsyncIterator[AudioChunk]:
        """Convert text to speech audio chunks."""
        async for audio_chunk in self._tts_model.stream_tts(text):
            yield audio_chunk

    async def _play_sound_effect(self) -> AsyncIterator[AudioChunk]:
        """Play the configured sound effect."""
        async for effect_chunk in self._voice_effect.stream():
            yield effect_chunk

    @property
    def stream(self) -> Stream:
        """Expose the FastRTC Stream instance."""
        return self._stream

    @property
    def stt_model(self):
        return self._stt_model

    @property
    def tts_model(self):
        return self._tts_model

    @property
    def react_agent(self):
        return self._react_agent

    @property
    def voice_effect(self):
        return self._voice_effect

    def set_thread_id(self, thread_id: str) -> None:
        self._thread_id = thread_id

    def set_fallback_message(self, message: str) -> None:
        self._fallback_message = message

    def set_tool_use_message(self, message: str) -> None:
        self._tool_use_message = message

    def set_sound_effect_seconds(self, seconds: float) -> None:
        self._sound_effect_seconds = seconds
