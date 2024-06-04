from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core import ChatPromptTemplate
from typing import Tuple
from pydantic import BaseModel, Field


class PiletPromptTemplate(BaseModel):

    system_prompt: str = Field(default=None)

    def get_chat_prompt_template(self, current_reasoning: Tuple[str, str]) -> ChatPromptTemplate:
        system_msg = ChatMessage(role=MessageRole.SYSTEM, content=self.system_prompt)
        messages = [system_msg]
        for raw_msg in current_reasoning:
            if raw_msg[0] == "user":
                messages.append(
                    ChatMessage(role=MessageRole.USER, content=raw_msg[1])
                )
            else:
                messages.append(
                    ChatMessage(role=MessageRole.ASSISTANT, content=raw_msg[1])
                )
        return ChatPromptTemplate(message_templates=messages)
