from textwrap import dedent
from typing import Any

from pilet.jobs import Job


class AudioStreaming(Job):
    description: str = dedent(f"""""")
    summary: str = ""
    expected_output: str = ""
    raw_output: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
