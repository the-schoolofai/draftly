# Draftly - API

The backend for Draftly. A LangChain agent (`create_agent`) turns a short idea into a complete email draft: subject line, greeting, body, and sign-off. FastAPI will serve it to the web app.

| File | What it is |
|---|---|
| `app/agent.py` | The Draftly agent: the playground baseline, run as a CLI chat |
| `app/main.py` | The FastAPI app (currently a `GET /` hello route; agent endpoints come next) |

**Agent stack**

- **Model:** cloud LLM from `.env` via `init_chat_model` (default `google_genai:gemini-3.5-flash-lite`)
- **Tool:** `get_today_date`, called when the email needs the current date
- **Memory:** PostgreSQL checkpointer (`PostgresSaver`) keyed by `thread_id`
- **Middleware:** `SummarizationMiddleware` summarizes long conversations

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- A model API key (Google Gemini by default)
- PostgreSQL running locally (needed by `app/agent.py`)

## Setup

```bash
cd draftly
cd api

uv sync                 # creates .venv/ and installs deps from uv.lock
cp .env.example .env    # then fill in your values
```

`.env`:

```env
DRAFTLY_LLM_MODEL=google_genai:gemini-3.5-flash-lite
DRAFTLY_API_KEY=your-api-key
DRAFTLY_DB_URI=postgresql://postgres:your%40password@localhost:5432/test?sslmode=disable
```

| Variable | Purpose |
|---|---|
| `DRAFTLY_LLM_MODEL` | `provider:model` string for `init_chat_model` |
| `DRAFTLY_API_KEY` | Provider API key |
| `DRAFTLY_DB_URI` | PostgreSQL connection string. URL-encode special characters in the password (`@` → `%40`) |

No Postgres yet? Start one with Docker:

```bash
docker run -d --name draftly-pg -e POSTGRES_PASSWORD=yourpassword -e POSTGRES_DB=test -p 5432:5432 postgres:17
```

## Run

All commands run from inside `api/`, because the code loads `.env` from the current folder.

### 1. Agent (CLI chat)

```bash
uv run app/agent.py
```

```
Conversation name: leave-request
You: ask my manager for leave this Friday, mention today's date
Draftly: Subject: Leave Request for Friday ...
You: make it shorter
Draftly: Subject: Friday Off Request ...
You: quit
```

Use the same **Conversation name** again later to continue that thread; the history is stored in Postgres. Type `quit`, `exit` or `bye` to stop.

### 2. API server (FastAPI)

```bash
uv run fastapi dev app/main.py    # development: auto-reload on save
uv run fastapi run app/main.py    # production mode: no reload, listens on 0.0.0.0
```

| URL | What |
|---|---|
| http://127.0.0.1:8000 | API root (`GET /` → `{"Hello": "World"}`) |
| http://127.0.0.1:8000/docs | Swagger UI: try the endpoints in the browser |
| http://127.0.0.1:8000/redoc | ReDoc reference docs |

Use a different port with `--port 8001`.

## Daily uv commands

| Task | Command |
|---|---|
| Install / update deps after a pull | `uv sync` |
| Add a package | `uv add langchain-anthropic` |
| Remove a package | `uv remove langchain-anthropic` |
| Run any script | `uv run <file>.py` |

> Learning how the agent is built? Each concept has its own step in [`../playground`](../playground/README.md).
