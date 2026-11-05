import streamlit as st

from components import (
    LAB_DB,
    LAB_WH,
    attendee_schema,
    render_build_click,
    render_catch_up,
    render_check,
    render_expected,
    render_explanation,
    render_guide_ref,
    render_new_chat,
    render_presenter,
    render_prompt,
    render_session_header,
    render_split,
    render_troubleshoot,
    render_whats_happening,
    render_what_you_built,
)

render_session_header("Module 1", "Create an AGENTS.md", "15 min", "project context CoCo reads every session, and starter code brought up to your conventions")

render_split(
    you=["Paste two prompts", "Read what CoCo wrote, click **Keep**", "Click **Build**"],
    coco=["Writes AGENTS.md from your list", "Audits the starter models against it", "Fixes the violation it finds"],
)

render_explanation("What is AGENTS.md? (read this first)", """
`AGENTS.md` is a Markdown file at the top of your project with the conventions, context and commands you want the agent to know **every session, automatically**.
Without it you'd re-explain your database names, naming conventions and preferred commands in every new chat. With it, that context is always there.

Think of it as the onboarding document you'd write for a new team member, except this one reads it perfectly every time. Jeremiah's three rules:
- **Keep it short.** Every line uses up the agent's attention. Does it *actually* need this sentence?
- **Encode what the model can't infer.** Don't explain how dbt works; CoCo knows. Do write down *your* database, schema and build command.
- **Stable facts only.** Things that don't change from session to session go here; today's task goes in your prompt.
""")

render_new_chat()

# ---------------------------------------------------------------- Step 1
st.markdown("#### Step 1: Create your AGENTS.md")
render_guide_ref("Create an AGENTS.md → Create Your AGENTS.md", f"your own schema {attendee_schema()}; dbt runs in Snowflake, so no --project-dir and no local install")
render_whats_happening("You're handing CoCo a list of team facts. It turns them into a tidy file and shows it to you before saving. Nothing runs in Snowflake yet.")

PROMPT_1_1 = f"""Create an AGENTS.md file at the root of this project. Include:
- The Snowflake database ({LAB_DB}), schema ({attendee_schema()}), and warehouse ({LAB_WH})
- dbt runs inside Snowflake for this project (Snowflake-managed mode): never install dbt or run dbt in a terminal. I run builds with the Build button on the Project Action Bar
- The dbt build command to use: `dbt build`
- The command to build a single model: `dbt build --select <model_name>`
- Snake_case naming convention for model files
- The source data is TPCH_SF1 in SNOWFLAKE_SAMPLE_DATA; all raw tables must be referenced through _sources.yml
- This project uses CoCo Desktop — do not use the `cortex` CLI command"""
render_prompt("Prompt 1.1", "Create AGENTS.md", PROMPT_1_1)

st.markdown("CoCo shows the new file with **Keep** and **Undo** buttons. Read it, then click **Keep**. Yours may be worded differently, and that's OK. It should look something like this, and the schema must be **" + attendee_schema() + "**:")
st.code(f"""# Project: tricon_coco_lab

## Snowflake
- Database: {LAB_DB}
- Schema: {attendee_schema()}
- Warehouse: {LAB_WH}

## dbt Commands
- dbt runs inside Snowflake (Snowflake-managed). Never install dbt or use a terminal; builds run from the Project Action Bar
- Build + test: `dbt build`
- Single model: `dbt build --select <model_name>`

## Naming Conventions
- Model files: snake_case
- Source schema: TPCH_SF1 in SNOWFLAKE_SAMPLE_DATA (always via _sources.yml)

## CoCo
- This project uses CoCo Desktop — do not use the `cortex` CLI command""", language="markdown")
st.caption("Why the last line? CoCo has bundled skills that know the `cortex` CLI and can try to use it. This line stops that, exactly as in the guide.")
st.caption("What's not here from the guide: the feature-branch and pull-request rules. There's no Git in this version, so we left them out.")

