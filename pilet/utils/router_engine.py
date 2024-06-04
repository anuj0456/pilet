from typing import List, Any, Optional
from pydantic import Field, PrivateAttr

from llama_index.core import PromptTemplate
from llama_index.llms.openai import OpenAI
from llama_index.program.openai import OpenAIPydanticProgram
from llama_index.core.query_engine import CustomQueryEngine, BaseQueryEngine
from llama_index.core.response_synthesizers import TreeSummarize

from pilet.utils.utility import Utility
from pilet.utils.router_output import Answers

from pilet.agents import Agent
from pilet.jobs import Job
from pilet.tools import Tool


class RouterQueryEngine(CustomQueryEngine):
    """Use our Pydantic program to perform routing."""

    _engine_type: str = PrivateAttr()

    query_engine: Optional[List[Any]]
    choice_descriptions: Optional[List[str]]
    verbose: Optional[bool] = False
    router_prompt: Optional[PromptTemplate]
    llm: Optional[OpenAI]
    summarizer: Optional[TreeSummarize] = Field(default_factory=TreeSummarize)

    def _process_query_engine(self):
        if isinstance(self.query_engine, Agent):
            _engine_type = "agent"
        elif isinstance(self.query_engine, Job):
            _engine_type = "job"
        elif isinstance(self.query_engine, Tool):
            _engine_type = "tool"

        self.choice_descriptions = []
        for engine in self.query_engine:
            self.choice_descriptions.append(engine.summary)

    def custom_query(self, query_str: str):
        """Define custom query."""

        self._process_query_engine()
        prompt = Utility.router_prompt(self.choice_descriptions)

        program = OpenAIPydanticProgram.from_defaults(
            output_cls=Answers,
            prompt=prompt,
            verbose=self.verbose,
            llm=self.llm,
        )

        choices_str = Utility.get_choice_str(self.choice_descriptions)
        output = program(context_list=choices_str, query_str=query_str)
        # print choice and reason, and query the underlying engine
        if self.verbose:
            print(f"Selected choice(s):")
            for answer in output.answers:
                print(f"Choice: {answer.choice}, Reason: {answer.reason}")

        responses = []
        for answer in output.answers:
            choice_idx = answer.choice - 1
            query_engine = self.query_engine[choice_idx]
            print(query_engine)
            response = query_engine.query(query_str)
            responses.append(response)

        # if a single choice is picked, we can just return that response
        if len(responses) == 1:
            return responses[0]
        else:
            # if multiple choices are picked, we can pick a summarizer
            response_strs = [str(r) for r in responses]
            result_response = self.summarizer.get_response(
                query_str, response_strs
            )
            return result_response
