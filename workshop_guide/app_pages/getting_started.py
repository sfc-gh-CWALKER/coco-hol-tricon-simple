import streamlit as st

from components import (
    KIT_NAME,
    LAB_DB,
    LAB_ROLE,
    MIN_COCO_NOTE,
    attendee_schema,
    render_build_click,
    render_catch_up,
    render_check,
    render_expected,
    render_guide_ref,
    render_kit_download,
    render_presenter,
    render_prompt,
    render_split,
    render_troubleshoot,
    setup_complete,
)

st.title("Module 0: Setup (10 minutes)")
st.markdown(f"""
No Git, no dbt install, no Python, no tokens, no terminal. **dbt runs inside Snowflake**, and CoCo does the typing.
Everyone shares one account, so each person builds in their **own schema**, `{LAB_DB}.TPCH_<INITIALS>`.
""")

render_split(
    you=["Install CoCo Desktop", "Sign in with your browser", "Download and open the lab folder", "Click **Build** once"],
    coco=["Creates your schema", "Checks everything is connected", "Tells you **READY** or what to fix"],
)

render_guide_ref("Setup", "the ZIP replaces fork/clone, the PAT and the dbt profile; dbt runs inside Snowflake")

st.markdown("#### What is Cortex Code?")
with st.container(border=True):
    st.markdown("""
**Cortex Code (CoCo)** is Snowflake's AI coding agent. You describe what you want in plain English; it reads your project, writes the code, runs it, and checks the result.
Unlike a generic assistant it knows Snowflake natively: your schemas, your role's permissions and Snowflake best practices. The model and your data stay inside Snowflake's security boundary.

It comes in three forms. Today we use **CoCo Desktop**, because it supports everything we build: skills, plugins, hooks and subagents.

| Form | Best for |
|---|---|
| CoCo in Snowsight | SQL and notebooks in the browser, nothing to install |
| **CoCo Desktop** (today) | Full projects: files, skills, plugins, hooks, subagents |
| CoCo CLI | Terminal and automation, e.g. CI/CD (the facilitator demos it in Module 4) |
""")

with st.expander(":material/school: New to dbt? The 2-minute version", expanded=True):
    st.markdown("""
**dbt** turns SQL `SELECT` statements into tables, in the right order, with tests. That's all you need for today.

| Word | Means | In your lab folder |
|---|---|---|
| **Model** | One `.sql` file = one table dbt builds | `models/customers.sql`, `models/orders_summary.sql` |
| **Source** | Raw data dbt reads from (here: Snowflake's built-in TPC-H sample sales data) | `models/_sources.yml` |
| **`source()`** | How a model points at raw data, instead of typing the full table name | `{{ source('tpch', 'orders') }}` |
| **Test** | A rule the data must pass, e.g. *no duplicate keys* | `models/_schema.yml` (CoCo creates it in Module 2) |
| **Build** | Create every table, then run every test | The **Build** button at the bottom of CoCo Desktop |

**The data:** TPC-H, a standard sample of customers, orders, line items and suppliers that's in every Snowflake account. Your tables land in **your own schema**, so nobody overwrites anyone.
""")

if not setup_complete():
    st.warning("**First, type your initials in the sidebar** (3 letters, e.g. CJW). Your download and every prompt then use them.", icon=":material/arrow_back:")

# ---------------------------------------------------------------- Step 1
st.markdown("#### Step 1: Install CoCo Desktop")
with st.container(border=True):
    st.markdown(f"""
1. [Download CoCo Desktop](https://www.snowflake.com/en/product/snowflake-coco/downloads/). Windows: choose the **User installer** (no admin rights needed).
2. Install it and open it. Already have it? Make sure you're on {MIN_COCO_NOTE}.

That's the only thing you install today.
""")

# ---------------------------------------------------------------- Step 2
st.markdown("#### Step 2: Sign in")
with st.container(border=True):
    st.markdown(f"""
1. In CoCo Desktop, add a Snowflake connection. Your facilitator will put the **account identifier** on screen.
2. Authentication: **Browser / SSO**. Sign in with your Tricon account when the browser opens.
3. Click the connection name at the top → **Change Role** → **{LAB_ROLE}**.
""")
    render_expected(f"The top bar shows your connection with role **{LAB_ROLE}**.")
    render_troubleshoot([
        (f"{LAB_ROLE} isn't in the role list", "Raise your hand. The admin grants it in a minute; don't continue without it."),
        ("Browser didn't open", "Click **Browser didn't open?** and open the link yourself."),
        ("*Account not found*", "Check the account identifier on the facilitator's screen (`orgname-accountname`)."),
    ])

