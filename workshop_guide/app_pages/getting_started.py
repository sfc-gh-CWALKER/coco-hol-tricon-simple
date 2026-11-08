from pathlib import Path

import streamlit as st

from components import (
    KIT_NAME,
    LAB_DB,
    LAB_ROLE,
    MIN_COCO_NOTE,
    DBT_VERSION,
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
**What it is:** dbt (data build tool) is the **T** in ELT. The data is already loaded into Snowflake; dbt **transforms** it.
You write a plain SQL `SELECT`, and dbt turns it into a table in Snowflake, builds tables in the right order, and checks the results with tests.

**Why teams use it instead of loose SQL scripts:** every transformation is a file you can version in Git, review, reuse and test.
dbt works out which table depends on which, so you never have to run scripts in the right order by hand.

**How one run works:**
1. dbt reads your `.sql` files and fills in the `{{ ... }}` bits with real Snowflake table names (this is called *compiling*).
2. It runs that SQL in Snowflake, creating each model as a **table** (this project's setting in `dbt_project.yml`; dbt can also create views).
3. It runs your tests. A test is just a query that looks for bad rows: **no rows back = pass**.

| Word | In plain English | Where to find it in your lab folder |
|---|---|---|
| **Project** | The folder dbt works in, plus its settings | `dbt_project.yml` (name `tricon_coco_lab`, models built as tables) |
| **Source** | The raw tables dbt reads but never changes. Here: Snowflake's free TPC-H sample sales data | `models/_sources.yml` lists them once: customer, orders, lineitem… |
| **Model** | One `.sql` file containing one `SELECT` = one table dbt builds. The file name becomes the table name | `models/customers.sql` → table `CUSTOMERS` (customers joined to their nation and region) |
| **`source()`** | A shortcut that points at a raw table by its short name, so the full name lives in one place and dbt knows the dependency | `customers.sql` uses `{{ source('tpch', 'customer') }}` |
| **Hard-coded name** | Typing the full table name instead. It works, but dbt can't track it, and every file breaks if the source moves | `orders_summary.sql` uses `SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS`. **You fix this in Module 1** |
| **Test** | A rule the data must pass, e.g. *order_key is never empty and never duplicated* | `models/_schema.yml`. Doesn't exist yet; CoCo writes it in Module 2 |
| **Build** | Build every model **and** run every test in one go (`dbt build` = run + test) | The **Build** button on the Project Action Bar at the bottom of CoCo Desktop |
| **Profile** | Which Snowflake account, role and schema to build into | `dbt_projects_profiles.yml` (already points at your schema) |

**The data:** TPC-H, a standard sample of customers, orders, line items and suppliers that ships with every Snowflake account (`SNOWFLAKE_SAMPLE_DATA`). It's read-only and contains no Tricon data.
Your tables land in **your own schema**, so nobody overwrites anyone. For Build Week, swap the source to Tricon tables and the same pattern applies.
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
    upd_text, upd_img = st.columns([3, 2], gap="large")
    with upd_text:
        st.markdown("""
3. **Check for updates, even if you just installed it.** The lab needs the latest version.
   - **macOS:** **Cortex Code** menu (top left) → **Check for Updates…**
   - **Windows:** **Help** → **Check for Updates**
4. If an update is offered, install it and let CoCo Desktop restart.
""")
        st.warning(f"**Don't skip this.** Older versions are missing features the lab uses. You need {MIN_COCO_NOTE.split(' (')[0]}.", icon=":material/system_update:")
    with upd_img:
        st.image(str(Path(__file__).resolve().parent.parent / "static" / "check_for_updates.png"), caption="macOS: Cortex Code → Check for Updates…")

# ---------------------------------------------------------------- Step 2
st.markdown("#### Step 2: Sign in")
with st.container(border=True):
    form_col, img_col = st.columns([3, 2], gap="large")
    with form_col:
        st.markdown("1. In CoCo Desktop, open **Sign in to Snowflake** (add a connection) and fill it in:")
        st.markdown("**Account identifier** (copy this):")
        st.code("BGMSATT-STA98695", language=None)
        st.markdown("**Connection name:** leave the auto-filled value.")
        st.markdown("**Username** (type your own):")
        st.code("<your-email>@triconhomes.com", language=None)
        st.warning("**Add your username.** It's your full Tricon email address, e.g. `jsmith@triconhomes.com`. The form won't connect without it.", icon=":material/person:")
        st.markdown(f"""
2. **Authentication:** choose **SSO**, then sign in with your Tricon account when the browser opens.
3. Click the connection name at the top → **Change Role** → **{LAB_ROLE}**.
""")
    with img_col:
        st.image(str(Path(__file__).resolve().parent.parent / "static" / "sign_in.png"), caption="The Sign in to Snowflake form in CoCo Desktop")
    render_expected(f"The top bar shows your connection with role **{LAB_ROLE}**.")
    render_troubleshoot([
        (f"{LAB_ROLE} isn't in the role list", "Raise your hand. The admin grants it in a minute; don't continue without it."),
        ("Browser didn't open", "Click **Browser didn't open?** and open the link yourself."),
        ("*Account not found*", "Paste the account identifier exactly: `BGMSATT-STA98695`."),
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
with st.container(border=True):
    st.markdown(f"""
Everything for dbt happens in the **Project Action Bar** at the **bottom** of the CoCo Desktop window (boxed in red):
- **Left:** the project, **tricon-coco-lab**
- **Middle (sliders icon):** run options. Open it and set **dbt Version** to **dbt {DBT_VERSION}**
- **Command box:** choose **dbt build**, not *dbt run*. Build creates the tables **and** runs the tests.
- **Right:** the **▶ Run** button and the **Snowflake** icon, which shows dbt runs inside Snowflake

When it finishes, the **Output** panel ends with **`Done. PASS=2 ... ERROR=0`** and **✓ Completed**.
""")
    st.image(str(Path(__file__).resolve().parent.parent / "static" / "coco_action_bar.png"), caption=f"The Project Action Bar at the bottom of CoCo Desktop. Set dbt Version to {DBT_VERSION} in the run options (sliders icon).")
render_build_click("Build")
render_expected(f"The run ends with **success** (no errors) and the Lineage view shows `customers` and `orders_summary`. Two tables now exist in `{LAB_DB}.{attendee_schema()}`.")
render_troubleshoot([
    ("The bar shows a **Python Interpreter** box (local mode)", "Click **Switch to Snowflake-managed** on the bar. You never need local dbt."),
    ("*Workspace ... not allowed* / *blocked by feature policy*", "The account blocks the workspaces that Snowflake-managed dbt uses. Raise your hand; the admin must allow WORKSPACE in personal databases."),
    ("*Schema ... does not exist*", "Step 4 didn't finish. Paste Prompt 0.1 again."),
    ("It's slow (several minutes)", "30 people are building at once on one warehouse. Wait; the first run is the slowest."),
    ("*self signed certificate in certificate chain* when uploading files",
     "The corporate network (Netskope SSL inspection) is re-signing traffic. SQL still works; only the upload is blocked. "
     "Fix: get the Netskope root certificate (`.pem`/`.crt`) from the location the facilitator shares, or export it from "
     "`certmgr.msc` → Trusted Root Certification Authorities → Netskope → Export → Base-64 `.cer`. Then search the Start menu for "
     "**Edit environment variables for your account**, add `NODE_EXTRA_CA_CERTS` = the file's full path, **fully quit CoCo Desktop** "
     "(including the tray icon), reopen it and click Build again. Still stuck? Raise your hand."),
])
st.info("**Tip:** run this Build in the first few minutes. If your network blocks it, you'll find out now, not in Module 2.", icon=":material/bolt:")
render_check(f"""Check my setup: confirm the tables CUSTOMERS and ORDERS_SUMMARY exist in {LAB_DB}.{attendee_schema()} and show their row counts. Answer PASS or FAIL.""")
render_catch_up("""My setup failed and the facilitator is busy. Read START_HERE.md and scripts/setup.sql, tell me in plain language which step failed and the one thing I should do next. Don't change any files.""")
