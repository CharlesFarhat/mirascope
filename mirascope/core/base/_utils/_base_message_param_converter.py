"""A new base converter approach."""

from abc import ABC, abstractmethod
from typing import Any

from mirascope.core import BaseMessageParam


class BaseMessageParamConverter(ABC):
    """Base class for converting message params to/from provider formats."""

    @abstractmethod
    def to_provider(self, base_params: list[BaseMessageParam]) -> list[Any]:
        """Converts Mirascope base message params -> provider-specific messages."""
        pass

    @abstractmethod
    def from_provider(self, provider_messages: list[Any]) -> list[BaseMessageParam]:
        """Converts provider-specific messages -> Mirascope base message params."""
        pass
