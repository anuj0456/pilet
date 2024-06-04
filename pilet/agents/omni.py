from typing import Any, List
import speech_recognition as sr

from pydantic import (
    Field,
    PrivateAttr
)

from pilet.agents.agent import Agent
from pilet.jobs import Job


class InteractiveAgent(Agent):
    """Interactive Agent for voice and text.

       Works only in Interactive mode or job_completion mode.

       Attributes:
           enable_voice: Whether to enable for voice or text.
           stream: Whether to listen audio continuously.
    """
    _recognizer: Any = PrivateAttr()
    _audio_m: Any = sr.Microphone()

    name: str = "Omni"
    role: str = "Expert in understanding audios and videos"
    goal: str = "Accept feedback to improve the final output"
    summary: str = "You are an expert in rewriting prompts according from user feedback."

    jobs: List[Job] = None
    tools: List[Any] = None
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


