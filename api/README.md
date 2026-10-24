# Draftly - API

The backend for Draftly. A LangChain agent (`create_agent`) that turns a short idea into a complete email draft: subject line, greeting, body, and sign-off.

- **Model:** `gemma4:31b-cloud` via Ollama
- **Tool:** `get_today_date`, which the agent calls when the email needs the current date

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com/), signed in so it can run cloud models

## Run

```bash
uv sync
uv run app/main.py
```

Type your idea when prompted:

```
Enter email draft idea: ask my manager for Friday off
```

> For now the agent runs as a CLI script. FastAPI endpoints for the web app come next.
