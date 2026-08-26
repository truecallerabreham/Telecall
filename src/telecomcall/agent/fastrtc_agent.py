"""Voice agent pipeline - STT -> Agent -> TTS."""

import asyncio
from typing import AsyncIterator, List, Optional, Tuple

import numpy as np
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from loguru import logger

from telecomcall.agent.tools.plan_search import search_plan_mock_tool
from telecomcall.agent.utils import model_has_tool_calls
from telecomcall.config import settings
from telecomcall.stt.utils import get_stt_model
from telecomcall.tts.utils import get_tts_model
from telecomcall.voice import get_sound_effect

AudioChunk = Tuple[int, np.ndarray]

DEFAULT_SYSTEM_PROMPT = """
Your name is Lisa, and you work for TelecomCo mobile carrier company.
Your task is to provide information about mobile plans using the `search_plan_mock_tool`.
Don't use asterisks or emojis, as you are engaged in a phone call. Just return short and informative responses.
""".strip()


class VoiceAgent:
    """
    Voice agent pipeline: STT -> Agent -> TTS.
    No fastrtc or torch required - uses cloud APIs.
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
        self._stt_model = stt_model or get_stt_model(settings.stt_model)
        self._tts_model = tts_model or get_tts_model(settings.tts_model)
        self._voice_effect = voice_effect or get_sound_effect()

        self._react_agent = self._create_react_agent(
            system_prompt=system_prompt,
            tools=tools,
        )

        self._thread_id = thread_id
        self._fallback_message = fallback_message
        self._tool_use_message = tool_use_message
        self._sound_effect_seconds = sound_effect_seconds

    def _create_react_agent(self, system_prompt=None, tools=None):
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

    async def process_audio(self, audio: bytes, sample_rate: int = 16000) -> str:
        """Process incoming audio: transcribe -> agent -> return text response."""
        transcription = self._stt_model.stt(audio, sample_rate)
        logger.info(f"Transcription: {transcription}")

        response = await self._get_agent_response(transcription)
        logger.info(f"Agent response: {response}")
        return response

    async def _get_agent_response(self, text: str) -> str:
        """Get agent response for text input."""
        result = self._react_agent.invoke(
            {"messages": [{"role": "user", "content": text}]},
            {"configurable": {"thread_id": self._thread_id}},
        )

        for msg in reversed(result["messages"]):
            if hasattr(msg, "content") and msg.content:
                return msg.content

        return self._fallback_message

    async def text_to_speech(self, text: str) -> AudioChunk:
        """Convert text to audio."""
        async for chunk in self._tts_model.stream_tts(text):
            return chunk
        return (24000, np.zeros(24000, dtype=np.int16))

    async def chat(self, user_text: str) -> str:
        """Simple text chat - returns text response."""
        return await self._get_agent_response(user_text)

    @property
    def stt_model(self):
        return self._stt_model

    @property
    def tts_model(self):
        return self._tts_model

    @property
    def react_agent(self):
        return self._react_agent

    def set_thread_id(self, thread_id: str) -> None:
        self._thread_id = thread_id
