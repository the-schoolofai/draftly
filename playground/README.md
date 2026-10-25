# Draftly Playground

Standalone LangChain scripts that build the **Draftly AI email draft agent** one concept at a time.
Each file runs on its own. Read and run them **in order**: every step keeps what the step before it had and adds one new idea.

> Type a short idea (e.g. *"ask my manager for Friday off"*) and Draftly writes a full email: Subject line, greeting, body, sign-off. Missing details become placeholders like `[Name]`.

---

## Learning path

| # | File | Concept | What's new | Memory | Needs |
|---|---|---|---|---|---|
| 00 | `agent_00.py` | **LLM call** | `init_chat_model` → `llm.invoke()`. No agent, no system prompt | None | Ollama |
| 01 | `agent_01.py` | **First agent** | `create_agent` + Draftly `SYSTEM` prompt | None | Ollama |
| 02 | `agent_02.py` | **Cloud LLM + config** | Model and API key from `.env`, `thinking_level`, `max_retries` | None | `.env` |
| 03 | `agent_03.py` | **Chat loop (manual memory)** | `while` loop; we store the `messages` list ourselves | Python list | `.env` |
| 04 | `agent_04.py` | **Checkpointer memory** | `InMemorySaver` + `thread_id`; the agent stores history | RAM (lost on exit) | `.env` |
| 05 | `agent_05.py` | **Persistent memory** | `SqliteSaver` writes to `memory.db` | SQLite file | `.env` |
| 06 | `agent_06.py` | **Production memory** | `PostgresSaver` + `checkpointer.setup()` | PostgreSQL | `.env` + Postgres |
| 07 | `agent_07.py` | **Middleware** | `SummarizationMiddleware` shrinks long history | PostgreSQL + summary | `.env` + Postgres |
| ★ | `agent.py` | **Draftly baseline (all concepts)** | Steps 02 → 07 combined + `get_today_date` tool the agent decides when to call | PostgreSQL + summary | `.env` + Postgres |

`agent.py` puts every concept together: cloud LLM from `.env`, system prompt, tool, chat loop, `thread_id`, Postgres checkpointer and summarization middleware. Its summary trigger is a realistic 4000 tokens, keeping the last 10 messages. Step 07 uses 100 tokens so you can watch it fire.

---

## Agentic AI concepts covered

| Concept | Where | Notes |
|---|---|---|
| **Model (LLM)** | all | `init_chat_model("provider:model")` picks the provider from the prefix: `ollama:`, `google_genai:`, `openai:` |
| **System prompt** | 01 → ★ | Gives the agent its role: Draftly, the email drafter |
| **Agent loop** | 01 → ★ | `create_agent` runs model → tool → model until it has a final answer |
| **Tools** | ★ | A plain Python function with a docstring. The docstring tells the model when to use the tool |
| **Messages** | 01 → ★ | Input `{"messages": [{"role": "user", "content": ...}]}`. The reply is `result["messages"][-1].text` |
| **Short-term memory** | 03 → ★ | 03 is manual; 04+ use a **checkpointer** keyed by `thread_id` |
| **Threads** | 04 → ★ | `config={"configurable": {"thread_id": ...}}`. Each conversation name has its own history |
| **Persistence** | 05 → ★ | Memory lives in RAM (04), a SQLite file (05), or PostgreSQL (06, 07, ★) |
| **Middleware** | 07, ★ | Hooks into the agent loop; here it summarizes old messages to save tokens |
| **Reliability** | 02 → ★ | `max_retries=3` retries failed model calls |

### How a turn flows

```
You ──► agent.invoke({"messages": [...]}, config)
          │
          ├─ checkpointer loads thread history      (04+, ★)
          ├─ middleware runs (e.g. summarize)       (07, ★)
          ├─ LLM + SYSTEM prompt
          │     └─ tool call? ──► run tool ──► back to LLM   (★)
          └─ checkpointer saves new messages        (04+, ★)
          ▼
Draftly: <email draft>
```

---

## Setup

