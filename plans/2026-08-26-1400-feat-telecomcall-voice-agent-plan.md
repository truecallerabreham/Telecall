---
title: "TelecomCall - AI Voice Mobile Carrier Assistant - Plan"
type: feat
date: 2026-08-26
topic: telecomcall-voice-agent
artifact_contract: ce-unified-plan/v1
artifact_readiness: requirements-only
product_contract_source: ce-brainstorm
execution: code
---

# TelecomCall - AI Voice Mobile Carrier Assistant - Plan

## Goal Capsule

**Objective:** A phone number a user can call where an AI agent answers and helps with mobile carrier questions — plans, pricing, billing, technical support — using the exact same architecture as the Neural Maze realtime-phone-agents-course, rebranded as an original portfolio product.

**Product Authority:** This plan owns the full product from project scaffolding through deployment. The tech stack is locked: FastRTC + LangGraph + Groq + Qdrant + Moonshine + Kokoro + Twilio (free trial) + Opik.

**Open Blockers:** None. All decisions settled.

## Product Contract

### Summary

TelecomCall is an AI voice assistant that replaces human call center agents for mobile carriers. Users call a phone number (via Twilio free trial), and the agent handles plan inquiries, billing questions, technical support, and account management. The architecture mirrors the Neural Maze course exactly — rebranded and rebuilt from scratch with a call analytics dashboard as the portfolio differentiator.

### Key Decisions

1. **Sector: Mobile carrier call center** (session-settled: user-directed — chosen over e-commerce, restaurants, real estate: user wants to replace human call centers, which is a $340B+ industry)

2. **Phone-first, not browser-first** (session-settled: user-directed — chosen over browser voice chat: user wants a real product you can call, not a browser demo)

3. **Build from scratch, course as reference** (session-settled: user-directed — chosen over forking week1: user wants original work for portfolio)

4. **Call analytics dashboard as portfolio differentiator** (session-settled: user-directed — chosen over multi-persona or sentiment escalation: shows production thinking)

5. **Free resources only** (session-settled: user-directed — no RunPod, no Qdrant Cloud, no Together AI. Twilio free trial OK)

6. **LLM: Groq free tier + Ollama local** (session-settled: user-approved — flexible approach, both options available)

7. **Micro-milestone build style** (session-settled: user-directed — brick by brick, each step shown with code, run it, see result, screenshot at milestone goals)

### Requirements

**Core Voice Agent**
- R1. Agent answers incoming phone calls via Twilio
- R2. Agent processes voice through STT (Moonshine) → LangGraph → TTS (Kokoro) pipeline
- R3. Agent responds with natural-sounding speech
- R4. Agent handles multi-turn conversations with memory

**Telecom Domain**
- R5. Agent can list available mobile plans from a catalog
- R6. Agent can search plans by attributes (price, data, features)
- R7. Agent can compare two plans
- R8. Agent can explain billing components
- R9. Agent can provide basic technical troubleshooting
- R10. Agent can suggest upgrade paths

**Semantic Search**
- R11. Plans indexed in Qdrant for vector search
- R12. Agent handles natural language queries ("I need lots of data for cheap")
- R13. Search works via Superlinked framework

**Analytics Dashboard**
- R14. Every call traced in Opik (STT time, LLM time, TTS time, tool calls)
- R15. Dashboard shows call metrics (latency, transcription quality, tool usage)
- R16. Conversation history stored and searchable

**Deployment**
- R17. Runs locally via Docker Compose (Qdrant + app)
- R18. Exposed via ngrok for Twilio integration
- R19. Deployable to Render free tier

**Observability**
- R20. Opik tracing on every agent step
- R21. Call recording and transcription storage

### Key Flows

**F1. Incoming Call Flow**
User dials Twilio number → Twilio connects to FastAPI server → FastRTC WebSocket handles audio → Moonshine STT transcribes → LangGraph agent processes with tools → Kokoro TTS generates response → Audio streams back to caller

**F2. Plan Search Flow**
User asks "what plans do you have?" → STT transcribes → Agent recognizes plan query → Agent calls plan_search_tool → Tool queries Qdrant via Superlinked → Returns matching plans → Agent formats response → TTS speaks answer

**F3. Multi-turn Flow**
User: "I need a plan with lots of data" → Agent finds data plans → User: "What about the cheaper one?" → Agent uses conversation history to understand "the cheaper one" refers to previous results → Agent filters and responds

**F4. Analytics Flow**
Agent processes call → Opik captures each step (STT, LLM, tool calls, TTS) with timing → Data stored in Opik → Dashboard endpoint aggregates and displays metrics

### Acceptance Examples

**AE1. Basic plan inquiry**
- User calls the number
- Agent: "Thank you for calling TelecomCo. My name is Lisa. How can I help you today?"
- User: "What plans do you have?"
- Agent lists 3-5 plans with names and prices
- Screenshot: Agent responding with plan list

**AE2. Semantic search**
- User: "I need a plan with at least 50GB data for under $40"
- Agent finds matching plans from catalog
- Agent: "I found the Perfect Data plan with 60GB for $35 a month. Would you like to know more?"
- Screenshot: Agent with search results

**AE3. Multi-turn conversation**
- Turn 1: User asks about plans
- Turn 2: User asks "What about the cheaper one?" (agent remembers context)
- Turn 3: User asks "Does it include international calling?"
- Agent handles all follow-ups correctly
- Screenshot: 5-turn conversation in Opik dashboard

**AE4. Phone call demo**
- User dials the Twilio number from their phone
- Agent answers and handles the conversation
- Full conversation visible in Opik dashboard
- Screenshot: Working phone call + dashboard

### Scope Boundaries

**In scope (this plan):**
- Phone-callable AI agent for mobile carrier
- Plan search, billing, troubleshooting, upgrade tools
- Qdrant + Superlinked semantic search
- Opik analytics dashboard
- Docker Compose local deployment
- Twilio free trial integration

**Deferred to later:**
- Real carrier API integration (account lookup, billing API)
- Outbound calls (calling customers back)
- Multiple agent personas
- Sentiment-aware escalation to human agents
- Payment processing
- Production deployment (beyond free tier)

**Outside this product's identity:**
- This is a portfolio project, not a production telecom system
- No real carrier data — uses synthetic plan catalog
- No real billing integration — uses mock billing tool

### Dependencies / Assumptions

- **D1.** Groq API key required (free tier, no credit card)
- **D2.** Twilio account required (free trial, no credit card)
- **D3.** Docker required for Qdrant
- **D4.** Python 3.11+ required
- **D5.** Machine needs ~8GB RAM for local STT/TTS models
- **A1.** Course code is MIT licensed — rebranding and restructuring is permitted
- **A2.** Free tier limits are sufficient for portfolio demos

### Outstanding Questions

None — all decisions settled in conversation.
