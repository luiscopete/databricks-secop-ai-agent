import logging
from contextlib import AsyncExitStack
from typing import AsyncGenerator

import mlflow
from agents import Runner, set_default_openai_api, set_default_openai_client
from agents.tracing import set_trace_processors
from databricks.sdk import WorkspaceClient
from databricks_openai import AsyncDatabricksOpenAI
from mlflow.genai.agent_server import invoke, stream
from mlflow.types.responses import (
    ResponsesAgentRequest,
    ResponsesAgentResponse,
    ResponsesAgentStreamEvent,
)

from agent_server.agents import create_secop_ai_agent
from agent_server.history import normalize_history_items
from agent_server.mcp import create_secop_ai_mcp
from agent_server.utils import get_session_id, process_agent_stream_events

logger = logging.getLogger(__name__)

# OpenAI Agents SDK -> Databricks Foundation Model API.
# This configuration matches the tool-calling flow already validated in the notebook.
set_default_openai_client(AsyncDatabricksOpenAI())
set_default_openai_api("chat_completions")

# Use MLflow as the tracing backend instead of OpenAI's trace exporters.
set_trace_processors([])
mlflow.openai.autolog()
logging.getLogger("mlflow.utils.autologging_utils").setLevel(logging.ERROR)


async def _create_connected_agent(stack: AsyncExitStack):
    """Connect the required MCP server, verify it, and create the agent."""
    workspace_client = WorkspaceClient()

    secop_ai_mcp = create_secop_ai_mcp(workspace_client)
    secop_ai_mcp = await stack.enter_async_context(secop_ai_mcp)

    # Fail early if the App service principal cannot discover the UC functions.
    tools = await secop_ai_mcp.list_tools()
    logger.info("SECOP AI MCP connected with %s tools", len(tools))

    return create_secop_ai_agent(secop_ai_mcp)


@invoke()
async def invoke_handler(
    request: ResponsesAgentRequest,
) -> ResponsesAgentResponse:
    """Handle a non-streaming request from MLflow AgentServer."""
    if session_id := get_session_id(request):
        mlflow.update_current_trace(metadata={"mlflow.trace.session": session_id})

    async with AsyncExitStack() as stack:
        secop_ai_agent = await _create_connected_agent(stack)

        messages = normalize_history_items(
            [item.model_dump() for item in request.input]
        )

        result = await Runner.run(
            secop_ai_agent,
            input=messages,
        )

        return ResponsesAgentResponse(
            output=[item.to_input_item() for item in result.new_items]
        )


@stream()
async def stream_handler(
    request: ResponsesAgentRequest,
) -> AsyncGenerator[ResponsesAgentStreamEvent, None]:
    """Handle a streaming request from MLflow AgentServer/chat UI."""
    if session_id := get_session_id(request):
        mlflow.update_current_trace(metadata={"mlflow.trace.session": session_id})

    async with AsyncExitStack() as stack:
        secop_ai_agent = await _create_connected_agent(stack)

        messages = normalize_history_items(
            [item.model_dump() for item in request.input]
        )

        result = Runner.run_streamed(
            secop_ai_agent,
            input=messages,
        )

        async for event in process_agent_stream_events(result.stream_events()):
            yield event
