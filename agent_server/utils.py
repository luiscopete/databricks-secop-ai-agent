from typing import AsyncGenerator, AsyncIterator
from uuid import uuid4

from agents.result import StreamEvent
from mlflow.types.responses import ResponsesAgentRequest, ResponsesAgentStreamEvent


def get_session_id(request: ResponsesAgentRequest) -> str | None:
    """Return a conversation/session identifier when the caller supplied one."""
    if request.context and request.context.conversation_id:
        return request.context.conversation_id

    if request.custom_inputs and isinstance(request.custom_inputs, dict):
        return request.custom_inputs.get("session_id")

    return None


async def process_agent_stream_events(
    async_stream: AsyncIterator[StreamEvent],
) -> AsyncGenerator[ResponsesAgentStreamEvent, None]:
    """Translate OpenAI Agents SDK stream events to MLflow Responses events."""
    current_item_id = str(uuid4())

    async for event in async_stream:
        if event.type == "raw_response_event":
            event_data = event.data.model_dump()

            if event_data.get("type") == "response.output_item.added":
                current_item_id = str(uuid4())
                if event_data.get("item") is not None:
                    event_data["item"]["id"] = current_item_id
            elif event_data.get("item") is not None and event_data["item"].get("id") is not None:
                event_data["item"]["id"] = current_item_id
            elif event_data.get("item_id") is not None:
                event_data["item_id"] = current_item_id

            yield event_data

        elif event.type == "run_item_stream_event" and event.item.type == "tool_call_output_item":
            yield ResponsesAgentStreamEvent(
                type="response.output_item.done",
                item=event.item.to_input_item(),
            )
