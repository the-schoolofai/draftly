from typing import Literal

from pydantic import BaseModel, Field


class Draft(BaseModel):
    """A complete email draft."""

    subject: str = Field(description="Email subject in a single line")
    body: str = Field(description="Email body: greeting, body and sign-off")
    tone: Literal["friendly", "professional", "casual"] = Field(
        description="Tone of the email"
    )
