"""Types for interacting with Chroma using Mirascope."""

from typing import Any, Literal, Optional

from chromadb import CollectionMetadata, Settings
from chromadb.api.types import URI, Document, IDs, Loadable, Metadata
from chromadb.config import DEFAULT_DATABASE, DEFAULT_TENANT
from chromadb.types import Vector
from pydantic import BaseModel, ConfigDict

from ..rag.types import BaseVectorStoreParams


class ChromaParams(BaseVectorStoreParams):
    metadata: Optional[CollectionMetadata] = None
    get_or_create: bool = False


class ChromaQueryResult(BaseModel):
    ids: list[IDs]
    embeddings: Optional[list[list[Vector]]] = None
    documents: Optional[list[list[Document]]] = None
    uris: Optional[list[list[URI]]] = None
    data: Optional[list[Loadable]] = None
    metadatas: Optional[list[list[Optional[Metadata]]]] = None
    distances: Optional[list[list[float]]] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ChromaSettings(BaseModel):
    mode: Literal["http", "persistent", "ephemeral"] = "persistent"
    path: str = "./chroma"
    host: str = "localhost"
    port: int = 8000
    ssl: bool = False
    headers: Optional[dict[str, str]] = None
    settings: Optional[Settings] = None
    tenant: str = DEFAULT_TENANT
    database: str = DEFAULT_DATABASE

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    def kwargs(self) -> dict[str, Any]:
        """Returns all parameters for the index as a keyword arguments dictionary."""
        if self.mode == "http":
            exclude = {"mode", "path"}
        elif self.mode == "persistent":
            exclude = {"mode", "host", "port", "ssl", "headers"}
        elif self.mode == "ephemeral":
            exclude = {"mode", "host", "port", "ssl", "headers", "path"}
        kwargs = {
            key: value
            for key, value in self.model_dump(exclude=exclude).items()
            if value is not None
        }
        return kwargs
