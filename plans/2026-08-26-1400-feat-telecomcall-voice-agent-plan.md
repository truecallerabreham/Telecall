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
  - `pyproject.toml`, `.env.example`, `.gitignore`, `Makefile`, `README.md`
  - `src/telecomcall/config.py`
  - All `__init__.py` files
  - `scripts/test_llm.py`
- **Micro-milestones:**
  - 1.1 Create directory structure — DONE
  - 1.2 Create pyproject.toml — DONE
  - 1.3 Create .env.example — DONE
  - 1.4 Create .gitignore — DONE
  - 1.5 Create README.md — DONE
  - 1.6 Create config.py — DONE
  - 1.7 Create Makefile — DONE
  - 1.8 Create test_llm.py — **DONE** (LLM responded successfully)

### U2. Core Agent

- **Goal:** Create a LangGraph agent with a mock plan search tool.
- **Requirements:** R6, R7, R9
- **Dependencies:** U1
- **Micro-milestones:**
  - 2.1 Create agent/utils.py
  - 2.2 Create agent/tools/plan_search.py
  - 2.3 Create test_agent.py — **[MILESTONE GOAL]**

### U3. Voice Layer

- **Goal:** Implement STT, TTS, sound effects, and FastRTC agent class.
- **Requirements:** R2, R3, R4, R5
- **Dependencies:** U2
- **Micro-milestones:**
  - 3.1 Create stt/base.py
  - 3.2 Create stt/local/moonshine.py
  - 3.3 Create stt/utils.py
  - 3.4 Create tts/base.py
  - 3.5 Create tts/local/kokoro.py
  - 3.6 Create tts/utils.py
  - 3.7 Create voice.py
  - 3.8 Create agent/fastrtc_agent.py
  - 3.9 Create test_voice.py — **[MILESTONE GOAL]**

### U4. FastAPI + Twilio

- **Goal:** Create FastAPI app with Twilio webhook routes.
- **Requirements:** R1, R16
- **Dependencies:** U3
- **Micro-milestones:**
  - 4.1 Create api/main.py
  - 4.2 Create api/routes/voice.py
  - 4.3 Create scripts/make_outbound_call.py
  - 4.4 Test FastAPI health — **[MILESTONE GOAL]**
  - 4.5 Create Dockerfile
  - 4.6 Create docker-compose.yml

### U5. Telecom Data

- **Goal:** Create mock telecom data.
- **Requirements:** R10
- **Dependencies:** None
- **Micro-milestones:**
  - 5.1 Create data/mock_plans.json
  - 5.2 Create data/mock_customers.json
  - 5.3 Create data/mock_support_tickets.json
  - 5.4 Create data/mock_billing.json — **[MILESTONE GOAL]**

### U6. Semantic Search

- **Goal:** Set up Qdrant and ingest data.
- **Requirements:** R11, R12
- **Dependencies:** U5
- **Micro-milestones:**
  - 6.1 Create infrastructure/superlinked/service.py
  - 6.2 Test ingestion and search — **[MILESTONE GOAL]**

### U7. Multi-turn Memory

- **Goal:** Conversation state management.
- **Requirements:** R8
- **Dependencies:** U3
- **Micro-milestones:**
  - 7.1 Update fastrtc_agent.py
  - 7.2 Test multi-turn — **[MILESTONE GOAL]**

### U8. Billing & Support Tools

- **Goal:** Agent tools for data access.
- **Requirements:** R7, R12
- **Dependencies:** U5, U6
- **Micro-milestones:**
  - 8.1 Create customer_lookup.py
  - 8.2 Create billing_lookup.py
  - 8.3 Create support_tickets.py
  - 8.4 Update plan_search.py
  - 8.5 Test all tools — **[MILESTONE GOAL]**

### U9. Analytics Dashboard

- **Goal:** Opik integration and Gradio dashboard.
- **Requirements:** R13, R14
- **Dependencies:** U3, U8
- **Micro-milestones:**
  - 9.1 Create observability/opik_tracer.py
  - 9.2 Test dashboard — **[MILESTONE GOAL]**

### U10. Polish & Deploy

- **Goal:** Final integration and documentation.
- **Requirements:** R15, R16, R17
- **Dependencies:** U1-U9
- **Micro-milestones:**
  - 10.1 Update docker-compose.yml
  - 10.2 Update Makefile
  - 10.3 Update README.md
  - 10.4 Test end-to-end — **[MILESTONE GOAL]**

---

## Verification Contract

| Gate | Command | Applies to |
|------|---------|------------|
| LLM connectivity | `uv run python scripts/test_llm.py` | U1 |
| Agent response | `uv run python scripts/test_agent.py` | U2 |
| Voice chat | `uv run python scripts/test_voice.py` | U3 |
| FastAPI health | `curl http://localhost:8000/health` | U4 |
| Qdrant health | `curl http://localhost:6333/healthz` | U6 |
| Data ingestion | `uv run python scripts/ingest_plans.py` | U6 |
| Dashboard | `uv run python scripts/test_dashboard.py` | U9 |
| End-to-end | `uv run python scripts/test_e2e.py` | U10 |

---

## Definition of Done

- [ ] All 10 phases complete with working milestones
- [ ] Phone call to Twilio number connects and gets AI response
- [ ] Gradio browser voice chat works
- [ ] Analytics dashboard displays logged queries
- [ ] All tests pass
- [ ] Docker Compose starts all services
- [ ] README documents setup and usage
