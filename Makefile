ifeq (,$(wildcard .env))
$(error .env file is missing. Please create one based on .env.example)
endif

include .env

CHECK_DIRS := src/

# --- Ruff ---

format-fix:
	uv run ruff format $(CHECK_DIRS)
	uv run ruff check --select I --fix

lint-fix:
	uv run ruff check --fix $(CHECK_DIRS)

format-check:
	uv run ruff format --check $(CHECK_DIRS)
	uv run ruff check -e $(CHECK_DIRS)
	uv run ruff check --select I -e

lint-check:
	uv run ruff check $(CHECK_DIRS)

# --- Run Gradio ---

start-gradio-application:
	uv run python scripts/test_voice.py

# --- Qdrant Ingestion ---

ingest-plans:
	uv run python scripts/ingest_plans.py

# --- Outbound Calls ---

outbound-call:
	uv run python scripts/make_outbound_call.py

# --- Application Local Deployment ---

start-call-center:
	docker compose up --build -d

stop-call-center:
	docker compose down

delete-call-center:
	docker compose down -v

start-ngrok-tunnel:
	@echo "Starting ngrok tunnel on port 8000..."
	@echo "Remember to close the tunnel when you're done!"
	sleep 5
	ngrok http 8000
