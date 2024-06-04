from abc import ABC
from typing import Optional
from pydantic import (
    Field
)

from pilet.tools import Tool
from pilet.constants import TranslatorModel


class Speech2Text(Tool, ABC):
    """
    Tool to convert speech to text and translate, if required.

    Attributes:
        use_local: Whether to use local model.
        translate: Whether to translate.
        model: Model to be used for Speech to Text and Translation
    """

    name: str = "Speech2Text2Translate"
    description: str = "Tool to convert speech to text and translate, if required."

    use_local: Optional[bool] = Field(default=False, description="Whether to use local model.")
    translate: Optional[bool] = Field(default=False, description="Whether to translate the text.")
    model: Optional[TranslatorModel] = Field(
        dafault="default",
        description="Model to be used for Speech to Text and Translation"
    )

    def run(self, sr, audio):
        if self.model == TranslatorModel.DEFAULT:
            text = sr.recognize_google(audio)
        elif self.model == TranslatorModel.SEAMLESS_4T:
            pass
        elif self.model == TranslatorModel.CUSTOM:
            if self.use_local:
                pass
            else:
                pass

        if self.translate:
            pass
        else:
            pass

        return text


