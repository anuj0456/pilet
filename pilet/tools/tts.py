from abc import ABC
from typing import Optional
from openai import OpenAI

from pydantic import (
    Field
)

from pilet.tools import Tool
from pilet.constants import TranslatorModel


class Text2Speech(Tool, ABC):
    """
    Tool to convert text to speech and translate, if required.

    Attributes:
        use_local: Whether to use local model.
        translate: Whether to translate.
        model: Model to be used for Speech to Text and Translation
    """

    name: str = "Text"
    description: str = "Tool to convert text to speech and translate, if required."

    use_local: Optional[bool] = Field(default=False, description="Whether to use local model.")
    translate: Optional[bool] = Field(default=False, description="Whether to translate the text.")
    model: Optional[TranslatorModel] = Field(
        dafault="default",
        description="Model to be used for Speech to Text and Translation"
    )

    def run(self, text, speech_file_path):
        client = OpenAI()
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )
        response.stream_to_file(speech_file_path)
