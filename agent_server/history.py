"""Helpers for replaying conversation history through OpenAI Agents SDK."""


def normalize_history_items(messages: list[dict]) -> list[dict]:
    """Normalize assistant history that does not contain an SDK message id.

    MLflow ResponsesAgent input can replay assistant messages without an ``id``.
    OpenAI Agents SDK accepts these reliably when represented as the simple
    ``{"role": "assistant", "content": ...}`` input form.
    """
    normalized: list[dict] = []

    for message in messages:
        if message.get("type") != "message" or message.get("role") != "assistant":
            normalized.append(message)
            continue

        content = message.get("content")

        if isinstance(content, str):
            normalized.append({"role": "assistant", "content": content})
            continue

        if isinstance(content, list) and "id" not in message:
            text_parts = []
            for part in content:
                if isinstance(part, dict) and part.get("type") == "output_text":
                    text_parts.append(part.get("text", ""))

            normalized.append(
                {
                    "role": "assistant",
                    "content": "\n".join(text_parts),
                }
            )
            continue

        normalized.append(message)

    return normalized
