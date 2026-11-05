import streamlit as st

from components import (
    LAB_DB,
    LAB_ROLE,
    LAB_WH,
    attendee_schema,
    render_build_click,
    render_catch_up,
    render_check,
    render_expected,
    render_explanation,
    render_new_chat,
    render_prompt,
    render_session_header,
    render_split,
    render_troubleshoot,
    render_what_you_built,
)

render_session_header("Module 1", "Teach CoCo Your Team's Rules", "20 min", "an AGENTS.md CoCo reads every session, and starter code that follows it")

render_split(
    you=["Paste three prompts", "Read what CoCo changed and click **Keep**", "Click **Build**"],
    coco=["Writes AGENTS.md", "Audits the starter models against it", "Fixes the violation it finds"],
)

render_explanation("What is AGENTS.md?", """
A short file at the top of the project with the rules you'd tell a new teammate: which database and schema to use, how to build, naming conventions, what never to do.
CoCo reads it **automatically at the start of every chat**, so you stop repeating yourself. It's the first thing to set up on a real Tricon project.
""")

render_new_chat()

PROMPT_1_1 = f"""Create AGENTS.md at the top level of this project (next to dbt_project.yml). Keep it under 25 lines. Include:
- Snowflake: database {LAB_DB}, schema {attendee_schema()} (my schema; never write anywhere else), warehouse {LAB_WH}, role {LAB_ROLE}
- dbt runs inside Snowflake (Snowflake-managed mode). Never install dbt or use a terminal; I run builds from the Project Action Bar
- Always dbt build, never dbt run. Never use --target prod; dev is the only target
- Model files are snake_case
- Raw data is SNOWFLAKE_SAMPLE_DATA.TPCH_SF1 and must only be referenced through source('tpch', ...) in models/_sources.yml
- Every model's primary key needs not_null and unique tests in models/_schema.yml
- Show me changes before saving. Don't use the cortex CLI or git"""
render_prompt("Prompt 1.1", "Write AGENTS.md", PROMPT_1_1)
render_expected(f"A new `AGENTS.md` at the top of the Explorer that names **{attendee_schema()}**. Click **Keep** to save it.")

PROMPT_1_2 = """Using only the rules in AGENTS.md, audit every model in models/.
List each violation as: file, line, rule broken, fix. Don't change anything yet."""
render_prompt("Prompt 1.2", "Audit the Starter Code", PROMPT_1_2)
render_expected("CoCo finds that **`orders_summary.sql` references `SNOWFLAKE_SAMPLE_DATA` directly** instead of `source()`. That violation was planted on purpose.")

PROMPT_1_3 = """Fix the violations you found. Show me the change, then save it.
Tell me when to click Build on the Project Action Bar, and after I say "built", check the run results in target/run_results.json and tell me PASS or FAIL."""
render_prompt("Prompt 1.3", "Fix It and Verify", PROMPT_1_3)
render_build_click("Build")
render_expected("The build succeeds, and CoCo reports **PASS** after reading the results. The tables in your schema are rebuilt.")

render_troubleshoot([
    ("AGENTS.md landed inside `models/`", "Ask: *Move AGENTS.md to the top level of the project.*"),
    ("CoCo found no violations", "Ask: *Check orders_summary.sql's FROM and JOIN lines against the source() rule.*"),
    ("CoCo can't find target/run_results.json", "The build hasn't synced back yet. Wait for it to finish, then say *built* again."),
    ("CoCo starts installing dbt", "Stop it: *No installs. AGENTS.md says dbt runs in Snowflake.*"),
])
render_check(f"""Check Module 1: AGENTS.md exists at the top level and names schema {attendee_schema()}; no file in models/ contains SNOWFLAKE_SAMPLE_DATA; the last dbt build in target/run_results.json succeeded. Answer PASS or FAIL for each.""")
render_catch_up("""Catch me up on Module 1: copy solutions/m1_AGENTS.md to AGENTS.md at the top level, and copy solutions/m1_orders_summary.sql over models/orders_summary.sql. Then tell me to click Build.""")

render_what_you_built([
    "AGENTS.md: team rules CoCo follows in every chat",
    "Starter code brought up to standard by CoCo, reviewed and approved by you",
    f"Tables rebuilt in {LAB_DB}.{attendee_schema()} by dbt running in Snowflake",
])
