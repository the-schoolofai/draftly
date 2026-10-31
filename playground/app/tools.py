from datetime import date

from langchain.tools import tool


@tool
def get_today_date() -> str:
    """Get today's date. Use it when the email needs the current date."""
    return date.today().strftime("%A, %B %d, %Y")


# Ideas for next tools:
# - web search
# - file search (RAG)

TOOLS = [get_today_date]
