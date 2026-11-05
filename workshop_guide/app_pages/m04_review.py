import streamlit as st

from components import (
    ORIGINAL_APP,
    render_catch_up,
    render_check,
    render_expected,
    render_explanation,
    render_guardrail,
    render_new_chat,
    render_prompt,
    render_session_header,
    render_split,
    render_troubleshoot,
    render_what_you_built,
)

render_session_header("Module 4", "A Reviewer That Never Changes Code", "15 min", "a read-only dbt-review agent that checks work before a person approves it")

render_split(
    you=["Paste two prompts", "Decide which suggested fixes to accept"],
    coco=["Creates the review agent", "Reviews every model and reports PASS/FAIL", "Applies only the fixes you approve"],
)

render_explanation("What is a subagent?", """
A subagent is a specialist CoCo hands a job to. This one is a **reviewer**: it can read files, but it has no permission to edit them.
That's the Build Week rule in miniature: **agents propose, people approve.** Teams usually run this before every pull request.
""")

render_new_chat()

PROMPT_4_1 = """Create a project subagent at .cortex/agents/dbt-review.md.
Front matter: name dbt-review; description "Review this project's dbt models against AGENTS.md and report PASS/FAIL per convention. Read-only."; tools: read, grep, glob only (no write or edit); model: auto.
Instructions: for every .sql file in models/, check (1) no SNOWFLAKE_SAMPLE_DATA or other three-part raw names, (2) primary key has not_null and unique tests in models/_schema.yml, (3) snake_case file name, (4) has a description.
Output one table: model | check | PASS/FAIL | suggested fix, then "Overall: PASS" or "Overall: FAIL (n issues)". Never edit files.
Show me the file, then save it."""
render_prompt("Prompt 4.1", "Create the Reviewer", PROMPT_4_1)
render_expected("A new file `.cortex/agents/dbt-review.md` whose tool list has **no write or edit**.")

PROMPT_4_2 = """Use the dbt-review agent to review all models. Show me its table.
Then ask me which suggested fixes to apply, and apply only the ones I approve."""
render_prompt("Prompt 4.2", "Run the Review", PROMPT_4_2)
render_expected("A review table for `customers`, `orders_summary` and `supplier_performance`, ending with **Overall: PASS** or a short list of fixes for you to approve.")
render_guardrail("The reviewer can't change code; you decide what gets fixed. In Build Week, this is the step before a pull request.")

render_troubleshoot([
    ("CoCo reviews the models itself instead of using the agent", "Ask: *Run this with the dbt-review subagent.* If it still isn't found, reopen the folder and start a new chat."),
    ("The reviewer edits a file", "Click **Undo** and check the agent's `tools:` line has only read, grep, glob."),
])
render_check("""Check Module 4: .cortex/agents/dbt-review.md exists and its tools are only read, grep and glob. Then run it and tell me the overall result.""")
render_catch_up("""Catch me up on Module 4: copy solutions/m4_agent/dbt-review.md to .cortex/agents/dbt-review.md, start the dbt-review subagent on all models, and show me its table.""")

render_what_you_built([
    "A read-only dbt-review agent the team can run before every pull request",
    "A review of every model, with you deciding which fixes go in",
])

st.markdown("#### Going further (facilitator demo, not hands-on today)")
with st.container(border=True):
    st.markdown(f"""
Packaging the skill and reviewer as a **plugin**, a **prod-safety hook**, publishing to the **Plugins Catalog**, and running the review in **GitHub Actions** on every pull request.
The facilitator will show these live. To try them later, see the [full lab guide]({ORIGINAL_APP}). It needs Git and a local dbt install.
""")
