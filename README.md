# TelecomCall - AI Voice Mobile Carrier Assistant

An AI voice assistant that replaces human call center agents for mobile carriers. Users call a phone number and the AI agent handles plan inquiries, billing questions, technical support, and account management.

## Tech Stack

- **Agent**: LangGraph + Groq LLM
- **Voice I/O**: FastRTC + Gradio (browser testing) + Twilio (phone calls)
- **Vector Search**: Qdrant (local Docker)
- **STT**: Moonshine (local)
- **TTS**: Kokoro (local)
- **Observability**: Opik

## Getting Started

1. Copy `.env.example` to `.env` and fill in your API keys
2. Install dependencies: `uv sync`
3. Run the test script: `uv run python scripts/test_llm.py`
4. Start the voice agent: `uv run python scripts/test_voice.py`
5. Start the call center: `make start-call-center`

## Project Structure

```
src/telecomcall/
├── agent/           # LangGraph agent + tools
├── api/             # FastAPI app + routes
├── infrastructure/  # Qdrant/Superlinked integration
├── observability/   # Opik tracing
├── stt/             # Speech-to-Text models
├── tts/             # Text-to-Speech models
├── config.py        # Pydantic settings
└── voice.py         # Sound effects
```

## License

MIT
