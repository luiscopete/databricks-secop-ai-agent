# Unity Catalog tools

These files are the source-controlled definitions of the Unity Catalog tools
exposed to the SECOP AI Agent through Databricks Managed MCP.

The SQL functions are deployed under `secop_ai.ai_agents_tools`.

`fetch_contract_files` is implemented in Python and retrieves contract file
metadata from the Colombian `datos.gov.co` API.

Unity Catalog is the runtime/deployed representation, while this directory is
the source of truth in Git.

The agent discovers the deployed functions through the Managed MCP endpoint.

`search_contracts` is referenced by the project, but its source definition is
not yet included in this directory because its definition was not provided.
