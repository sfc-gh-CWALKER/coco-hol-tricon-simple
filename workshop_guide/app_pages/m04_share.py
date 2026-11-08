import streamlit as st

from components import (
    ORIGINAL_APP,
    render_expected,
    render_explanation,
    render_takeaway,
    render_facilitator_demo,
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
render_takeaway(
    """Publishing turned your plugin folder into a **Snowflake object** in your personal database, with a share link and versions. It stays private until you grant READ to a role.
Everyone publishes the same plugin name, but each copy lives in its own personal database (`USER$<you>`), so nothing collides or gets overwritten.""",
    """Standards are now distributed like any other governed Snowflake asset: one team owns the plugin, grants it to the data engineering role, and everyone syncs the latest version. No zip files, no "which copy is current?".""",
)

st.markdown("### Part B: Enforce standards automatically in CI/CD (facilitator demo)")
render_guide_ref("Enforce Standards Automatically in CI/CD", "facilitator demo: needs a GitHub repo, a Snowflake token and network access that Tricon laptops and accounts don't have today")
render_facilitator_demo(
    "run dbt-review exactly as CI does",
    "CI needs a GitHub repository, stored secrets and network access for GitHub's servers. None of that is set up for attendees, and it isn't needed to see the idea.",
    """
**Before the session** (about 3 min): from the lab repo, run the pre-flight. It plants a violation in a *copy* of your lab folder and runs the exact CI command against it:
```
facilitator/check_demos.sh ~/Downloads/tricon-coco-lab <your-connection> --with-pass
```
It must end in **ALL DEMO CHECKS PASSED**: planted violation → `OVERALL: FAIL`, clean project → `OVERALL: PASS`. Needs the CoCo CLI (`cortex`) on your Mac.

**On screen, main demo (works anywhere, about 1 minute):**
1. Show the workflow file `facilitator/pr-review.yml`. Point at its one real step, the same subagent from Module 3:
   `cortex --print "Use the dbt-review agent ..." --plugin-dir .cortex/plugins/coco-de-guide`
2. In your lab folder, create `models/bad_orders.sql`, a "teammate's change" that breaks the rule:
   ```
   SELECT o_orderkey AS order_key FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS
   ```
3. In the CoCo Desktop **terminal**, run what CI runs:
   ```
   cortex --print "Use the dbt-review agent to review the models in this project. Do not change any files. End your reply with exactly one line: OVERALL: PASS or OVERALL: FAIL" --plugin-dir .cortex/plugins/coco-de-guide --connection <your-connection> -o review.md
   ```
4. Open `review.md`. It names `bad_orders.sql:2`, gives the `source()` fix and ends **OVERALL: FAIL**. In GitHub this is the PR comment, and the failed check blocks the merge.
5. Delete `models/bad_orders.sql` so your folder is clean again.

Say: *"Same agent, two contexts. Desktop while you work, headless on every pull request. No human has to remember the rules."*

**Optional extra: the real GitHub run.** Only if prepared in advance; it hasn't been run against this lab's layout yet:
- A GitHub repo with your lab folder at the root, plus `.github/workflows/pr-review.yml` copied from `facilitator/pr-review.yml`
- Secrets `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD` (a PAT)
- The demo account's network policy must allow `SNOWFLAKE.NETWORK_SECURITY.GITHUBACTIONS_GLOBAL`. The SE demo account's VPN-only policy blocks GitHub today, so a run fails to connect without this change.
- Open a PR adding `bad_orders.sql`: the review posts as a comment in 1–2 minutes, and the check goes red.
""",
)
render_whats_happening("""**CI/CD** means checks that run by themselves whenever someone proposes a change (a *pull request*).
The guide wires the **same dbt-review subagent** from Module 3 into GitHub Actions: every pull request that touches a model gets a PASS/FAIL review posted as a comment, before a person approves it.""")
with st.container(border=True):
    st.markdown("""
**What the facilitator shows:**
1. **A workflow file**, `pr-review.yml`, that installs the **CoCo CLI**, connects to Snowflake and runs the dbt-review agent headless
2. **A "teammate's change"** that reads the raw table directly, breaking the AGENTS.md rule
3. **The review**: it names the file and line, proposes the `source()` fix, and ends **OVERALL: FAIL**. In GitHub that's the PR comment and a red check.

**Why the CLI here?** Desktop is for interactive work. The CLI runs headless in any CI system and uses the same plugin from `.cortex/plugins/`.
""")
st.markdown(f"Want to do it yourself after the workshop? The [full lab guide]({ORIGINAL_APP}) walks through it, with Git and a local dbt install.")

render_takeaway(
    """The same `dbt-review` subagent ran headless through the **CoCo CLI** in a CI pipeline, caught a teammate's change that broke the rules, and failed the pull request with the exact fix.""",
    """This closes the loop: the standards you wrote in Module 1 are now enforced **automatically on every change**, not just when someone remembers to check.
It's the target end state for Tricon's dbt workflow: AGENTS.md and skills to build right, hooks to stay safe, a reviewer in CI to keep it that way.""",
)

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

**Part B:** run `facilitator/check_demos.sh` that morning. Then follow the runbook above: planted `bad_orders.sql`, then the headless review, then OVERALL: FAIL. The review takes about a minute; talk through `facilitator/pr-review.yml` while it runs.

**Bridge to Build Week:** "Every Build Week idea should end the same way: an agent that proposes, a person who approves, and a guardrail that holds."
""")
