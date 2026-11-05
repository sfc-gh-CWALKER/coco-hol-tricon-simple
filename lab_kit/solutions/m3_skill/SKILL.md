---
name: new-dbt-model
description: Create a new dbt model in this project following team conventions. Use when adding a model for a new source table or analytical use case.
---

# Conventions
1. Raw tables only through `{{ source('tpch', '<table>') }}` (models/_sources.yml). Never write SNOWFLAKE_SAMPLE_DATA in model SQL.
2. File name is snake_case and matches the model name.
3. The primary key gets `not_null` and `unique` tests in models/_schema.yml, plus a one-line description.
4. Build with `dbt build --select <model_name>` in Snowflake-managed mode. Never install dbt, use a terminal, or use `--target prod`.

# Workflow
1. Confirm the source tables and the grain (one row per what?). Ask if unclear.
2. Write models/<model_name>.sql.
3. Add the model to models/_schema.yml with a description and tests.
4. Run the build and report: model built yes/no, tests passed/failed, row count.
5. If anything fails, show the error and propose a fix. Don't retry more than twice.
