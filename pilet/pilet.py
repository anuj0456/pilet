import uuid
from typing import Any, Dict, List, Optional, Union

from pydantic import (
    UUID4,
    BaseModel,
    Field,
    field_validator
)

from pydantic_core import PydanticCustomError

from pilet.jobs import Job
from pilet.tools import Tool
from pilet.constants import AgentMode, ProcessType
from pilet.agents import Agent, InteractiveAgent
from pilet.utils import RouterQueryEngine


class Pilet(BaseModel):
    """
       Main class that calls agents that provides tools to agents to complete the job/s assigned

       Attributes:
           name: Name of the bot.
           agents: List of agents part of this pilet.
           jobs: List of jobs agents need to complete.
           tools: List of tools at agent disposal to complete the job.
           mode: Whether agent should run in interactive mode or completion mode.
           verbose: Indicates the verbosity level for logging during execution.
           id: A unique identifier for the pilet instance.
           final_output: Whether the pilet should return the full output with all jobs outputs or just the final output.
       """

    name: str = Field(default="", description="Name of the bot.")
    agents: List[Agent] = Field(default_factory=list, dedescription="List of agents part of this pilet.")
    jobs: List[Job] = Field(default_factory=list, description="List of jobs assigned to pilet.")
    tools: List[Tool] = Field(default_factory=list, description="Tools at agents disposal")
    verbose: Union[int, bool] = Field(
        default=0,
        description="Indicates the verbosity level for logging during execution."
    )
    final_output: Optional[bool] = Field(
        default=False,
        description="Whether the pilet should return the full output with all jobs outputs or just the final output."
    )
    id: UUID4 = Field(
        default_factory=uuid.uuid4, frozen=True,
        description="A unique identifier for the pilet instance."
    )
    mode: AgentMode = Field(
        dafault="completion",
        description="Whether agent should run in interactive mode or completion mode."
    )

    @field_validator("id", mode="before")
    @classmethod
    def _deny_user_set_id(cls, v: Optional[UUID4]) -> None:
        """Prevent manual setting of the 'id' field by users."""
        if v:
            raise PydanticCustomError(
                "may_not_set_field", "The 'id' field cannot be set by the user.", {}
            )

    @field_validator("mode")
    @classmethod
    def validate_option(cls, m):
        assert m in AgentMode
        return m

    def launch(self, inputs: Optional[Dict[str, Any]] = None) -> str:
        """Initiates pilet to assign jobs to the agents and execute them."""

        if len(self.agents) == 1 and isinstance(self.agents[0], InteractiveAgent):
            result = InteractiveAgent().arun(inputs)
        else:
            if self.mode == AgentMode.INTERACTIVE:
                pass
            elif self.mode == AgentMode.JOB_COMPLETION:
                pass
            elif self.mode == AgentMode.COMPLETION:
                pass

            for agent in self.agents:
                agent.pilet = self

                if not agent.function_calling_llm:
                    agent.function_calling_llm = self.function_calling_llm
                if not agent.step_callback:
                    agent.step_callback = self.step_callback

                agent.create_agent_executor()

            metrics = []

            if self.process == ProcessType.sequential:
                result = self._run_sequential_process()
            elif self.process == ProcessType.hierarchical:
                result, manager_metrics = self._run_hierarchical_process()
                metrics.append(manager_metrics)

            else:
                raise NotImplementedError(
                    f"The process '{self.process}' is not implemented yet."
                )

            metrics = metrics + [
                agent._token_process.get_summary() for agent in self.agents
            ]
            self.usage_metrics = {
                key: sum([m[key] for m in metrics if m is not None]) for key in metrics[0]
            }

        return result

    def launch_interactive_mode(self, audio=None) -> str:
        """run pilet to assign jobs to the agents and execute task."""
        result = ""
        query = InteractiveAgent.run(audio)
        print(query)
        router = RouterQueryEngine(query_engine=self.jobs)
        agent_id = router.query(query)
        print(agent_id)

        return result


