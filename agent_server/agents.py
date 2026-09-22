import logging

from agents import Agent
from databricks_openai.agents import McpServer

from agent_server.config import MODEL_ENDPOINT


logger = logging.getLogger(__name__)


def create_secop_ai_agent(secop_ai_mcp: McpServer) -> Agent:

    """Create the single SECOP AI agent and attach its managed MCP tools."""

    # Temporary debug log to verify which model
    # the Databricks App is actually using.
    logger.info(
        "Creating SECOP AI agent with model endpoint: %s",
        MODEL_ENDPOINT,
    )

    return Agent(
        name="SECOP AI Agent",

        instructions="""
You are a specialized AI agent for querying Colombian government contract data
from SECOP (Sistema Electrónico de Contratación Pública).

Help users find and analyze government contract opportunities using natural
language queries.

Use the available tools whenever contract data must be retrieved. You can
search by budget range, entity (NIT), location (department), contract type,
recent contracts, high-value contracts, files, and statistical summaries.

Never invent contract information. If the tools do not return relevant data,
say that no relevant information was found. Base factual claims about SECOP
contracts on tool results.
""".strip(),

        model=MODEL_ENDPOINT,

        mcp_servers=[secop_ai_mcp],
    )