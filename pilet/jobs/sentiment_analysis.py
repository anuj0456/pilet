from textwrap import dedent
from abc import ABC
from typing import Optional, List

from pilet.jobs import Job
from pilet.tools import Tool


class SentimentAnalysis(Job, ABC):
    description: str = dedent(f"""Analyze the following text and determine its sentiment. 
    Categorize the sentiment as Positive, Negative, or Neutral. 
    Provide a brief explanation for your classification""")
    summary: str = "Analyze a given text and categorize its sentiment as Positive, Negative, or Neutral."
    expected_output: str = "sentiments of the text"
    raw_output: str = ""
    tools: Optional[List[Tool]] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def process_query(self, query: str) -> str:
        pass
