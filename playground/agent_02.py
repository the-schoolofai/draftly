# Step 02 - Cloud LLM from .env (model + API key, thinking, retries)
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

# Single turn
q = input("Enter email draft idea: ")
result = agent.invoke(
    {"messages": [{"role": "user", "content": q}]}
)

print(result["messages"][-1].text)
