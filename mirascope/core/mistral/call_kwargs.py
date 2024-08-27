"""This module contains the type definition for the Mistral call keyword arguments."""

from mistralai.models.chat_completion import ChatMessage

from mirascope.core.base.call_kwargs import BaseCallKwargs

from .call_params import MistralCallParams
from .tool import MistralTool


class MistralCallKwargs(MistralCallParams, BaseCallKwargs[MistralTool]):
    model: str
    messages: list[ChatMessage]
