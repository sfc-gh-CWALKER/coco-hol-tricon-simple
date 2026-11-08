import streamlit as st

from components import (
    render_catch_up,
    render_check,
    render_expected,
    render_explanation,
    render_takeaway,
    render_facilitator_demo,
    render_guardrail,
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

PLUGIN_DIR = ".cortex/plugins/coco-de-guide"

render_session_header("Module 3", "Plugin, Hook & Subagent", "25 min", "the coco-de-guide plugin: your skill + a production-safety hook + a dbt-review subagent")

render_split(
    you=["Paste five prompts (Step 6 is a facilitator demo)", "Click **Keep** on each file", "Check the plugin is on in **Settings → Plugins**"],
    coco=["Moves your skill into the plugin", "Writes the manifest, the hook and the reviewer", "Blocks a production command; reviews every model"],
)

render_explanation("What is a Plugin? (read this first)", f"""
Your skill works, but only in this project. To reuse it elsewhere you'd copy it and maintain two versions. And a team needs more than skills: a **guardrail** that stops dangerous commands, and a **reviewer** that checks work. Three loose things, none versioned together.

A **plugin** is one installable unit that bundles them, with a version number:

| Piece | What it is | Today |
|---|---|---|
| **Skill** | Step-by-step recipe, guides an interactive task | `new-dbt-model` |
| **Hook** | A script that runs *before* CoCo uses a tool, and can block it | Block `dbt ... --target prod` |
| **Subagent** | A specialist that runs a whole task on its own and reports back | `dbt-review` |
| **MCP server** | Connects CoCo to outside tools (not covered today) | |

```
{PLUGIN_DIR}/
├── .cortex-plugin/
│   ├── plugin.json      # the manifest: name, version, what's inside
│   └── activation.md    # shown when the plugin is turned on
├── skills/new-dbt-model/SKILL.md
├── agents/dbt-review.md
└── hooks/hooks.json + validate-bash.sh
```
CoCo finds plugins in `.cortex/plugins/` automatically, once the folder is **trusted**.
""")

render_new_chat()

# ---------------------------------------------------------------- Step 1
st.markdown("#### Step 1: Copy the skill into the plugin, then delete the original")
render_guide_ref("Create a Custom Plugin → Move the Skill into the Plugin", "CoCo copies the file and you delete the old folder in the Explorer, instead of mkdir/mv in a terminal")
render_whats_happening("Same skill, new home. Inside the plugin it gets versioned and shared together with the hook and reviewer you add next.")
render_prompt("Prompt 3.1", "Copy the Skill into the Plugin", f"""Copy the skill file .snowflake/cortex/skills/new-dbt-model/SKILL.md to {PLUGIN_DIR}/skills/new-dbt-model/SKILL.md.
Don't change its content. Don't use a terminal or the cortex CLI, and don't try to delete anything: I'll delete the old folder myself. Tell me when the copy is done.""")
st.markdown("""Then **you** remove the old copy, so the skill exists in only one place:
1. In the **Explorer** (left), right-click the **`.snowflake`** folder → **Delete** → confirm.
2. That folder only contains the original `SKILL.md`, which is now inside the plugin.""")
render_whats_happening("""Why don't we ask CoCo to delete it? Its file tools can **create and edit** files but not delete them, and your AGENTS.md tells it not to use a terminal. So CoCo copies, you delete. If CoCo offers to run `rm -rf .snowflake`, say **no** and delete it in the Explorer instead.""")
render_expected(f"`{PLUGIN_DIR}/skills/new-dbt-model/SKILL.md` exists, and the `.snowflake/` folder is gone from the Explorer.")
render_troubleshoot([
    ("CoCo says the original is still there and offers to use the terminal", "Reply *No, I'll delete it myself*, then delete `.snowflake` in the Explorer."),
    ("You can't see `.snowflake` in the Explorer", "It may already be gone. If you're on Windows File Explorer instead, turn on **View → Show → Hidden items**."),
    ("You deleted `.snowflake` before the copy finished", "Run the Module 2 catch-up prompt to restore the skill, then copy it again."),
])

# ---------------------------------------------------------------- Step 2
render_takeaway(
    """The skill moved from your project folder into the plugin folder. It works exactly the same, but now it belongs to a package that can be versioned and shared.""",
    """A skill in one person's project helps one person. Inside a plugin it can be shipped to the whole team, which is the point of the next steps.""",
)

st.markdown("#### Step 2: Create the plugin manifest")
render_guide_ref("Create a Custom Plugin → Create the Plugin Manifest", "no 'consult the docs' line: the docs page doesn't list every field, so the prompt gives the exact manifest")
render_whats_happening("`plugin.json` is the plugin's label: its name, version, and where to find its skills, agents and hooks.")
render_prompt("Prompt 3.2", "Create the Manifest", f"""Create a CoCo plugin manifest for this project at {PLUGIN_DIR}/.cortex-plugin/plugin.json.
The manifest must include all of the following fields:
- name: "coco-de-guide"
- version: 1.0.0
- author: me
- skills: pointing to ./skills
- agents: pointing to ./agents
- hooks: pointing to ./hooks/hooks.json
Use exactly these fields, with these values.

Also create {PLUGIN_DIR}/.cortex-plugin/activation.md that briefly explains
what the plugin includes.

Do not use the cortex CLI — write the files directly.""")
st.code("""{
  "name": "coco-de-guide",
  "description": "dbt/Snowflake data engineering plugin for the CoCo DE Guide",
  "version": "1.0.0",
  "author": { "name": "<YOUR_NAME>" },
  "skills": ["./skills"],
  "agents": ["./agents"],
  "hooks": "./hooks/hooks.json"
}""", language="json")
st.caption("Yours may differ slightly. If CoCo tries `cortex plugin ...` commands, remind it: *Do not use the cortex CLI — write the files directly.*")

# ---------------------------------------------------------------- Step 3
render_takeaway(
    """`plugin.json` is the plugin's label: its name, version and where its skills, hooks and agents live. CoCo reads it to load everything at once.""",
    """Versioning means everyone runs the same standards, and you can roll out a change (v1.1 adds a new rule) the way you'd ship any other code.""",
)

st.markdown("#### Step 3: Add a production safety hook")
render_guide_ref("Create a Custom Plugin → Add a Production Safety Hook")
render_whats_happening("""AI agents will run whatever you ask, including commands that write to **production**. A **PreToolUse hook** is a small script CoCo must run *before* every terminal command.
If the command contains `dbt` and `--target prod`, the script says no, and CoCo can't run it. A hard rule, regardless of what the agent decides.""")
render_prompt("Prompt 3.3", "Create the Hook", f"""Consult the CoCo Desktop hooks documentation at
https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/hooks
for the correct hooks.json schema and shell script format.

Create a PreToolUse hook at {PLUGIN_DIR}/hooks/validate-bash.sh that blocks
any dbt command that includes --target prod. If the command is blocked, return a clear error
message explaining that direct production dbt runs are not allowed and to use the CI/CD
pipeline instead.

Also create {PLUGIN_DIR}/hooks/hooks.json that wires this script to the
PreToolUse event using the matcher value "bash" (lowercase).""")
st.code(f"""{{
  "hooks": {{
    "PreToolUse": [
      {{
        "matcher": "bash",
        "hooks": [
          {{ "type": "command", "command": "bash {PLUGIN_DIR}/hooks/validate-bash.sh", "timeout": 10 }}
        ]
      }}
    ]
  }}
}}""", language="json")

# ---------------------------------------------------------------- Step 4
render_takeaway(
    """A **hook** is a small script that runs *before* CoCo uses a tool. This one checks every terminal command and blocks anything that targets production.""",
    """This is a hard guardrail, not a polite request. Even if a prompt or a teammate asks for a production run, it can't happen from a laptop. Changes go to production through your normal release process, which keeps Security and audit comfortable as you scale AI use.""",
)

st.markdown("#### Step 4: Add a dbt review subagent")
render_guide_ref("Create a Custom Plugin → Add a dbt Review Subagent", "reviews every model and reads the last Build's results, instead of git diff against origin/main and dbt build in a terminal; read-only tools")
render_whats_happening("""A **subagent** runs a whole job by itself and hands back a report, like asking a colleague for a code review. A skill walks *with* you through a task.
This one gets only **read** tools, so it can check but never change anything. In Module 4, the same reviewer runs automatically on every pull request.""")
render_prompt("Prompt 3.4", "Create the dbt-review Subagent", f"""Consult the CoCo Desktop agents documentation at
https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/agents
for the correct agent definition format and frontmatter schema.

Create a dbt-review subagent at {PLUGIN_DIR}/agents/dbt-review.md.
The subagent should:
- Review every dbt model file in models/
- Check target/run_results.json to see whether the last build and its tests passed. It is large, so grep it for "status" and "unique_id" instead of reading it whole. If the file doesn't exist, report that check as N/A: "no build results yet: click Build", not FAIL
- Verify that each convention from the new-dbt-model skill is met
- Produce a concise PASS/FAIL report per convention with specific remediation steps for any failures
- For build fixes, the remediation is "click Build on the Project Action Bar"; never suggest dbt terminal commands
- Never edit files

It should use only the read, grep, and glob tools. Set the model to auto.""")
render_expected(f"`{PLUGIN_DIR}/agents/dbt-review.md` with `name`, `description`, `tools` (read, grep, glob) and `model: auto` at the top.")

# ---------------------------------------------------------------- Step 5
render_takeaway(
    """A **subagent** is a specialist CoCo hands a whole job to. `dbt-review` can only *read* files (no edits, no SQL), checks each model against the conventions and reports PASS or FAIL.""",
    """It's a code reviewer that never gets tired and always applies the same checklist. Your senior engineers review logic, not formatting, and the same reviewer later runs in CI on every pull request (Module 4).""",
)

st.markdown("#### Step 5: Activate the plugin")
render_guide_ref("Create a Custom Plugin → Activate the Plugin")
with st.container(border=True):
    st.markdown("""##### :material/person: You do: check it's on
1. Click the **Settings** gear at the bottom of the left sidebar → **Plugins**.
2. Find **coco-de-guide**. If it's toggled off, turn it on. Not there at all? Click **↻** (refresh).
3. Click the card: it should list the **skill**, the **hook** and the **subagent**.
""")
st.caption("Project plugins only switch on in a **trusted** folder. If it shows but is disabled: Command Palette → *Manage Workspace Trust*, or use the toggle.")

# ---------------------------------------------------------------- Step 6
render_takeaway(
    """Turning the plugin on loads the skill, hook and subagent into CoCo together, for every chat in this project.""",
    """One switch gives a new team member the whole team setup. That's how onshore and offshore engineers start from the same standards on day one.""",
)

st.markdown("#### Step 6: Test the hook (facilitator demo, try it too if you like)")
render_guide_ref("Create a Custom Plugin → Test the Hook", "facilitator demo; attendees can try it too")
st.info(":material/co_present: **The facilitator runs this one on screen.** You're welcome to try it too. Heads-up: in testing on Tricon's environment the hook didn't always start, so it may not block on your laptop. If that happens, try the sample fix below; if it still doesn't work, no problem, just watch the facilitator's demo.")
render_prompt("Prompt 3.5", "Try to Deploy to Production", """This is a test of our production-safety hook. Start a new chat for it.
Use the bash tool to run exactly this command, and tell me what happens:
echo dbt build --target prod
(It's only an echo, so it can't change anything. It's here so the hook sees the text "dbt build --target prod".)""")
render_expected("CoCo is **blocked before the command runs**: *[Hook] Tool execution blocked: direct production dbt runs are not allowed (--target prod). Deploy to production through the CI/CD pipeline instead.*")
render_whats_happening("""The agent decided to run the command; the hook said no. **Prompts are suggestions; hooks are rules.**
We use `echo` so nothing can go wrong even if the hook doesn't fire: the worst case is that a line of text gets printed.""")
render_explanation("It printed the line instead of blocking? Try this sample fix", """
That just means the hook didn't start on your machine. It's a setup difference, not something you did wrong. The usual cause on Windows: the hook runs `bash`, and `bash` isn't on CoCo's PATH.

Paste this into CoCo:
```
My production-safety hook didn't block "echo dbt build --target prod".
Read .cortex/plugins/coco-de-guide/hooks/hooks.json and hooks/validate-bash.sh,
work out why the hook didn't run on this machine (for example bash not on PATH),
and propose the smallest fix. Show me the change before you make it.
Don't install anything.
```
CoCo can usually diagnose it and adjust `hooks.json`, for example by pointing it at Git Bash's full path if Git is installed. If it still doesn't block, leave it there and watch the facilitator's demo; you'll see exactly how it should behave.

**The lesson:** guardrails need testing on the machines that will actually run them.
""")
render_presenter("""**Facilitator (everything up to here is already done on your machine):** open a **new chat** and paste Prompt 3.5. Expect the block message.
Say: *"The agent decided to run it. The hook said no. Prompts are suggestions; hooks are rules."*
If CoCo refuses before trying (it read AGENTS.md), say that's guardrail layer one working, and ask: *"Use the bash tool anyway, it's only an echo."*""")
render_guardrail("Even with clear instructions, agents generate actions on the fly. Hooks are the hard guardrail that holds no matter what the agent decides.")
render_explanation("Two limits of this hook (good discussion points)", """
- **It only blocks what it matches.** It catches `--target prod` and `--target=prod`, and the short flag `-t prod`. Every pattern you forget is a gap, so test guardrails like code.
- **Its path is relative to this project.** `hooks.json` runs `bash .cortex/plugins/coco-de-guide/hooks/validate-bash.sh`, which only resolves inside the lab folder. When a teammate installs the plugin from the Catalog (Module 4), it lives in their user plugin folder, so the script isn't found and the hook fails open. The CoCo docs don't document a plugin-root path variable, so for now **hooks are reliable only for plugins used from the project folder.**
""")
st.caption("The script itself is tested: run directly with bash, it blocks all three prod forms and allows `--target dev`.")

# ---------------------------------------------------------------- Step 7
render_takeaway(
    """The facilitator asked CoCo to run a production deployment, and the hook stopped it before it ran, with a clear reason.""",
    """Guardrails only matter if you've seen them work. This is the evidence to show your security and platform leads: the agent is powerful, but production is protected.""",
)

st.markdown("#### Step 7: Try the subagent")
render_guide_ref("Create a Custom Plugin → Try the Subagent Locally")
render_whats_happening("The reviewer runs to completion by itself: it reads each model, checks the three conventions, reads the last build results, and gives you a PASS/FAIL table.")
render_prompt("Prompt 3.6", "Run the Review", "Use the dbt-review agent to review the models in this project.")
render_expected("A table per model (`customers`, `orders_summary`, `supplier_performance`) ending in an overall **PASS**, or specific fixes for anything that breaks a convention. If you haven't built since catching up, the build check shows **N/A: click Build**. Click Build and run the review again.")

render_troubleshoot([
    ("coco-de-guide isn't in Settings → Plugins", "Click **↻**. Check `" + PLUGIN_DIR + "/.cortex-plugin/plugin.json` exists (note both dots). Then trust the folder."),
    ("Facilitator: the prod command ran anyway", "Check the plugin is **on**, `hooks.json` uses matcher `bash` (lowercase), and CoCo has the **lab folder** open (the hook path is relative). Rerun `facilitator/check_demos.sh`."),
    ("Facilitator: CoCo refused without trying", "AGENTS.md doing its job. Show the hook directly with the terminal command in the runbook."),
    ("CoCo reviews the models itself instead of using the agent", "Ask: *Run this with the dbt-review subagent.*"),
])
render_check(f"""Check Module 3, change nothing: {PLUGIN_DIR} contains .cortex-plugin/plugin.json, skills/new-dbt-model/SKILL.md, hooks/hooks.json, hooks/validate-bash.sh and agents/dbt-review.md; dbt-review's tools are only read, grep and glob. PASS or FAIL for each.""")
render_catch_up(f"""Catch me up on Module 3: copy everything in solutions/m3_plugin/coco-de-guide/ (including the hidden .cortex-plugin folder) to {PLUGIN_DIR}/, Don't delete anything or use a terminal. Then tell me to delete the .snowflake folder in the Explorer if it exists, and to check Settings → Plugins.""")

render_takeaway(
    """The reviewer ran by itself and returned a table per model with PASS, or the exact fixes needed.""",
    """Fast, consistent feedback before anything is merged. For Build Week, run `dbt-review` on your project before you demo it.""",
)

render_what_you_built([
    "coco-de-guide: one versioned plugin with your skill, a hook and a subagent",
    "A hook that blocks direct production dbt runs",
    "dbt-review: a read-only reviewer the team (and CI) can run on any change",
])

render_presenter("""
**Story:** "A skill is a recipe. A plugin is the cookbook, plus a lock on the oven door, plus a taster."

**Beat 1 (Step 6):** the hook is the moment people remember. Do it on screen even if laptops vary.

**Beat 2 (Step 7):** emphasise *same agent, two contexts*: locally now, on every pull request in Module 4.

**What's simplified vs. the guide:** the reviewer checks all models and the last Build's results instead of a git diff, and has no bash tool. The idea is identical.
""")
