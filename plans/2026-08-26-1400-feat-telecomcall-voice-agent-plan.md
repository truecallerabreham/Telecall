---
title: TelecomCall - AI Voice Mobile Carrier Assistant - Plan
type: feat
date: 2026-08-26
artifact_contract: ce-unified-plan/v1
artifact_readiness: implementation-ready
product_contract_source: ce-plan-bootstrap
execution: code
---

# TelecomCall - AI Voice Mobile Carrier Assistant - Plan

## Goal Capsule

- **Objective:** Users can call a phone number and converse with an AI assistant that answers mobile carrier questions (plans, billing, support) using natural voice, with the full conversation logged and queryable in an analytics dashboard.
- **Means:** LangGraph agent on Groq LLM, local STT/TTS via FastRTC, Twilio for phone connectivity, Qdrant for semantic search, Opik for observability. (session-settled: user-directed — chosen over cloud STT/TTS and other LLMs: free tier, local-first, no credit card required)
- **Authority hierarchy:** The plan is the authority. If implementation discovers a conflict between plan decisions and runtime reality, surface it rather than guessing.
- **Stop conditions:** All 10 phases complete, voice call works end-to-end on real phone number, analytics dashboard shows logged queries.
- **Execution profile:** Incremental phase-by-phase delivery. Each phase produces a working milestone.
- **Tail ownership:** Implementation agent owns the commit trail; plan owner owns scope.

---

## Product Contract

### Summary

TelecomCall replaces human call center agents for mobile carriers with an AI voice assistant. Users call a real Twilio phone number, the AI answers, and handles plan inquiries, billing questions, technical support, and account management through natural conversation. A Gradio browser interface is available for development testing.

### Problem Frame

Mobile carrier call centers handle millions of calls daily for routine questions — plan details, billing inquiries, support tickets. This is expensive, slow, and inconsistent. TelecomCall demonstrates an AI-first alternative: a voice agent that understands natural speech, searches a knowledge base of carrier data, and responds with synthesized speech — all accessible via a simple phone call.

### Requirements

#### Voice Interaction

- R1. The system accepts incoming phone calls via Twilio and routes audio to the AI agent.
- R2. Speech-to-text converts caller audio to text using a local Moonshine model.
- R3. Text-to-speech converts agent responses to audio using a local Kokoro model.
- R4. The system supports browser-based voice chat via Gradio for development testing.
- R5. Audio processing round-trip (speech in → speech out) completes within 3 seconds on local hardware.

#### Agent Intelligence

- R6. A LangGraph agent powered by Groq LLM processes user queries and generates responses.
- R7. The agent has access to tools: plan search, customer lookup, billing lookup, support ticket management.
- R8. The agent maintains multi-turn conversation memory within a single call session.
- R9. The agent uses a telecom-specific system prompt and responds in a natural, phone-appropriate manner.

#### Data & Search

- R10. Mock telecom data (plans, customers, billing, support tickets) is stored in JSON files.
- R11. Data is ingested into Qdrant as vector embeddings for semantic search.
- R12. The agent retrieves relevant data through semantic search when answering queries.

#### Observability

- R13. All agent queries and responses are logged to Opik for analytics.
- R14. A Gradio dashboard displays logged queries with filtering and search capabilities.

#### Deployment

- R15. The system runs locally with Docker Compose (app + Qdrant).
- R16. The system connects to a real Twilio phone number for incoming calls.
- R17. All external services use free tiers (Groq, Twilio trial, local Qdrant).

### Scope Boundaries

#### In Scope

- Voice I/O via Twilio (phone) and Gradio (browser)
- LangGraph agent with tool calling
- Mock telecom data (plans, customers, billing, support)
- Semantic search via Qdrant
- Multi-turn conversation memory
- Opik observability and analytics dashboard
- Local development with Docker Compose

#### Deferred to Follow-Up Work

- Real carrier data integration
- Authentication and customer verification
- Payment processing
- Multi-language support
- Production deployment (cloud hosting, scaling)

#### Outside This Product's Identity

- Replacing all human agents (this is a focused demo)
- Real-time sentiment analysis during calls
- Video call support
- SMS/chat channel support

### Key Decisions

- **Session-settled:** Groq LLM over alternatives — free tier, fast inference, no credit card. Governs R6.
- **Session-settled:** Local STT/TTS (Moonshine + Kokoro) over cloud services — free, no API costs, privacy. Governs R2, R3.
- **Session-settled:** Twilio for phone connectivity — free trial sufficient, industry standard. Governs R1.
- **Session-settled:** Qdrant local Docker over cloud — free, no API key needed. Governs R11.
- **Session-settled:** Opik over alternatives — free tier, built-in LLM observability. Governs R13.
- **Session-settled:** Gradio for browser testing — already in FastRTC stack, minimal setup. Governs R4.

