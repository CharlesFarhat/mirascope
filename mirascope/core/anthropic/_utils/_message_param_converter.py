import base64
from os import PathLike
from typing import cast

from anthropic.types import MessageParam

from mirascope.core import BaseMessageParam
from mirascope.core.anthropic._utils import convert_message_params
from mirascope.core.base import ImagePart, TextPart, ToolCallPart
from mirascope.core.base._utils._base_message_param_converter import (
    BaseMessageParamConverter,
)


class AnthropicMessageParamConverter(BaseMessageParamConverter):
    """Converts between Anthropic `MessageParam` objects and Mirascope `BaseMessageParam`."""

    @staticmethod
    def to_provider(message_params: list[BaseMessageParam]) -> list[MessageParam]:
        """
        Convert from Mirascope `BaseMessageParam` to Anthropic's `MessageParam`.
        """
        return convert_message_params(message_params)

    @staticmethod
    def from_provider(message_params: list[MessageParam]) -> list[BaseMessageParam]:
        """
        Convert from Anthropic's `MessageParam` back to Mirascope `BaseMessageParam`.
        """
        converted: list[BaseMessageParam] = []
        for message_param in message_params:
            role: str = "assistant"
            content = message_param["content"]
            has_tool_call: bool = False
            if isinstance(content, str):
                converted.append(BaseMessageParam(role=role, content=content))
                continue
            converted_content = []

            for block in content:
                if not isinstance(block, dict):
                    continue

                if block["type"] == "text":
                    text = block.get("text")
                    if not isinstance(text, str):
                        raise ValueError(
                            "TextBlockParam must have a string 'text' field."
                        )
                    converted_content.append(TextPart(type="text", text=text))

                elif block["type"] == "image":
                    source = block.get("source")
                    if not source or source.get("type") != "base64":
                        raise ValueError(
                            "ImageBlockParam must have a 'source' with type='base64'."
                        )
                    image_data = source.get("data")
                    media_type = source.get("media_type")
                    if not image_data or not media_type:
                        raise ValueError(
                            "ImageBlockParam source must have 'data' and 'media_type'."
                        )
                    if media_type not in [
                        "image/jpeg",
                        "image/png",
                        "image/gif",
                        "image/webp",
                    ]:
                        raise ValueError(
                            f"Unsupported image media type: {media_type}. "
                            "BaseMessageParam currently only supports JPEG, PNG, GIF, and WebP images."
                        )
                    if isinstance(image_data, str):
                        decoded_image_data = base64.b64decode(image_data)
                    elif isinstance(image_data, PathLike):
                        with open(image_data, "rb") as image_data:
                            decoded_image_data = image_data.read()
                    else:
                        decoded_image_data = image_data.read()
                    converted_content.append(
                        ImagePart(
                            type="image",
                            media_type=media_type,
                            image=decoded_image_data,
                            detail=None,
                        )
                    )

                elif block["type"] == "tool_use":
                    converted_content.append(
                        ToolCallPart(
                            type="tool_call",
                            args=cast(dict, block["input"]),
                            id=block["id"],
                            name=block["name"],
                        )
                    )
                    has_tool_call = True
                else:
                    # Any other block type is not supported
                    raise ValueError(
                        f"Unsupported block type '{block['type']}'. "
                        "BaseMessageParam currently only supports text and image parts."
                    )

            converted.append(
                BaseMessageParam(
                    role="tool" if has_tool_call else role, content=converted_content
                )
            )

        return converted
