from typing import List
from pydantic import BaseModel


class Answer(BaseModel):
    """Represents a single choice with a reason."""
    choice: int
    reason: str


class Answers(BaseModel):
    """Represents a list of answers."""
    answers: List[Answer]
