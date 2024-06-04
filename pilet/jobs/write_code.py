from textwrap import dedent
from abc import ABC
from typing import Optional, List

from pilet.jobs import Job
from pilet.tools import Tool


class WriteCode(Job, ABC):
    description: str = dedent(f"""Analyze the video feed and extract key information from it.  
                                  Identify key points  by removing the noise.""")
    summary: str = "Analyze video feed and extract key points by removing noise"
    expected_output: str = "clean video"
    raw_output: str = ""
    tools: Optional[List[Tool]] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def process_query(self, query: str) -> str:
        pass


class ReWriteCode(Job, ABC):
    description: str = dedent(f"""Analyze the video feed and extract key information from it.  
                                  Identify key points  by removing the noise.""")
    summary: str = "Analyze video feed and extract key points by removing noise"
    expected_output: str = "clean video"
    raw_output: str = ""
    tools: Optional[List[Tool]] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def process_query(self, query: str) -> str:
        pass