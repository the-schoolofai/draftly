from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

from app.config import MODEL, PROVIDER
from app.tools import get_today_date


llm = init_chat_model(
    model=MODEL,
    model_provider=PROVIDER,
    # temperature=0.2,
    max_retries=3,
    reasoning_effort="low"
)

SYSTEM = """
You are Draftly, a helpful AI email draft agent.
Write a clear, concise email with a Subject line, greeting, body, and sign-off.
Match the tone to the request. Use placeholders like [Name] for missing details.
Output only the email.
"""

agent = create_agent(
    model=llm,
    tools=[get_today_date],
    system_prompt=SYSTEM,
)

def run_agent(text: str) -> str:
    messages = [{"role": "user", "content": text}]

    try:
        result = agent.invoke({"messages": messages})
    except Exception as err:
        return f"Sorry, something went wrong: {err}"

    return result["messages"][-1].text


if __name__ == "__main__":
    # Chat loop
    while True:
        q = input("You: ")
        if q.lower() in ("quit", "exit", "bye"):
            break

        print("Draftly:", run_agent(q))


# (.play) mac@rizwan playground % uv run --active -m app.agent
