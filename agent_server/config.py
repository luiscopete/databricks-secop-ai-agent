import os

CATALOG = os.getenv("CATALOG", "secop_ai")
SECOP_AI_TOOLS_SCHEMA = os.getenv("SECOP_AI_TOOLS_SCHEMA", "ai_agents_tools")
MODEL_ENDPOINT = os.getenv("MODEL_ENDPOINT", "databricks-meta-llama-3-3-70b-instruct")