### Sources

- Course reference: `github.com/neural-maze/realtime-phone-agents-course`
- Architecture article: `theneuralmaze.substack.com/p/the-architecture-of-realtime-phone`
- FastRTC documentation
- LangGraph documentation
- Twilio API documentation

---

## Planning Contract

### Key Technical Decisions

- KTD1. **LangGraph agent architecture** — Use LangGraph's `create_agent` with `InMemorySaver` checkpoint for stateful multi-turn conversations. The agent receives audio, transcribes via STT, processes through the LLM with tool access, and synthesizes response via TTS. (session-settled: user-directed — chosen over raw LangChain agent: course proven pattern, checkpoint support for memory)

- KTD2. **FastRTC stream handler pattern** — Wrap the agent in a `ReplyOnPause` handler that processes audio chunks through the STT → Agent → TTS pipeline. The `FastRTCAgent` class encapsulates all dependencies and exposes a `Stream` object for both Gradio and Twilio integration. (session-settled: user-directed — chosen over direct WebSocket handling: course proven pattern, handles audio chunking automatically)

- KTD3. **Qdrant local-first vector search** — Run Qdrant in Docker alongside the app. Ingest mock data as vector embeddings. The agent's plan search tool queries Qdrant semantically rather than doing keyword matching. (session-settled: user-directed — chosen over in-memory search: scalable, persists across restarts, matches course architecture)

- KTD4. **Twilio media stream integration** — Use Twilio's `<Connect><Stream>` TwiML to bridge phone audio to the FastRTC handler via WebSocket. The FastAPI webhook returns TwiML that connects the call to the media stream endpoint. (session-settled: user-directed — chosen over Twilio's built-in <Gather>: real-time bidirectional audio, not turn-based)

- KTD5. **Tool-based data access** — Expose telecom data (plans, customers, billing, tickets) as LangChain tools that the agent can call. Each tool queries the relevant data source (Qdrant for search, JSON for direct lookups). (session-settled: user-directed — chosen over embedding all data in system prompt: scalable, keeps context window clean, allows dynamic queries)

- KTD6. **Opik tracing integration** — Use Opik's Python SDK to log agent queries, responses, tool calls, and latency metrics. The Gradio dashboard reads from Opik's API to display analytics. (session-settled: user-directed — chosen over custom logging: built-in dashboard, LLM-specific metrics, free tier)

### Assumptions

