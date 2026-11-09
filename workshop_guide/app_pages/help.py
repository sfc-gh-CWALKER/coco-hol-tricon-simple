import streamlit as st

from components import DBT_VERSION, KIT_NAME, LAB_DB, LAB_ROLE, LAB_WH, attendee_schema, render_kit_download

st.title("Help & Troubleshooting")
st.markdown("Find your symptom below. Still stuck? Paste the module's **Catch me up** prompt, or raise your hand.")

st.markdown("#### Quick health check (paste into CoCo any time)")
st.code(f"""Health check, change nothing: (1) does the open folder have dbt_project.yml at its top level? (2) is my role {LAB_ROLE}? (3) does schema {LAB_DB}.{attendee_schema()} exist, and which tables are in it? (4) did the last build in target/run_results.json succeed? One line per item, PASS or FAIL.""", language="text", wrap_lines=True)

st.markdown("#### Setup and sign-in")
st.markdown(f"""
| If you see | Do this |
|---|---|
| {LAB_ROLE} isn't in the role list | Raise your hand: the admin grants it to your user |
| *Account not found* | Use the account identifier on the facilitator's screen (`orgname-accountname`) |
| *Another participant already uses these initials* | Add a letter in the sidebar, download the kit again, open the new folder |
| No Project Action Bar at the bottom | Switch to **Editor** view, or **View → Appearance → Project Action Bar** |
| The bar shows **Python Interpreter** | Click **Switch to Snowflake-managed** |
| *... feature policy ...* / workspace blocked | The account blocks Snowflake-managed dbt. Raise your hand (admin fix) |
""")

st.markdown("#### dbt builds")
st.markdown(f"""
| If you see | Do this |
|---|---|
| *Schema ... does not exist* | Paste Prompt 0.1 (Setup) again |
| *SNOWFLAKE_SAMPLE_DATA ... does not exist* | Admin needs to share the sample database with {LAB_ROLE}. Raise your hand |
| Tables appear in someone else's schema | Your `dbt_projects_profiles.yml` doesn't say `{attendee_schema()}`. Download your kit again |
| Build queued for minutes | 30 people share {LAB_WH}. Wait, or the facilitator sizes it up |
| *takes no keyword argument 'arguments'* | The Build ran on dbt 1.9. Pick **dbt Version 1.12.3** in the Build run options |
| *dbt1159 Deprecated test arguments* or *dbt1308 ... account is empty* | The Build ran on dbt 2.0. Pick **dbt Version 1.12.3** |
| A test fails on `order_status` | TPC-H statuses are **F, O, P**; ask CoCo to fix the test to match the data |
| CoCo says it can't see the results | Wait for the build to finish (results sync back), then say *built* again |
""")

st.markdown("#### CoCo")
st.markdown("""
| If you see | Do this |
|---|---|
| CoCo wants to install dbt, Python or run a terminal | Say: *No installs. This project's dbt runs in Snowflake; I'll click Build.* |
| CoCo runs `cortex ...` or `git` commands | Say: *Don't use the cortex CLI or git; write the files directly.* |
| A skill or agent doesn't show up | Reopen the folder (**File → Open Recent**), then start a new chat |
| The plugin isn't in **Settings → Plugins** | Click **↻**. The folder must be **trusted** (Command Palette → *Manage Workspace Trust*), and `.cortex/plugins/coco-de-guide/.cortex-plugin/plugin.json` must exist |
| The hook didn't block `--target prod` | The plugin must be **on**; on Windows the hook needs `bash`. Watch the facilitator's demo |
| *Publish to Plugins Catalog* fails on privileges | Your account restricts publishing. The facilitator demos it |
| CoCo seems confused | Start a **new chat** (**+** at the top of the chat panel) |
| You want the reference answer | Everything is in the `solutions/` folder |
""")

st.markdown("#### Start over")
with st.container(border=True):
    st.markdown(f"Download a fresh kit, unzip it to a **new** location, and open that folder. Your tables in `{LAB_DB}.{attendee_schema()}` are reused; the next Build overwrites them.")
    render_kit_download("kit_help")

st.markdown("#### Facilitator checklist (before the session)")
with st.container(border=True):
    st.markdown(f"""
- [ ] **Do one real Build click on a Tricon-managed laptop, on the corporate network.** Corporate TLS inspection (Netskope) breaks file uploads. Surya has sent every participant the Netskope `.pem` and manual steps (set `NODE_EXTRA_CA_CERTS`, then fully restart CoCo Desktop). Confirm at least one person has it working before the session, and keep a copy of the `.pem` handy for anyone who lost the email.
- [ ] Check the Build run options are set to **dbt Version {DBT_VERSION}**.
- [ ] Everyone is on **CoCo Desktop 1.21.3 or later** (needed for email-style personal database links in Module 4).
- [ ] Size **{LAB_WH}** up for the session: about 30 people × 5 builds.
- [ ] **Run `facilitator/check_demos.sh <your lab folder> <connection> --with-pass`** from the lab repo on your demo laptop. It must print *ALL DEMO CHECKS PASSED*. It covers both "watch, don't do" demos: the hook (Module 3, Step 6) and the headless CI review (Module 4, Part B). Needs `bash`, `jq` and the CoCo CLI.
- [ ] Remove or disable old copies of **coco-de-guide** and **new-dbt-model** on your demo machine, or `/` shows duplicates.
- [ ] **Open this lab site 10 minutes early.** Streamlit Community Cloud apps sleep when idle.
- [ ] Optional, only if you'll show a real GitHub run: a repo with `facilitator/pr-review.yml`, the three secrets, and the account network policy allowing GitHub Actions (the SE demo account's VPN policy blocks it today).
""")
