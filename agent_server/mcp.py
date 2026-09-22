from databricks.sdk import WorkspaceClient
from databricks_openai.agents import McpServer

from agent_server.config import CATALOG, SECOP_AI_TOOLS_SCHEMA


def build_mcp_url(
    workspace_client: WorkspaceClient,
    catalog: str,
    schema: str,
) -> str:
    """Build the managed MCP endpoint for all UC functions in a schema."""
    host = workspace_client.config.host.rstrip("/")
    return f"{host}/api/2.0/mcp/functions/{catalog}/{schema}"


def create_secop_ai_mcp(workspace_client: WorkspaceClient) -> McpServer:
    """Create the managed MCP connection used by the SECOP AI agent."""
    return McpServer(
        url=build_mcp_url(
            workspace_client=workspace_client,
            catalog=CATALOG,
            schema=SECOP_AI_TOOLS_SCHEMA,
        ),
        name="secop-ai-tools",
        workspace_client=workspace_client,
    )
