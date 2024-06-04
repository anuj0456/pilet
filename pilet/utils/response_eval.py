from llama_index.core.bridge.pydantic import Field, BaseModel


class ResponseEval(BaseModel):
    """Evaluation of whether the response has an error."""

    has_error: bool = Field(
        ..., description="Whether the response has an error."
    )
    new_question: str = Field(..., description="The suggested new question.")
    explanation: str = Field(
        ...,
        description=(
            "The explanation for the error as well as for the new question."
            "Can include the direct stack trace as well."
        ),
    )
