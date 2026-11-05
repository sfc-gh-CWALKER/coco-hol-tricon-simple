import streamlit as st

from components import (
    attendee_schema,
    LAB_DB,
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

render_session_header("Module 3", "Turn a Standard into a Skill", "20 min", "a reusable new-dbt-model skill, and a new model built with it")

render_split(
    you=["Paste two prompts", "Approve the skill and the new model", "Click **Build**"],
    coco=["Writes the skill file", "Uses it to build a supplier model the team's way", "Adds tests automatically"],
)

render_explanation("What is a skill?", """
A skill is a saved, step-by-step recipe CoCo follows when asked, for example *how our team builds a new dbt model*.
AGENTS.md says **what** the rules are; a skill says **how** to do a recurring task the same way every time.
Skills in this project's `.cortex/skills/` folder are shared with anyone who opens the project, which is how a team standard spreads.
""")

render_new_chat()

PROMPT_3_1 = """Create a project skill at .cortex/skills/new-dbt-model/SKILL.md.
Front matter: name new-dbt-model, and a description saying to use it when adding a dbt model to this project.
Body, under 25 lines:
- Conventions: raw tables only via source('tpch', ...); snake_case file names; primary key gets not_null and unique tests plus a description in models/_schema.yml
- Workflow: 1) confirm the source tables and the grain (one row per what?), 2) write models/<name>.sql, 3) add tests and description to models/_schema.yml, 4) tell me to click Build, 5) read target/run_results.json and report built yes/no, tests passed, row count
- Never install dbt, use a terminal, or use --target prod
Show me the file, then save it."""
render_prompt("Prompt 3.1", "Create the Skill", PROMPT_3_1)
render_expected("A new file `.cortex/skills/new-dbt-model/SKILL.md` in the Explorer. In the chat, type `/` and **new-dbt-model** appears in the list (if not, close and reopen the folder).")

PROMPT_3_2 = """Use the new-dbt-model skill to create a supplier_performance model: one row per supplier,
with total orders, total revenue (extended price after discount) and average discount, from the supplier and lineitem source tables."""
render_prompt("Prompt 3.2", "Build a Model with the Skill", PROMPT_3_2)
render_build_click("Build")
render_expected(f"CoCo followed the recipe without being told: `models/supplier_performance.sql` uses `source()`, the key has tests in `_schema.yml`, and the build succeeds. Table **{LAB_DB}.{attendee_schema()}.SUPPLIER_PERFORMANCE** exists.")

render_troubleshoot([
    ("`/` doesn't list new-dbt-model", "**File → Open Recent** → reopen the same folder, then start a new chat. The file must be exactly `.cortex/skills/new-dbt-model/SKILL.md`."),
    ("CoCo writes `SNOWFLAKE_SAMPLE_DATA` in the model", "Ask: *Follow the new-dbt-model skill's conventions.* That's the skill doing its job on review."),
    ("The build fails on supplier_performance", "Paste the error into the chat: *Explain this and propose a fix.*"),
])
render_check(f"""Check Module 3: .cortex/skills/new-dbt-model/SKILL.md exists with name new-dbt-model; models/supplier_performance.sql uses source() only; it has not_null and unique tests on its key; the last build succeeded. PASS or FAIL for each.""")
render_catch_up("""Catch me up on Module 3: copy solutions/m3_skill/SKILL.md to .cortex/skills/new-dbt-model/SKILL.md, then run Prompt 3.2 for me using that skill.""")

render_what_you_built([
    "A new-dbt-model skill your whole team can reuse",
    "supplier_performance, built to the team standard by following the skill",
])
