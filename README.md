# Draftly

An AI email draft agent. Type a short idea (e.g. *"ask my manager for Friday off"*) and Draftly writes a complete email with a subject line, greeting, body, and sign-off, matching the tone to the request. Missing details become placeholders like `[Name]`.

Under the hood it's a LangChain agent (`create_agent`) running `gemma4:31b-cloud` through Ollama, with a `get_today_date` tool it can call when the email needs the current date.

| Folder | Stack |
|---|---|
| `api/` | Python, FastAPI, LangChain agent |
| `web/` | Next.js |

## Quick start

```bash
# API
cd api && uv sync
uv run app/main.py

# Web
cd web && npm install
npm run dev
```
