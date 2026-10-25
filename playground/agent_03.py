# Step 03 - Chat loop with manual memory (we keep the message list ourselves)
import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent


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

# AI agent
agent = create_agent(
    model=llm,
    tools=[],
    system_prompt=SYSTEM,
)

# Chat loop (memory = our own messages list)
messages = []

while True:
    q = input("You: ")
    if q.lower() in ("quit", "exit", "bye"):
        break

    messages.append({"role": "user", "content": q})  # Human msg
    result = agent.invoke({"messages": messages})    # + AI msg + Tool msg(s)
    messages = result["messages"]                    # full history for next turn

    print("Draftly:", result["messages"][-1].text)