# ---------------------------------------------------------------- Step 2
st.markdown("#### Step 2: Validate the starter code against your conventions")
render_guide_ref("Validate the Starter Code Against Your Conventions")
render_whats_happening("The starter project was written **before** these rules existed, which is exactly what happens when you inherit someone's code. You ask CoCo to check the code against AGENTS.md and fix what's wrong.")

PROMPT_1_2 = """Review all dbt models in this project against the conventions in AGENTS.md
and fix any violations you find."""
render_prompt("Prompt 1.2", "Audit and Fix the Starter Models", PROMPT_1_2)
render_expected("CoCo finds that `orders_summary.sql` reads the raw tables by their full Snowflake names instead of through `_sources.yml`, and proposes the fix below. Click **Keep**.")
col1, col2 = st.columns(2)
col1.code("""-- Violation: direct source reference
FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS o
LEFT JOIN SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.LINEITEM l ...""", language="sql")
col2.code("""-- Fixed: references go through _sources.yml
FROM {{ source('tpch', 'orders') }} o
LEFT JOIN {{ source('tpch', 'lineitem') }} l ...""", language="sql")
st.caption("Why it matters: if the raw data ever moves, you change one line in `_sources.yml` instead of hunting through every model. dbt can also draw the lineage diagram only when models use `source()`.")

# ---------------------------------------------------------------- Step 3
st.markdown("#### Step 3: Build to confirm nothing broke")
render_guide_ref("Validate the Starter Code → run dbt build", "you click Build instead of typing dbt build in a terminal")
render_build_click("Build")
render_expected(f"**Success**: both models rebuilt in {LAB_DB}.{attendee_schema()} (no tests yet; Module 2 adds them).")

render_troubleshoot([
    ("AGENTS.md landed inside `models/`", "Ask: *Move AGENTS.md to the root of the project.*"),
    ("It says `TPCH_TRANSFORMED` or `<INITIALS>`", f"Type your initials in the sidebar and copy Prompt 1.1 again, or edit the file: schema `{attendee_schema()}`, then save (`CMD/CTRL+S`)."),
    ("CoCo found no violations", "Ask: *Check the FROM and JOIN lines in orders_summary.sql against the _sources.yml rule.*"),
    ("CoCo tries to install dbt or open a terminal", "Reply: *No. AGENTS.md says dbt runs in Snowflake; I'll click Build.*"),
    ("You clicked **Undo** by mistake", "Send the prompt again."),
])
render_check(f"""Check Module 1, change nothing: AGENTS.md is at the project root and names schema {attendee_schema()}; no file in models/ contains SNOWFLAKE_SAMPLE_DATA; the last build in target/run_results.json succeeded. PASS or FAIL for each.""")
render_catch_up("""Catch me up on Module 1: copy solutions/m1_AGENTS.md to AGENTS.md at the project root, and copy solutions/m1_orders_summary.sql over models/orders_summary.sql. Then tell me to click Build.""")

render_explanation("Why this matters", """
CoCo wasn't told what the violation was or what the fix should look like. It read the conventions, read the code and connected the two.
That's the value: not one dramatic prompt, but **every** prompt in the session grounded in your actual standards instead of the model's best guess.

**Tip from the guide:** any time you repeat the same context in several prompts (a convention, a command, a constraint), that's a sign it belongs in AGENTS.md.
""")

render_what_you_built([
    "AGENTS.md: project context CoCo reads in every chat",
    "Starter code brought up to the convention, reviewed and approved by you",
    f"Both models rebuilt in {LAB_DB}.{attendee_schema()}, with dbt running inside Snowflake",
])

render_presenter("""
**Jeremiah's framing:** "Anyone can get an agent to produce a result. Professionals ensure the right result, every time." AGENTS.md is step one.

**Demo beat:** after Prompt 1.2, show the before/after of `orders_summary.sql` on screen. Point out that nobody told CoCo what was wrong.

**If asked "is this like a README?":** yes, but written for the agent. It's loaded automatically into every chat.

**Timing:** ~5 min explaining, ~10 min hands-on. Don't wait for every Build to finish before moving on.
""")
