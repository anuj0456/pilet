from typing import Any, List, Optional
from llama_index.core.query_engine import RouterQueryEngine
from langchain_core.callbacks import BaseCallbackHandler

from pydantic import (
    BaseModel,
    Field,
    InstanceOf,
    PrivateAttr,
)

from pilet.tools import Tool
from pilet.jobs import Job


class Agent(BaseModel):
    """Represents an agent within a system.

    Each agent is defined by a role, a goal, a history, and optionally, a language model (LLM).
    Additionally, an agent may possess memory, operate in verbose mode, and delegate jobs to other agents.

    Attributes:
        name: Name of the agent.
        role: The role of the agent.
        goal: The objective of the agent.
        summary: Summary of the job.
        max_retry: Maximum number of iterations for an agent to execute a job.
        llm: The language model that will run the agent.
        use_kv_cache: Whether to use KV cache for faster inferencing.
        cache: Whether the agent should have memory or not.
        verbose: Whether the agent execution should be in verbose mode.
        tools: Tools at agents disposal.
        jobs: List of jobs assigned by pilet.
        allow_assign: Whether the agent is allowed to delegate jobs to other agents.
        step_callback: Callback to be executed after each step of the agent execution.
        callbacks: Function calls that are triggered during the agent's execution process
    """

    _router_query_engine: RouterQueryEngine = PrivateAttr()
    _allow_delegation: bool = PrivateAttr(default=True)

    name: Optional[str] = Field(description="Name of the agent")
    role: str = Field(description="Role of the agent")
    goal: str = Field(description="Objective of the agent")
    summary: str = Field(description="Summary of the job")
    pilet: Any = Field(default=True, description=" Pilet to which the agent belongs.")
    max_retry: Optional[int] = Field(default=10)
    llm: Optional[str] = Field(default="Openai", description="Language model that will run the agent.")
    use_kv_cache: bool = Field(default=False, description="Whether to use KV cache for faster inferencing.")
    cache: bool = Field(default=True, description="Whether the agent should use a cache for tool usage.")
    verbose: bool = Field(default=False, description="Verbose mode for the Agent Execution")
    allow_assign: bool = Field(default=True, description="Allow delegation of jobs to agents")
    tools: List[Tool] = Field(default_factory=list, description="Tools at agents disposal")
    jobs: List[Job] = Field(default_factory=list, description="List of jobs assigned by pilet.")
    step_callback: Optional[Any] = Field(
        default=None,
        description="Callback to be executed after each step of the agent execution.",
    )
    callbacks: Optional[List[InstanceOf[BaseCallbackHandler]]] = Field(
        default=None, description="Callback to be executed"
    )

    # def __init__(self, tools: Optional[List[Tool]], **kwargs: Any) -> None:
    #     """Init params."""
    #     super().__init__(**kwargs)
        # self._router_query_engine = RouterQueryEngine(
        #     selector=PydanticSingleSelector.from_defaults(),
        #     query_engine_tools=tools,
        #     verbose=kwargs.get("verbose", False),
        # )
        # self.prompt_str = query
        # super().__init__(
        #     tools=tools,
        #     **kwargs,
        # )