Requires **Python 3.13+** and [uv](https://docs.astral.sh/uv/).

The playground uses its own virtual env named **`.play/`**, not uv's default `.venv/`. Activate it first, then pass **`--active`** to every uv command so uv uses `.play/`.

### 0. Virtual env and dependencies

```bash
# 1. Go to the playground
cd draftly
cd playground

# 2. Create the env (first time only; skip it if .play/ already exists)
uv venv .play

# 3. Activate it (every new terminal)
source .play/bin/activate        # Windows: .play\Scripts\activate

# 4. Install dependencies from pyproject.toml / uv.lock into .play/
uv sync --active
```

**Daily uv commands** (run with `.play` active):

| Task | Command |
|---|---|
| Install / update deps after a pull | `uv sync --active` |
| Add a package | `uv add --active langchain-anthropic` |
| Remove a package | `uv remove --active langchain-anthropic` |
| Run a script | `uv run --active agent.py` |
| List installed packages | `uv pip list` |
| Leave the env | `deactivate` |

> Forgot `--active`? uv then creates and uses a separate `.venv/` and warns that `VIRTUAL_ENV=.play` doesn't match. Re-run the command with `--active`.

### 1. Local model (steps 00, 01)

Install [Ollama](https://ollama.com), then pull the models:

```bash
ollama pull gemma3:1b     # agent_00.py
ollama pull qwen3.5:4b    # agent_01.py
```

### 2. Cloud model (steps 02 → 07, ★)

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

```env
DRAFTLY_LLM_MODEL=google_genai:gemini-3.5-flash-lite
DRAFTLY_API_KEY=your-api-key
DRAFTLY_DB_URI=postgresql://postgres:your%40password@localhost:5432/test?sslmode=disable
```

| Variable | Used by | Purpose |
|---|---|---|
| `DRAFTLY_LLM_MODEL` | 02 → 07, ★ | `provider:model` string for `init_chat_model` |
| `DRAFTLY_API_KEY` | 02 → 07, ★ | Provider API key |
| `DRAFTLY_DB_URI` | 06, 07, ★ | PostgreSQL connection string. URL-encode special characters in the password (`@` → `%40`) |

> `thinking_level` is a Gemini (`google_genai`) option. Remove it if you switch to another provider.

### 3. PostgreSQL (steps 06, 07, ★)

Any local Postgres works, for example with Docker:

```bash
docker run -d --name draftly-pg -e POSTGRES_PASSWORD=yourpassword -e POSTGRES_DB=test -p 5432:5432 postgres:17
```

`checkpointer.setup()` creates the checkpoint tables on the first run.

---

## Run

With `.play` active, run each step in order from inside `playground/` (each script reads `.env` and `memory.db` from the current folder):

```bash
uv run --active agent_00.py   # 00 LLM call           (Ollama)
uv run --active agent_01.py   # 01 first agent        (Ollama)
uv run --active agent_02.py   # 02 cloud LLM          (.env)
uv run --active agent_03.py   # 03 chat loop
uv run --active agent_04.py   # 04 InMemorySaver
uv run --active agent_05.py   # 05 SqliteSaver        (memory.db)
uv run --active agent_06.py   # 06 PostgresSaver      (Postgres)
uv run --active agent_07.py   # 07 summarization      (Postgres)
uv run --active agent.py      # ★  Draftly baseline   (.env + Postgres)
```

`python agent_00.py` works too while `.play` is active.

**Before each step:**

| Step | Check |
|---|---|
| 00, 01 | Ollama is running (`ollama list` shows the model) |
| 02 → 05 | `.env` has `DRAFTLY_LLM_MODEL` and `DRAFTLY_API_KEY` |
| 06, 07, ★ | Postgres is running and `.env` has `DRAFTLY_DB_URI` |

- **Single-turn scripts** (00, 01, 02): enter one email idea and get one draft.
- **Chat scripts** (03 → 07, ★): keep refining the draft, e.g. *"make it more formal"*. Type `quit`, `exit` or `bye` to stop.
- **Memory scripts** (04 → 07, ★) ask for a **Conversation name** (the `thread_id`). Use the same name again to continue that conversation. In 05 → 07 and ★ this works even after you restart the script.

### Try it

```
Conversation name: leave-request
You: ask my manager for leave this Friday, mention today's date
Draftly: Subject: Leave Request for Friday ...          ← calls get_today_date (★)
You: make it shorter and mention I'll finish the report Thursday
Draftly: Subject: Friday Off Request ...
```

---

## Files

```
playground/
├── agent_00.py … agent_07.py   # learning steps, run in order
├── agent.py                    # Draftly baseline: all concepts combined
├── memory.db                   # SQLite memory (created by agent_05.py)
├── pyproject.toml / uv.lock    # dependencies
├── .env                        # your keys (never commit)
└── .play/                      # virtual environment
```
