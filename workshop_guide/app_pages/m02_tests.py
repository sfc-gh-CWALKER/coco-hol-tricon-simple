import streamlit as st

from components import (
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

render_session_header("Module 2", "Add Data Quality Tests", "15 min", "tests that run on every build and catch bad data before anyone sees it")

render_split(
    you=["Paste two prompts", "Approve the tests", "Click **Build**"],
    coco=["Profiles the data", "Writes tests that match it", "Reads the results and explains any failure"],
)

render_explanation("Why tests?", """
A test is a rule the data must follow: *every order has a customer*, *status is F, O or P*, *keys are unique*.
dbt runs them on every **Build**, so a broken pipeline or a stale table shows up as a failed test, not as a wrong number in a report.
This is the foundation for Joel's "pipeline health" pain point.
""")

render_new_chat()

PROMPT_2_1 = """Add data quality tests for both models in a new file models/_schema.yml.
First query the data in my schema to see real values, so the tests match it (for example the actual order_status values).
Include: not_null and unique on each primary key, a relationships test from orders_summary.customer_key to customers,
and accepted_values where a column has a small fixed set of values. Give each model a one-line description.
For accepted_values and relationships, nest the parameters under an arguments: key.
Show me the file, save it, then tell me to click Build."""
render_prompt("Prompt 2.1", "Write the Tests", PROMPT_2_1)
render_build_click("Build")
render_expected("The build succeeds with **all tests passing** (about 10 or more, depending on what CoCo chose).")

PROMPT_2_2 = """I clicked Build. Read target/run_results.json and summarize in plain language: how many tests ran, how many passed,
and for any failure, what it means for the data and the smallest fix. Don't change files unless I say so."""
render_prompt("Prompt 2.2", "Explain the Results", PROMPT_2_2)
render_expected("A short, plain-language summary: *N tests, all passed*, or one sentence per failure.")

render_troubleshoot([
    ("A test on `order_status` fails", "TPC-H statuses are **F, O, P**. Ask: *Fix the accepted_values for order_status to match the data.*"),
    ("*'arguments' is not a valid key*", "Your dbt version expects the older layout. Ask: *Remove the arguments: wrapper from the tests.*"),
    ("Build says *0 tests*", "`_schema.yml` isn't in `models/`. Ask CoCo to move it there, then Build again."),
])
render_check("""Check Module 2: models/_schema.yml exists with not_null and unique on both primary keys, and the last build in target/run_results.json has no failed tests. Answer PASS or FAIL.""")
render_catch_up("""Catch me up on Module 2: copy solutions/m2_schema.yml to models/_schema.yml, then tell me to click Build.""")

render_what_you_built([
    "models/_schema.yml: tests and descriptions for both models",
    "A build that fails loudly when the data breaks the rules",
])
