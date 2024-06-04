from typing import Any, List
import speech_recognition as sr

from pydantic import (
    Field,
    PrivateAttr
)

from pilet.agents.agent import Agent
from pilet.jobs import Job, WriteCode
from pilet.tools import CodeGen


class CodeMasterAgent(Agent):
    """Agent to write/rewrite code.

       Attributes:
           enable_voice: Whether to enable for voice or text.
           stream: Whether to listen audio continuously.
    """

    name: str = "CodeMaster"
    role: str = "Expert in writing code"
    goal: str = "To write new code as per user instructions or rewrite code to another language"
    summary: str = "You are an expert in rewriting code according as per user instructions."

    jobs: List[Job] = [WriteCode]
    tools: List[Any] = [CodeGen]
    enable_voice: bool = True
    stream: bool = Field(default=False, description="Whether to listen audio continuously.")

    def __init__(self, /, **data: Any):
        super().__init__(**data)

    @classmethod
    def run(cls, file=None):
        cls._recognizer = sr.Recognizer()
        text = cls._run(cls, file)
        return text

    @classmethod
    async def arun(cls, file=None):
        cls._recognizer = sr.Recognizer()
        text = cls._run(cls, file)
        return text

    async def listen(self):
        with self._audio_m as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def interrupt(self, stop):
        if stop:
            stop_listening = self.recognizer.listen_in_background(self._audio_m, self._process_audio)
            stop_listening()

    def _run(self, file):
        file_audio = sr.AudioFile(file)
        with file_audio as source:
            audio_text = self._recognizer.record(source)
            text = self._recognizer.recognize_google(audio_text)
            return text