- Groq free tier provides sufficient API calls for development and demo.
- Twilio free trial supports incoming calls to the provisioned number.
- Local hardware (user's machine) can run Moonshine STT and Kokoro TTS with acceptable latency.
- Qdrant Docker container runs reliably on the user's machine.
- The user has Python 3.11+, Docker, and Git installed (confirmed).

### Implementation Constraints

- All external services must use free tiers (no credit card).
- Build from scratch — course code is reference only, not forked.
- Each phase produces a working, testable milestone.
- Code follows course architecture patterns but uses original implementation.

### Sequencing

The work is sequenced in 10 phases, each building on the previous:

1. **Project Foundation** — directory structure, config, dependencies
2. **Core Agent** — LangGraph agent with mock tool
3. **Voice Layer** — STT, TTS, sound effects, FastRTC agent class
4. **FastAPI + Twilio** — webhooks, outbound calls, Docker
5. **Telecom Data** — mock data creation
6. **Semantic Search** — Qdrant setup and data ingestion
7. **Multi-turn Memory** — conversation state management
8. **Billing & Support Tools** — agent tools for data access
9. **Analytics Dashboard** — Opik integration and Gradio UI
10. **Polish & Deploy** — Docker Compose, end-to-end testing

---

## Implementation Units

### U1. Project Foundation

- **Goal:** Establish the project structure, dependencies, and configuration that all subsequent phases build on.
- **Requirements:** R15, R17
- **Dependencies:** None
- **Files:**
  - `pyproject.toml` — project metadata and dependencies
  - `.env.example` — environment variable template
  - `.gitignore` — git ignore rules
  - `Makefile` — build and run commands
  - `README.md` — project documentation
  - `src/telecomcall/__init__.py` — package init
  - `src/telecomcall/config.py` — Pydantic settings
  - `src/telecomcall/agent/__init__.py` — agent package
  - `src/telecomcall/agent/tools/__init__.py` — tools package
  - `src/telecomcall/stt/__init__.py` — STT package
  - `src/telecomcall/stt/local/__init__.py` — local STT package
  - `src/telecomcall/tts/__init__.py` — TTS package
  - `src/telecomcall/tts/local/__init__.py` — local TTS package
  - `src/telecomcall/api/__init__.py` — API package
  - `src/telecomcall/api/routes/__init__.py` — routes package
  - `src/telecomcall/infrastructure/__init__.py` — infrastructure package
  - `src/telecomcall/infrastructure/superlinked/__init__.py` — Qdrant package
  - `src/telecomcall/observability/__init__.py` — observability package
  - `scripts/test_llm.py` — LLM connection test
- **Approach:** Create the full directory tree matching the course architecture. `pyproject.toml` includes all dependencies (FastRTC, LangGraph, Groq, Qdrant, Opik, Twilio, etc.). `config.py` uses Pydantic settings with nested models for Groq, Twilio, Qdrant, and Opik configuration. `test_llm.py` makes a basic Groq API call to verify connectivity.
- **Test scenarios:**
  - `uv sync` installs all dependencies without errors
  - `test_llm.py` prints an LLM response when run with valid API key
  - All `__init__.py` files exist and are importable
  - `config.py` loads settings from `.env` file
- **Verification:** Run `uv run python scripts/test_llm.py` and see a response from the LLM.

### U2. Core Agent

- **Goal:** Create a LangGraph agent with a mock plan search tool that can respond to plan queries.
- **Requirements:** R6, R7, R9
- **Dependencies:** U1
- **Files:**
  - `src/telecomcall/agent/utils.py` — `model_has_tool_calls()` helper
  - `src/telecomcall/agent/tools/plan_search.py` — mock plan search tool
  - `scripts/test_agent.py` — agent test script
- **Approach:** Implement `model_has_tool_calls()` heuristic that detects tool calls in model step data. Create a mock `search_plan_mock_tool` using LangChain's `@tool` decorator. `test_agent.py` creates a LangGraph agent with Groq LLM, InMemorySaver checkpointer, and the mock tool, then tests with a plan query.
- **Test scenarios:**
  - Agent responds to "what plans do you have?" using the mock tool
  - Tool call detection works for different message formats
  - Agent maintains conversation state across multiple invocations
- **Verification:** Run `uv run python scripts/test_agent.py` and see the agent invoke the tool and respond with plan information.

### U3. Voice Layer

- **Goal:** Implement STT, TTS, sound effects, and the FastRTC agent class that wraps everything into a voice-processing pipeline.
- **Requirements:** R2, R3, R4, R5
- **Dependencies:** U2
- **Files:**
  - `src/telecomcall/stt/base.py` — abstract STT base class
  - `src/telecomcall/stt/local/moonshine.py` — Moonshine STT implementation
  - `src/telecomcall/stt/utils.py` — STT model factory
  - `src/telecomcall/tts/base.py` — abstract TTS base class
  - `src/telecomcall/tts/local/kokoro.py` — Kokoro TTS implementation
  - `src/telecomcall/tts/utils.py` — TTS model factory
  - `src/telecomcall/voice.py` — sound effects (keyboard background)
  - `src/telecomcall/agent/fastrtc_agent.py` — FastRTCAgent class
  - `scripts/test_voice.py` — browser voice chat test
- **Approach:** Abstract STT/TTS behind base classes for flexibility. Moonshine and Kokoro implementations wrap FastRTC's model getters. `FastRTCAgent` class encapsulates the full pipeline: STT → Agent → TTS with sound effects. It creates the LangGraph agent internally, builds a `ReplyOnPause` handler, and exposes a `Stream` object. `test_voice.py` launches the Gradio UI.
- **Test scenarios:**
  - STT transcribes audio input to text
  - TTS converts text to audio output
  - FastRTCAgent processes audio through the full pipeline
  - Gradio UI launches and accepts voice input
  - Audio round-trip completes within 3 seconds
- **Verification:** Run `uv run python scripts/test_voice.py`, open the Gradio URL, speak into the microphone, and hear the agent respond.

### U4. FastAPI + Twilio

- **Goal:** Create the FastAPI application with Twilio webhook routes and Docker configuration for production deployment.
- **Requirements:** R1, R16
- **Dependencies:** U3
- **Files:**
  - `src/telecomcall/api/main.py` — FastAPI app creation
  - `src/telecomcall/api/routes/voice.py` — Twilio webhook routes
  - `scripts/make_outbound_call.py` — outbound call script
  - `Dockerfile` — production container
  - `docker-compose.yml` — app + Qdrant services
- **Approach:** FastAPI app with CORS middleware and voice routes. `/voice/webhook` and `/voice/incoming` return TwiML with `<Connect><Stream>` to bridge phone audio to FastRTC. `/voice/status` handles call status updates. `make_outbound_call.py` uses Twilio SDK to initiate calls. Docker Compose runs the app and Qdrant containers.
- **Test scenarios:**
  - FastAPI app starts and responds to health check
  - `/voice/webhook` returns valid TwiML XML
  - Outbound call script connects to a phone number
  - Docker Compose starts both services
- **Verification:** Run `uv run uvicorn telecomcall.api.main:app` and hit `/health` endpoint. Test webhook returns TwiML.

### U5. Telecom Data

- **Goal:** Create realistic mock data for a mobile carrier: plans, customers, support tickets, and billing records.
- **Requirements:** R10
- **Dependencies:** None (parallel with U1-U4)
- **Files:**
  - `data/mock_plans.json` — 5 mobile carrier plans
  - `data/mock_customers.json` — 5 customer accounts
  - `data/mock_support_tickets.json` — 5 support tickets
  - `data/mock_billing.json` — 5 monthly invoices
- **Approach:** Create structured JSON data representing a realistic mobile carrier. Plans range from Starter ($29/mo) to Business Pro ($149/mo). Customers have varying plans, usage levels, and account statuses. Support tickets cover technical, billing, and account issues. Billing records show monthly charges with breakdowns.
- **Test scenarios:**
  - All JSON files are valid and parseable
  - Plan data includes required fields (price, data allowance, features)
  - Customer data references valid plan IDs
  - Billing data references valid customer IDs
- **Verification:** Load each JSON file in Python and verify structure with Pydantic models.

### U6. Semantic Search

- **Goal:** Set up Qdrant and ingest mock data as vector embeddings for semantic search.
- **Requirements:** R11, R12
- **Dependencies:** U5
- **Files:**
  - `src/telecomcall/infrastructure/superlinked/service.py` — Qdrant search service
  - `scripts/ingest_plans.py` — data ingestion script
  - `docker-compose.yml` — updated with Qdrant service
- **Approach:** Create a `QdrantSearchService` class that connects to Qdrant, creates collections, and performs semantic search. `ingest_plans.py` reads JSON data, generates embeddings (using a sentence transformer or Groq embeddings), and upserts into Qdrant. The agent's plan search tool queries this service.
- **Test scenarios:**
  - Qdrant container starts and responds to health check
  - Ingestion script creates collection and upserts documents
  - Search returns relevant results for natural language queries
  - Search handles empty results gracefully
- **Verification:** Run `docker compose up -d qdrant`, then `uv run python scripts/ingest_plans.py`, then query Qdrant API and see results.

### U7. Multi-turn Memory

- **Goal:** Ensure the agent maintains conversation state across multiple turns within a single call session.
- **Requirements:** R8
- **Dependencies:** U3
- **Files:**
  - `src/telecomcall/agent/fastrtc_agent.py` — updated with thread management
  - `scripts/test_agent.py` — updated with multi-turn test
- **Approach:** The LangGraph agent already uses `InMemorySaver` for checkpointing. Each call session gets a unique `thread_id` (from Twilio CallSid or generated for Gradio). The agent's state persists across multiple user messages within the same session. Update `FastRTCAgent` to accept and manage thread IDs properly.
- **Test scenarios:**
  - Agent remembers context from previous turns in the same session
  - Different sessions (thread_ids) are isolated from each other
  - Agent handles follow-up questions correctly
- **Verification:** Run a multi-turn test script that sends 3 messages to the same thread and verifies the agent references earlier context.

### U8. Billing & Support Tools

- **Goal:** Implement agent tools for accessing customer data, billing information, and support tickets.
- **Requirements:** R7, R12
- **Dependencies:** U5, U6
- **Files:**
  - `src/telecomcall/agent/tools/plan_search.py` — updated to use Qdrant
  - `src/telecomcall/agent/tools/customer_lookup.py` — customer data tool
  - `src/telecomcall/agent/tools/billing_lookup.py` — billing data tool
  - `src/telecomcall/agent/tools/support_tickets.py` — support ticket tool
  - `src/telecomcall/agent/fastrtc_agent.py` — updated with all tools
- **Approach:** Implement LangChain `@tool` decorated functions for each data access pattern. `plan_search` queries Qdrant semantically. `customer_lookup` searches by phone number or name. `billing_lookup` retrieves invoices by customer ID. `support_tickets` searches tickets by customer or status. Register all tools with the agent.
- **Test scenarios:**
  - Plan search returns relevant plans for natural language queries
  - Customer lookup finds customers by phone number
  - Billing lookup returns invoice details
  - Support ticket search finds tickets by customer
  - Agent correctly routes queries to appropriate tools
- **Verification:** Run agent test with queries like "what's my bill?", "find my account", "check my tickets" and verify correct tool invocation.

### U9. Analytics Dashboard

- **Goal:** Integrate Opik for observability and create a Gradio dashboard showing logged queries.
- **Requirements:** R13, R14
- **Dependencies:** U3, U8
- **Files:**
  - `src/telecomcall/observability/opik_tracer.py` — Opik tracing setup
  - `scripts/test_dashboard.py` — dashboard test script
- **Approach:** Use Opik's Python SDK to trace agent executions. Log each query, response, tool call, and latency metric. Create a Gradio dashboard that reads from Opik's API and displays: query list with timestamps, response times, tool usage breakdown, and a search/filter interface.
- **Test scenarios:**
  - Opik tracer logs agent queries successfully
  - Dashboard displays logged queries in a table
  - Dashboard filters work correctly
  - Latency metrics are captured accurately
- **Verification:** Run agent with Opik tracing, then open dashboard and see logged data.

### U10. Polish & Deploy

- **Goal:** Final integration, end-to-end testing, and documentation for the complete system.
- **Requirements:** R15, R16, R17
- **Dependencies:** U1-U9
- **Files:**
  - `docker-compose.yml` — final configuration
  - `Makefile` — updated with all commands
  - `README.md` — final documentation
  - `scripts/test_e2e.py` — end-to-end test
- **Approach:** Verify the complete pipeline: phone call → Twilio → FastRTC → agent → response → phone. Update Docker Compose with all services. Create comprehensive Makefile targets. Write setup and usage documentation. Test outbound and inbound calls.
- **Test scenarios:**
  - Docker Compose starts all services successfully
  - Inbound call to Twilio number connects to agent
  - Agent responds to voice queries over the phone
  - Analytics dashboard shows call data
  - All Makefile commands work correctly
- **Verification:** Call the Twilio phone number, ask about plans, hear the agent respond, then check the analytics dashboard.

---

## Verification Contract

| Gate | Command | Applies to |
|------|---------|------------|
| Unit tests | `uv run pytest tests/` | All U-IDs |
| LLM connectivity | `uv run python scripts/test_llm.py` | U1 |
| Agent response | `uv run python scripts/test_agent.py` | U2 |
| Voice chat | `uv run python scripts/test_voice.py` | U3 |
| FastAPI health | `curl http://localhost:8000/health` | U4 |
| Qdrant health | `curl http://localhost:6333/healthz` | U6 |
| Data ingestion | `uv run python scripts/ingest_plans.py` | U6 |
| Dashboard | `uv run python scripts/test_dashboard.py` | U9 |
| End-to-end | `uv run python scripts/test_e2e.py` | U10 |
| Lint | `uv run ruff check src/` | All U-IDs |

---

## Definition of Done

### Global

- [ ] All 10 phases complete with working milestones
- [ ] Phone call to Twilio number connects and gets AI response
- [ ] Gradio browser voice chat works
- [ ] Analytics dashboard displays logged queries
- [ ] All tests pass
- [ ] Lint passes with no errors
- [ ] Docker Compose starts all services
- [ ] README documents setup and usage

### Per-Unit

- U1: `uv sync` succeeds, `test_llm.py` returns response
- U2: `test_agent.py` shows tool invocation and response
- U3: `test_voice.py` launches Gradio, voice round-trip works
- U4: FastAPI health endpoint returns 200, TwiML is valid
- U5: All JSON files parse correctly
- U6: Qdrant returns search results for queries
- U7: Multi-turn test shows context preservation
- U8: Agent routes to correct tools for different query types
- U9: Dashboard displays traced data
- U10: Full phone call flow works end-to-end

---

## Appendix

### Course Reference Architecture

The implementation follows the course architecture studied in prior sessions:
- `fastrtc_agent.py` — core agent class (week1)
- `config.py` — Pydantic settings (week1)
- `voice.py` — sound effects (week1)
- `api/main.py` — FastAPI app (week4)
- `api/routes/voice.py` — Twilio routes (week4)
- `infrastructure/superlinked/service.py` — Qdrant service (week4)
- `docker-compose.yml` — container orchestration (week4)

### Tech Stack Versions

- Python 3.11+
- FastRTC (latest)
- LangGraph + LangChain (latest)
- Groq API (openai/gpt-oss-20b model)
- Qdrant v1.17.4 (Docker)
- Twilio (latest Python SDK)
- Opik (latest)
- Moonshine STT (via FastRTC)
- Kokoro TTS (via FastRTC)
