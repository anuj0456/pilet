from textwrap import dedent
from abc import ABC
from typing import Optional, List

from pilet.jobs import Job
from pilet.tools import Tool


class QnA(Job, ABC):
    description: str = dedent(f"""Answer the following questions based on the provided context. 
    Ensure your responses are accurate and concise, addressing each question directly.""")
    summary: str = "Answer questions based on provided context with accurate and concise responses."
    expected_output: str = "Concise answers to each question"
    raw_output: str = ""
    tools: Optional[List[Tool]] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def process_query(self, query: str) -> str:
        pass
