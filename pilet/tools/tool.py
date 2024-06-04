from abc import ABC, abstractmethod
from typing import Any

from pydantic import (
    BaseModel,
    Field
)


class Tool(BaseModel, ABC):
    """
    Attributes:
        name: The unique name of the tool that clearly communicates its purpose.
        summary: Summary of what the tool can do.
        description: Used to tell the model how/when/why to use the tool.
    """

    name: str = Field(description="The unique name of the tool that clearly communicates its purpose.")
    summary: str = Field(description="Summary of what the tool can do.")
    description: str = Field(description="Used to tell the model how/when/why to use the tool.")

    def run(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        print(f"Using Tool: {self.name}")
        return self._run(*args, **kwargs)

    @abstractmethod
    def _run(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Here goes the actual implementation of the tool."""
