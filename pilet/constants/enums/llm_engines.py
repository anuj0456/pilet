from enum import Enum
from typing import Optional

from pydantic import field_validator

from pilet.constants.const import REST_API_TIMEOUT


class LLMEngines(Enum):
    AZURE = "azure"
    OPENAI = "openai"
    MISTRAL = "mistral"
    ANTHROPIC = "anthropic"
    CLAUDE = "claude"
    GEMINI = "gemini"
