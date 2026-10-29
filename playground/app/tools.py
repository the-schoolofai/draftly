from datetime import date


def get_today_date() -> str:
    """Get today's date. Use it when the email needs the current date."""
    return date.today().strftime("%A, %B %d, %Y")
