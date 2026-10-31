from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import BaseCheckpointSaver

from app.config import API_KEY, MODEL, PROVIDER
from app.middlewares import build_middleware
from app.prompts import SYSTEM
from app.schemas import Draft
from app.tools import TOOLS


llm = init_chat_model(
    model=MODEL,
    model_provider=PROVIDER,
    api_key=API_KEY or None,  # Ollama needs no key
    max_retries=3,
)


def build_agent(checkpointer: BaseCheckpointSaver):
    """Create the Draftly agent with tools, memory, structured output and middleware."""
    return create_agent(
        model=llm,
        system_prompt=SYSTEM,
        tools=TOOLS,
        checkpointer=checkpointer,
        response_format=Draft,
        middleware=build_middleware(llm),
    )


def format_draft(draft: Draft) -> str:
    """Turn a Draft into printable text."""
    return f"Subject: {draft.subject}\n\n{draft.body}\n\n[tone: {draft.tone}]"


def run_agent(agent, text: str, thread_id: str) -> str:
    """Send one message to the agent in a conversation thread and return the draft."""
    config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

    try:
        result = agent.invoke({"messages": [HumanMessage(text)]}, config=config)
    except Exception as err:
        return f"Sorry, something went wrong: {err}"

    draft = result.get("structured_response")
    if draft is None:
        # Fall back to the plain reply if the model skipped the schema
        return result["messages"][-1].text

    return format_draft(draft)
