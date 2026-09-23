# Unity Catalog tools

These files are the source-controlled definitions of the Unity Catalog tools
exposed to the SECOP AI Agent through Databricks Managed MCP.

The SQL functions are deployed under the catalog and schemas supplied through
the Bundle variables `catalog`, `tools_schema`, and `gold_schema`. The runtime
Unity Catalog objects are the deployed representation; this directory is the
source of truth in Git.

## Deployment

The deployment flow is:

1. Configure the Bundle variables, including an existing SQL Warehouse ID for
   `sql_warehouse_id`.
2. Deploy the Bundle.
3. Run the UC deployment Job.

For example, provide the warehouse ID at validation/deployment time without
committing it to the public repository:

```bash
databricks bundle validate -t dev --var sql_warehouse_id=<EXISTING_SQL_WAREHOUSE_ID>
databricks bundle deploy -t dev --var sql_warehouse_id=<EXISTING_SQL_WAREHOUSE_ID>
databricks bundle run deploy_uc_tools -t dev --var sql_warehouse_id=<EXISTING_SQL_WAREHOUSE_ID>
```

Once `sql_warehouse_id` is supplied through the target or the execution
environment, the standard flow is:

```bash
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run deploy_uc_tools -t dev
```

The SQL tasks require Databricks SQL and an existing SQL Warehouse. The
Warehouse must be running or available when the Job runs.

The responsibilities are separated as follows:

```text
uc_tools/*
    = source of truth

deploy_uc_tools
    = creates or replaces the UC functions

databricks.yml App uc_securable resources
    = grant EXECUTE to the Databricks App service principal

Managed MCP
    = exposes the deployed UC functions to the agent
```

The Bundle synchronizes these files into the workspace. The Job uses the
Bundle-deployed workspace files and does not configure a remote Git source.

`fetch_contract_files` is implemented in Python and retrieves contract file
metadata from the Colombian `datos.gov.co` API. Its current deployed Unity
Catalog Python function definition could not be retrieved without selecting a
Databricks workspace profile, so it remains manual and is not included in the
deployment Job.

`search_contracts` is referenced by the App, but its implementation is still
missing from source control. It is not included in the deployment Job.
