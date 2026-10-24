from datetime import date

from langchain.agents import create_agent


# Agent tool(s)
def get_today_date() -> str:
    """Get today's date. Use it when the email needs the current date."""
    return date.today().strftime("%A, %B %d, %Y")

# System prompt
SYSTEM = """
You are a helpful AI email draft agent.
Write a clear, concise email with a Subject line, greeting, body, and sign-off.
Match the tone to the request. Use placeholders like [Name] for missing details.
Output only the email.
"""

# AI agent
agent = create_agent(
    model="ollama:gemma4:31b-cloud",
    tools=[get_today_date],
    system_prompt=SYSTEM,
)

q = input("Enter email draft idea: ")
result = agent.invoke(
    {"messages": [{"role": "user", "content": q}]}
)

print(result["messages"][-1].text)
