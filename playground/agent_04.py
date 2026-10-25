# Step 04 - Short-term memory with a checkpointer (InMemorySaver + thread_id)
import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver


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

# AI agent (RAM memory - lost when the script exits)
agent = create_agent(
    model=llm,
    tools=[],
    system_prompt=SYSTEM,
    checkpointer=InMemorySaver(),
)

# Conversation thread
thread_id = input("Conversation name: ")
config = {"configurable": {"thread_id": thread_id}}

# Chat loop (agent remembers history per thread_id)
while True:
    q = input("You: ")
    if q.lower() in ("quit", "exit", "bye"):
        break

    result = agent.invoke(
        {"messages": [{"role": "user", "content": q}]},
        config=config,
    )
    print("Draftly:", result["messages"][-1].text)
