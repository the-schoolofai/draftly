# Draftly

An AI email draft agent. Type a short idea (e.g. *"ask my manager for Friday off"*) and Draftly writes a complete email with a subject line, greeting, body, and sign-off, matching the tone to the request. Missing details become placeholders like `[Name]`.

Under the hood it's a LangChain agent (`create_agent`) running `gemma4:31b-cloud` through Ollama, with a `get_today_date` tool it can call when the email needs the current date.

| Folder | Stack |
|---|---|
| `api/` | Python, FastAPI, LangChain agent |
| `web/` | Next.js |
| `playground/` | Standalone LangChain scripts that build the Draftly agent step by step |

## Quick start

```bash
# API
cd api && uv sync
uv run app/main.py

# Web
cd web && npm install
npm run dev
```

## Playground

`playground/` is where the Draftly agent is built up one concept at a time. Each script runs on its own:

| Step | Concept |
|---|---|
| `agent_00.py` | Plain LLM call (`init_chat_model`) |
| `agent_01.py` | First agent: `create_agent` + Draftly system prompt |
| `agent_02.py` | Cloud model and API key from `.env` |
| `agent_03.py` | Chat loop with manual memory |
| `agent_04.py` | Checkpointer memory (`InMemorySaver` + `thread_id`) |
| `agent_05.py` | Persistent memory (`SqliteSaver`) |
| `agent_06.py` | Production memory (`PostgresSaver`) |
| `agent_07.py` | Middleware (`SummarizationMiddleware`) |
| `agent.py` | Draftly baseline: every step combined + `get_today_date` tool |

```bash
cd playground
uv venv .play && source .play/bin/activate
uv sync --active
cp .env.example .env          # add your model, API key, DB URI
uv run --active agent.py
```

See [`playground/README.md`](playground/README.md) for the full learning path, setup (Ollama, `.env`, Postgres) and run order.
