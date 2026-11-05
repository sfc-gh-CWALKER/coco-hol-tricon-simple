import streamlit as st

from components import (
    ORIGINAL_APP,
    render_expected,
    render_explanation,
    render_guide_ref,
    render_presenter,
    render_prompt,
    render_session_header,
    render_split,
    render_troubleshoot,
    render_whats_happening,
    render_what_you_built,
)

render_session_header("Module 4", "Plugin Catalog & CI/CD", "20 min", "your plugin published to Snowflake for the team, and a live demo of dbt-review on every pull request")

render_split(
    you=["Click **Publish to Plugins Catalog**", "Confirm the name and who can see it", "Watch the CI/CD demo"],
    coco=["Creates the plugin object in Snowflake", "Uploads and versions the files", "Hands you a share link for teammates"],
)

# ---------------------------------------------------------------- Part A
st.markdown("### Part A: Publish to the Plugins Catalog (hands-on)")
render_guide_ref("Publish to the Plugin Catalog")
render_explanation("What is the Plugins Catalog?", """
Right now your plugin lives in your lab folder. The **Plugins Catalog** is Snowflake's built-in registry for sharing plugins across the organisation:

- **Governance**: access is controlled by Snowflake roles and grants, not Git permissions
- **Discoverability**: teammates browse and search for plugins inside CoCo Desktop
- **No credentials**: people install straight from Snowflake, no GitHub access needed
- **Versioning**: every publish is a new version; teammates sync to get the latest

Publishing creates a `CORTEX EXTENSION` object in your **personal database**. At Tricon, usernames are email addresses, so the database name has an `@` in it and needs double quotes:
`"USER$KTE@TRICONHOMES.COM".SKILL_SHARING.COCO_DE_GUIDE` (yours uses your email), with a share link like
`snow://skill_catalog/"USER$KTE@TRICONHOMES.COM".SKILL_SHARING.COCO_DE_GUIDE`
Copy the link CoCo gives you exactly, quotes included. Email-style links need **CoCo Desktop 1.21.3 or later**.
""")
render_whats_happening("One button turns your folder into a governed Snowflake object. A chat opens and a built-in skill does the work; you just confirm.")
with st.container(border=True):
    st.markdown("""##### :material/person: You do: publish
1. **Settings** gear (bottom of the left sidebar) → **Plugins**.
2. Click the **coco-de-guide** card → **Publish to Plugins Catalog** (cloud-upload icon).
3. A chat opens and the `share-skill-and-plugin` skill runs. Confirm the **name** and **description**.
4. When it asks who can access it, keep the default for the lab: **only you**. The link alone doesn't give anyone access. A teammate also needs **READ** granted to one of their roles (see below).
""")
render_expected("CoCo reports a **share URI** like `snow://skill_catalog/\"USER$<you>@TRICONHOMES.COM\".SKILL_SHARING.COCO_DE_GUIDE`, and notes that only you can read it so far. Copy the URI exactly, quotes included.")

render_prompt("Prompt 4.1", "How Would a Teammate Install It?", """Show me the share URI of the coco-de-guide plugin I just published and which roles can read it. Explain in three steps how a teammate installs it from the Plugins Catalog, and what I'd need to grant first. Don't change anything.""")
render_whats_happening("""Publishing and **sharing** are separate steps. That's the governance point: like any Snowflake object, the plugin is private until you **grant READ** to a role.
In real life you'd grant it to a team role, e.g. *grant READ to DATA_ENGINEERING*. CoCo can do this for you when you ask. Skip it in the lab, so 30 plugins don't flood everyone's catalog.""")
render_explanation("Installing a catalog plugin (the teammate's side)", """
0. First, the owner grants **READ** on the plugin to one of the teammate's roles (ask CoCo: *grant READ on my coco-de-guide plugin to role X*).
1. **Settings** → **Plugins** → **+** → **Add from Plugins Catalog**, or just paste the URI into the CoCo chat
2. Paste the `snow://skill_catalog/...` URI → **Import**
3. The plugin appears with a **CATALOG** badge. Later versions arrive with **Sync**.
""")
render_troubleshoot([
    ("*Insufficient privileges* / can't create SKILL_SHARING", "Your account may restrict publishing. Skip to Part B; the facilitator shows the publish flow."),
    ("No Publish button on the card, or the link with `@` in it doesn't import", "Update CoCo Desktop to **1.21.3 or later** (Help → Check for Updates)."),
    ("CoCo asks to make it public to everyone", "Say no for the lab. Keep it reachable by link only."),
])

# ---------------------------------------------------------------- Part B
st.markdown("### Part B: Enforce standards automatically in CI/CD (facilitator demo)")
render_guide_ref("Enforce Standards Automatically in CI/CD", "watch, not hands-on: it needs your own GitHub fork and a Snowflake token")
render_whats_happening("""**CI/CD** means checks that run by themselves whenever someone proposes a change (a *pull request*).
The guide wires the **same dbt-review subagent** from Module 3 into GitHub Actions: every pull request that touches a model gets a PASS/FAIL review posted as a comment, before a person approves it.""")
with st.container(border=True):
    st.markdown("""
**What the facilitator shows:**
1. **GitHub secrets**: `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD` (a token) on the repo
2. **A workflow file**, `.github/workflows/pr-review.yml`, written by CoCo from one prompt. It installs the **CoCo CLI**, connects to Snowflake and runs:
   `cortex --print "Use the dbt-review agent to review the changes in this PR"`
3. **A pull request** with a planted violation, and the review comment appearing on it

**Why the CLI here?** Desktop is for interactive work. The CLI runs headless in any CI system, and it finds the same plugin in `.cortex/plugins/` with no install step.
""")
st.markdown(f"Want to do it yourself after the workshop? The [full lab guide]({ORIGINAL_APP}) walks through it, with Git and a local dbt install.")

render_what_you_built([
    "coco-de-guide published to Snowflake's Plugins Catalog, with a share link for teammates",
    "Seen: the same dbt-review subagent enforcing standards on every pull request",
])

render_explanation("The whole journey, in one table", """
| Module | You built | Why it matters |
|---|---|---|
| 1 | AGENTS.md | Every chat starts grounded in your project's facts |
| 2 | Tests + new-dbt-model skill | Your team's conventions applied without reminding |
| 3 | Plugin: skill + hook + subagent | Packaged, versioned, with a hard production guardrail |
| 4 | Catalog + CI/CD | Shared with governance; standards enforced on every change |
""")

render_presenter("""
**Close with Jeremiah's line:** "Anyone can get an AI agent to produce a result. Professionals ensure the right result, every time." Then walk the table above.

**Part B demo checklist:** have your fork open, the secrets set, and a branch with a planted violation (e.g. a model using `SNOWFLAKE_SAMPLE_DATA` directly) ready to open as a PR. The review takes 2–4 minutes; talk through the workflow file while it runs.

**Bridge to Build Week:** "Every Build Week idea should end the same way: an agent that proposes, a person who approves, and a guardrail that holds."
""")
