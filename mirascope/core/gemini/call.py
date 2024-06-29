"""The `gemini_call` decorator for functions as LLM calls."""

from google.generativeai.types import ContentDict

from ..base import (
    BaseStream,
    call_factory,
    create_factory,
    extract_factory,
    stream_factory,
)
from ._structured_stream import structured_stream_decorator
from ._utils import (
    gemini_api_calculate_cost,
    get_json_output,
    handle_stream,
    handle_stream_async,
    setup_call,
)
from .call_params import GeminiCallParams
from .call_response import GeminiCallResponse
from .call_response_chunk import GeminiCallResponseChunk
from .dynamic_config import GeminiDynamicConfig
from .tool import GeminiTool

GeminiStream = BaseStream[
    GeminiCallResponseChunk,
    ContentDict,
    ContentDict,
    ContentDict,
    GeminiTool,
    GeminiDynamicConfig,
]

gemini_call = call_factory(
    TCallResponse=GeminiCallResponse,
    TCallResponseChunk=GeminiCallResponseChunk,
    TCallParams=GeminiCallParams,
    TDynamicConfig=GeminiDynamicConfig,
    TStream=GeminiStream,
    create_decorator=create_factory(
        TBaseCallResponse=GeminiCallResponse,
        setup_call=setup_call,
        calculate_cost=gemini_api_calculate_cost,
    ),
    stream_decorator=stream_factory(
        TBaseCallResponseChunk=GeminiCallResponseChunk,
        TStream=GeminiStream,
        TMessageParamType=ContentDict,
        setup_call=setup_call,
        handle_stream=handle_stream,
        handle_stream_async=handle_stream_async,
    ),
    extract_decorator=extract_factory(
        TBaseCallResponse=GeminiCallResponse,
        TToolType=GeminiTool,
        setup_call=setup_call,
        get_json_output=get_json_output,
        calculate_cost=gemini_api_calculate_cost,
    ),
    structured_stream_decorator=structured_stream_decorator,
)
'''A decorator for calling the Gemini API with a typed function.

This decorator is used to wrap a typed function that calls the Gemini API. It parses
the docstring of the wrapped function as the messages array and templates the input
arguments for the function into each message's template.

Example:

```python
@gemini_call(model="gemini-1.5-pro")
def recommend_book(genre: str):
    """Recommend a {genre} book."""

response = recommend_book("fantasy")
```

Args:
    model: The Gemini model to use in the API call.
    stream: Whether to stream the response from the API call.
    tools: The tools to use in the Gemini API call.
    **call_params: The `GeminiCallParams` call parameters to use in the API call.

Returns:
    The decorator for turning a typed function into an Gemini API call.
'''
