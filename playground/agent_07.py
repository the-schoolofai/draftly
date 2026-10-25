# Step 07 - Middleware: summarize long history (SummarizationMiddleware)
import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.postgres import PostgresSaver


load_dotenv(".env")

# LLM
llm = init_chat_model(
    model=os.getenv("DRAFTLY_LLM_MODEL"),
    api_key=os.getenv("DRAFTLY_API_KEY"),
    thinking_level="medium",
    max_retries=3,
)

# System prompt
SYSTEM = """
You are Draftly, a helpful AI email draft agent.
Write a clear, concise email with a Subject line, greeting, body, and sign-off.
Match the tone to the request. Use placeholders like [Name] for missing details.
Output only the email.
"""

# Database (special chars in the password must be URL-encoded, e.g. @ -> %40)
DB_URI = os.getenv("DRAFTLY_DB_URI")

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()  # create checkpoint tables (first run)

    # AI agent (+ middleware)
    agent = create_agent(
        model=llm,
        tools=[],
        system_prompt=SYSTEM,
        checkpointer=checkpointer,
        middleware=[
            SummarizationMiddleware(
                model=llm,
                trigger=("tokens", 100),  # summarize once history passes 100 tokens (low for demo)
                keep=("messages", 5),     # keep the last 5 messages as-is
            )
        ],
    )

    # Conversation thread
    thread_id = input("Conversation name: ")
    config = {"configurable": {"thread_id": thread_id}}

    # Chat loop
    while True:
        q = input("You: ")
        if q.lower() in ("quit", "exit", "bye"):
            break

        result = agent.invoke(
            {"messages": [{"role": "user", "content": q}]},
            config=config,
        )
        print("Draftly:", result["messages"][-1].text)
