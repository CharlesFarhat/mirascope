"""Contains the BaseMessageParamConverter class."""

from abc import ABC, abstractmethod
from typing import Any

from mirascope.core import BaseMessageParam


class BaseMessageParamConverter(ABC):
    """Base class for converting message params to/from provider formats."""

    @staticmethod
    @abstractmethod
    def to_provider(base_params: list[BaseMessageParam]) -> list[Any]:
        """Converts base message params -> provider-specific messages."""
        pass

    @staticmethod
    @abstractmethod
    def from_provider(provider_messages: list[Any]) -> list[BaseMessageParam]:
        """Converts provider-specific messages -> Base message params."""
        pass
