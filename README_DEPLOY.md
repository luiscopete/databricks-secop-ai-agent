# SECOP AI deployment checklist

## 1. Install and lock dependencies

```bash
uv sync
```

This creates/updates `uv.lock`.

## 2. Local authentication

Use an existing Databricks CLI profile or copy `.env.example` to `.env` and set the profile name.

## 3. Test the backend first

```bash
uv run start-server
```

Then, in another terminal, call `/health` or stop it and run:

```bash
uv run preflight
```

## 4. Get the MLflow experiment ID

Use the experiment where you want the agent traces stored. Keep the numeric/string experiment ID.

## 5. Validate the bundle

```bash
databricks bundle validate -t dev --var="experiment_id=<YOUR_EXPERIMENT_ID>" --profile work-dev
```

## 6. Deploy

```bash
databricks bundle deploy -t dev --var="experiment_id=<YOUR_EXPERIMENT_ID>" --profile work-dev
```

## 7. Start/redeploy the App if required by your CLI/template flow

```bash
databricks bundle run secop_ai -t dev --var="experiment_id=<YOUR_EXPERIMENT_ID>" --profile work-dev
```

## Environment isolation

The same source code can target another catalog/model by overriding bundle variables, for example:

```bash
databricks bundle deploy -t prod \
  --var="experiment_id=<PROD_EXPERIMENT_ID>" \
  --var="catalog=secop_ai_prod" \
  --var="tools_schema=ai_agents_tools" \
  --var="model_endpoint=databricks-gpt-oss-120b" \
  --profile work-prod
```
