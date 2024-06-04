from textwrap import dedent
from pydantic import Field
from abc import ABC
from typing import Optional, List

from pilet.jobs import Job
from pilet.tools import Tool


class Translator(Job, ABC):
    in_lang: str = Field(description="Input language to be converted")
    out_lang: str = Field(default="eng", description="Output language to be converted")

    description: str = dedent(f"""Translate the input from {in_lang} to {out_lang}. 
                                  The meaning of the sentence should not change.
                                  Identify key points by removing the noise.""")

    summary: str = "Translate the text from one language to another"
    expected_output: str = "translated text"
    raw_output: str = ""
    tools: Optional[List[Tool]] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def process_query(self, query: str) -> str:
        pass