# ---------------------------------------------------------------- Step 3
st.markdown("#### Step 3: Download and open your lab folder")
with st.container(border=True):
    render_kit_download("kit_setup")
    st.markdown(f"""
1. **Unzip** it (Windows: right-click → **Extract All**; macOS: double-click). Put it somewhere simple, like Documents.
2. In CoCo Desktop: **File → Open Folder** → choose the **`{KIT_NAME}`** folder that contains `dbt_project.yml`.
   **Windows:** *Extract All* makes a folder inside a folder (`{KIT_NAME}\\{KIT_NAME}`). Open the **inner** one.
3. Click **Trust** when asked.
""")
    render_expected("The Explorer (left) shows `models/`, `solutions/`, `dbt_project.yml` and `START_HERE.md`, and a **Project Action Bar** appears at the bottom of the window with project **tricon_coco_lab**.")
    render_troubleshoot([
        ("You see a folder *inside* the folder (`tricon-coco-lab/tricon-coco-lab`)", "Open the inner one: it's the one with `dbt_project.yml` directly in it."),
        ("No Project Action Bar at the bottom", "Switch from Agent view to **Editor** view (top left), or **View → Appearance → Project Action Bar**."),
        ("Windows: the files open in Notepad or the path has `.zip` in it", "You opened the ZIP without extracting. Right-click → **Extract All** first."),
    ])

# ---------------------------------------------------------------- Step 4
st.markdown("#### Step 4: Let CoCo set you up")
with st.container(border=True):
    PROMPT_0_1 = f"""Set me up for the lab.
1. Confirm the open folder contains dbt_project.yml at its top level. If it doesn't, stop and tell me to open the {KIT_NAME} folder itself.
2. Run every statement in scripts/setup.sql in Snowflake, exactly as written. Don't change it.
3. Confirm my current role is {LAB_ROLE} and that dbt_projects_profiles.yml uses schema {attendee_schema()}.
4. Don't install anything and don't use a terminal: dbt runs inside Snowflake for this project.
Finish with one line: READY, or NOT READY plus the exact reason."""
    render_prompt("Prompt 0.1", "Set Me Up", PROMPT_0_1)
    render_expected(f"**READY** and the schema **{LAB_DB}.{attendee_schema()}**, ending in *empty schema, a fresh start*. Ran the lab before? It says how many tables are left over; the next Build rebuilds them.")
    render_troubleshoot([
        ("*Another participant already uses these initials*", "Add a letter to your initials in the sidebar (e.g. CJW → CJWA), download the kit again, open the new folder, repeat this step."),
        (f"*Role {LAB_ROLE} ... not authorized*", f"Change role to {LAB_ROLE} (Step 2). If it's missing, raise your hand."),
        ("*SNOWFLAKE_SAMPLE_DATA does not exist*", "The admin needs to share the sample database with your role. Raise your hand."),
        ("CoCo wants to install dbt or run a terminal command", "Reply: *No. This project uses Snowflake-managed dbt; I'll click Build.* Then continue."),
        ("CoCo can't run SQL", f"Open `scripts/setup.sql`, then **Run all** (`CMD/CTRL+Shift+Enter`). Same result."),
    ])

# ---------------------------------------------------------------- Step 5
st.markdown("#### Step 5: Your first dbt build, in Snowflake")
render_build_click("Build")
render_expected(f"The run ends with **success** (no errors) and the Lineage view shows `customers` and `orders_summary`. Two tables now exist in `{LAB_DB}.{attendee_schema()}`.")
render_troubleshoot([
    ("The bar shows a **Python Interpreter** box (local mode)", "Click **Switch to Snowflake-managed** on the bar. You never need local dbt."),
    ("*Workspace ... not allowed* / *blocked by feature policy*", "The account blocks the workspaces that Snowflake-managed dbt uses. Raise your hand; the admin must allow WORKSPACE in personal databases."),
    ("*Schema ... does not exist*", "Step 4 didn't finish. Paste Prompt 0.1 again."),
    ("It's slow (several minutes)", "30 people are building at once on one warehouse. Wait; the first run is the slowest."),
])
render_check(f"""Check my setup: confirm the tables CUSTOMERS and ORDERS_SUMMARY exist in {LAB_DB}.{attendee_schema()} and show their row counts. Answer PASS or FAIL.""")
render_catch_up("""My setup failed and the facilitator is busy. Read START_HERE.md and scripts/setup.sql, tell me in plain language which step failed and the one thing I should do next. Don't change any files.""")
