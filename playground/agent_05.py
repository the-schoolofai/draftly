# Step 05 - Persistent memory in SQLite (SqliteSaver -> memory.db)
import os
import sqlite3
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver


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

# Checkpointer (file memory - survives restarts)
conn = sqlite3.connect("memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

# AI agent
agent = create_agent(
    model=llm,
    tools=[],
    system_prompt=SYSTEM,
    checkpointer=checkpointer,
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
