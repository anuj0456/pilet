from typing import Optional, List
from abc import abstractmethod
from pydantic import BaseModel, Field, model_validator

from pilet.tools import Tool


class Job(BaseModel):
    """Class that represents the result of a jobs."""

    query: Optional[str] = Field("User query that needs to answered")
    description: str = Field(description="Description of the job")
    summary: str = Field(description="Summary of the task", default=None)
    expected_output: str = Field(description="Expected Output of the job", default=None)
    raw_output: str = Field(description="Result of the job")
    tools: Optional[List[Tool]] = Field(description="Required for predefined jobs")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @model_validator(mode="after")
    def set_summary(self):
        excerpt = " ".join(self.description.split(" ")[:10])
        self.summary = f"{excerpt}..."
        return self

    def result(self):
        return self.expected_output

    @abstractmethod
    def process_query(self, query: str) -> str:
        """process_query implemented by inherited class"""
