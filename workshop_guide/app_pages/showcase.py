import streamlit as st

from components import (
    LAB_DB,
    attendee_schema,
    render_expected,
    render_guardrail,
    render_new_chat,
    render_prompt,
    render_takeaway,
    render_whats_happening,
)

st.title("Automation Showcase (optional, 20 min)")
st.markdown(f"""
The facilitator demos these live. Try any that look useful: each one is a **single prompt**, works only inside your schema **{LAB_DB}.{attendee_schema()}**, and **only proposes**. Nothing is changed until you say so.
Any of them can become your **Build Week** project.
""")
render_guardrail("Every prompt here ends with a proposal for a person to review. In Build Week: agents propose, people approve, nothing touches production.")
render_new_chat()

st.markdown("#### A1. Pipeline health: stale and broken tables")
st.caption("Joel's pain point: *monitoring for broken pipelines and stale tables*.")
render_whats_happening("""CoCo queries Snowflake's own metadata (row counts, last-altered times) and reads the last dbt build results, then writes a plain-language report. In the second prompt you save that recipe as a **skill**, so next time it's a one-liner.""")
render_prompt("Prompt A1.1", "Freshness Check", f"""In {LAB_DB}.{attendee_schema()}, list every table with its row count and last-altered time (INFORMATION_SCHEMA.TABLES).
Flag any table not updated in the last 24 hours as STALE and any table with 0 rows as EMPTY.
Then read target/run_results.json and list any failed models or tests.
Write a short health report to reports/pipeline_health.md: a status table, then "what to check first" in plain language. Don't change anything else.""")
render_prompt("Prompt A1.2", "Make It Repeatable", """Turn what you just did into a project skill at .cortex/plugins/coco-de-guide/skills/pipeline-health/SKILL.md (inside your plugin from Module 3), so anyone on the team can run "check pipeline health" and get the same report.
Show me the file, then save it.""")
render_expected("`reports/pipeline_health.md` with a status table, and a `pipeline-health` skill your team can reuse.")
render_takeaway(
    """One prompt checks every table for freshness and emptiness, reads the latest build and test results, and writes a report a person can act on. The second prompt turns that into a reusable skill inside your plugin.""",
    """Stale or broken tables are usually found by the business, in a report, after the fact. This flips it: the data team gets a "what to check first" list before anyone else notices.
For Build Week this could run against real Tricon pipelines, for example a daily Yardi load check, shared with the team as a plugin skill.""",
)

st.markdown("#### A2. Sensitive data sweep")
render_whats_happening("""CoCo looks at column names and a small sample of rows to spot data that looks personal or sensitive, then **drafts** the masking policy SQL into a file. It doesn't run it: a person reviews and approves first.""")
render_prompt("Prompt A2.1", "Find Sensitive Columns", f"""Look at every table in {LAB_DB}.{attendee_schema()}. Using column names and a 10-row sample of each,
list columns that look like personal or sensitive data (names, phones, addresses, account balances) as a table: table, column, why, suggested protection.""")
render_prompt("Prompt A2.2", "Propose the Policy", f"""Write the SQL for a masking policy that hides those columns from everyone except a role named DEMO_PII_READER, to proposals/masking.sql,
with a comment above each statement saying which finding it addresses. Do NOT run it. Tell me who should approve it.""")
render_expected("A findings table and `proposals/masking.sql`, **not executed**.")
render_takeaway(
    """An agent can do a first-pass sensitive-data review across a whole schema in minutes and write the exact policy SQL, while the decision and the execution stay with a person.""",
    """Tenant names, phone numbers, addresses and balances are exactly the data you can't let leak into AI answers. Masking policies protect it everywhere at once: in queries, dashboards and agents.
Drafting them is slow and easy to put off. Here it's done in minutes, ready for your governance or security lead to approve.""",
)

st.markdown("#### A3. A recurring KPI report, as an HTML page")
st.caption("Joel's pain point: *one home for reporting, including HTML artifacts*.")
render_whats_happening("""CoCo runs the SQL itself, builds a self-contained HTML page from the results, and then explains the biggest change using only numbers it queried. No copying into spreadsheets or slides.""")
render_prompt("Prompt A3.1", "Build the Report", f"""Using {LAB_DB}.{attendee_schema()}.ORDERS_SUMMARY and CUSTOMERS, compute net revenue (total_net_price) by region and month for 1998, and month-over-month change.
Create reports/kpi_1998.html: a self-contained page (no external scripts) with a title, three headline numbers, a table, and a two-sentence summary using only numbers from your queries.""")
render_prompt("Prompt A3.2", "Explain a Change", f"""In that data, find the biggest month-over-month move in net revenue for any region. Explain what drove it (which market segment or customers), using only query results. Add it to the bottom of the report.""")
render_expected("An HTML report you can open in a browser, and an explanation with real numbers.")
render_takeaway(
    """From governed tables to a shareable report, with the "why did this move?" explanation backed by real query results rather than guesses.""",
    """Recurring reporting (plan vs actual, occupancy, NOI) eats analyst and engineer time every month. When the models are tested and governed, an agent can draft the report and the commentary, and a person reviews it before it goes out.
That's the "one home for reporting" Joel asked for.""",
)

st.markdown("#### A4. Warehouse right-sizing advice")
render_whats_happening("""CoCo reads your own query history from the last day, works out what your dbt builds cost in time, and recommends a warehouse size. It only advises: it never changes the warehouse.""")
render_prompt("Prompt A4.1", "Review My Builds", f"""Using QUERY_HISTORY from INFORMATION_SCHEMA (last 24 hours, my queries only), summarize the queries my dbt builds ran: count, total elapsed time, slowest 5, and the warehouse used.
Recommend whether a smaller or larger warehouse size would suit this workload and why. Do NOT run ALTER WAREHOUSE.""")
render_expected("A short recommendation, **no warehouse changed**.")
render_takeaway(
    """The agent can reason about cost and performance from Snowflake's own history, and explain a sizing recommendation in plain language.""",
    """This is the optimization half of Joel's 2027 theme. Most savings come from right-sizing and scheduling, not big projects.
For Build Week, capture a "before" number for credits and runtime, so you can show the improvement.""",
)
