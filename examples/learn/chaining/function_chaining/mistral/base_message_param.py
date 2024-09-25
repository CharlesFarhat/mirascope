from mirascope.core import BaseMessageParam, mistral


@mistral.call("mistral-large-latest")
def summarize(text: str) -> list[BaseMessageParam]:
    return [BaseMessageParam(role="user", content=f"Summarize this text: {text}")]


@mistral.call("mistral-large-latest")
def translate(text: str, language: str) -> list[BaseMessageParam]:
    return [
        BaseMessageParam(
            role="user",
            content=f"Translate this text to {language}: {text}",
        )
    ]


summary = summarize("Long English text here...")
translation = translate(summary.content, "french")
print(translation.content)
