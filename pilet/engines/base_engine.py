from typing import Optional, Any, Dict

from pydantic import (
    BaseModel,
    Field,
)

from pilet.constants import *


class BaseLLM(BaseModel):
    """
        BaseLLM class inherited by all llm engines.

        Attributes:
            secret = "sk-..."
            openai.api_key = os.environ["OPENAI_API_KEY"]
            stream = llm.stream("Hi, write a short story")
        """

    model: str = Field(default=DEFAULT_OPENAI_MODEL, description="The LLM model to use.")
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        description="The temperature to use during generation.",
    )
    max_tokens: Optional[int] = Field(
        description="The maximum number of tokens to generate.",
    )

    api_key: str = Field(default=None, description="The OpenAI API key.")
    api_base: str = Field(description="The base URL for OpenAI API.")
    api_version: str = Field(description="The API version for OpenAI API.")

    def __init__(
            self,
            model: str = DEFAULT_OPENAI_MODEL,
            temperature: float = DEFAULT_TEMPERATURE,
            max_tokens: Optional[int] = None,
            max_retries: int = 3,
            timeout: float = 60.0,
            reuse_client: bool = True,
            api_key: Optional[str] = None,
            api_base: Optional[str] = None,
            api_version: Optional[str] = None,
            system_prompt: Optional[str] = None,
    ) -> None:

        super().__init__(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            max_retries=max_retries,
            api_key=api_key,
            api_version=api_version,
            api_base=api_base,
            timeout=timeout,
            reuse_client=reuse_client,
            system_prompt=system_prompt,
        )

        self._client = None
        self._aclient = None

    def _get_model_name(self) -> str:
        model_name = self.model
        if "ft-" in model_name:  # legacy fine-tuning
            model_name = model_name.split(":")[0]
        elif model_name.startswith("ft:"):
            model_name = model_name.split(":")[1]
        return model_name

    @classmethod
    def class_name(cls) -> str:
        return "openai_llm"

    def chat(self):
        pass

    def stream_chat(self, messages):
        pass

    def complete(self, prompt: str):
        pass

    def stream_complete(self, prompt: str, formatted: bool = False):
        pass

    def _use_chat_completions(self, kwargs: Dict[str, Any]) -> bool:
        if "use_chat_completions" in kwargs:
            return kwargs["use_chat_completions"]
        return self.metadata.is_chat_model

    def _stream_chat(self, messages):
        pass

    def _complete(self, prompt: str, **kwargs: Any):
        pass

    def _stream_complete(self, prompt: str, **kwargs: Any):
        pass

    def _update_max_tokens(self, all_kwargs: Dict[str, Any], prompt: str) -> None:
        """Infer max_tokens for the payload, if possible."""
        if self.max_tokens is not None or self._tokenizer is None:
            return
        # NOTE: non-chat completion endpoint requires max_tokens to be set
        num_tokens = len(self._tokenizer.encode(prompt))
        max_tokens = self.metadata.context_window - num_tokens
        if max_tokens <= 0:
            raise ValueError(
                f"The prompt has {num_tokens} tokens, which is too long for"
                " the model. Please use a prompt that fits within"
                f" {self.metadata.context_window} tokens."
            )
        all_kwargs["max_tokens"] = max_tokens

    def _get_response_token_counts(self, raw_response: Any) -> dict:
        """Get the token usage reported by the response."""
        if not isinstance(raw_response, dict):
            return {}

        usage = raw_response.get("usage", {})
        # NOTE: other model providers that use the OpenAI client may not report usage
        if usage is None:
            return {}

        return {
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
        }
