from langchain.agents.middleware import SummarizationMiddleware, ToolRetryMiddleware


def build_middleware(llm):
    """Middleware that runs inside the agent loop."""
    return [
        # Summarize old messages once history gets long; keep the last 20
        SummarizationMiddleware(
            model=llm,
            trigger=("tokens", 4000),
            keep=("messages", 20),
        ),
        # Retry a failing tool call up to 3 times
        ToolRetryMiddleware(max_retries=3),
        # Try other models if the main one fails:
        # ModelFallbackMiddleware("gpt-5.4-mini", "claude-sonnet-4-6"),
    ]
