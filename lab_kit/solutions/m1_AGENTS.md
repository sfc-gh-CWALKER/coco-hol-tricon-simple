# Project: Tricon CoCo Lab

## Snowflake
- Database: DEMO_DB
- Schema: TPCH_<INITIALS> (my schema; never write anywhere else)
- Warehouse: DEMO_WH
- Role: DEMO_ROLE

## dbt
- dbt runs inside Snowflake (CoCo Desktop Snowflake-managed mode). Never install dbt or use a terminal.
- Always use `dbt build` (not `dbt run`) so tests run too.
- Single model: `dbt build --select <model_name>`
- Never use `--target prod`. There is only the `dev` target.

## Conventions
- Model files: snake_case
- Raw data is SNOWFLAKE_SAMPLE_DATA.TPCH_SF1. Reference it only through `{{ source('tpch', '<table>') }}` (models/_sources.yml), never by its full name.
- Every model's primary key has `not_null` and `unique` tests in models/_schema.yml.

## Working style
- Show me changes before saving them. Never drop or replace objects outside my schema.
- Do not use the `cortex` CLI, git, or any terminal command.
