import streamlit as st

from components import (
    render_catch_up,
    render_check,
    render_expected,
    render_explanation,
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
st.markdown("#### Step 1: Move the skill into the plugin")
render_guide_ref("Create a Custom Plugin → Move the Skill into the Plugin", "CoCo moves the files, instead of mkdir/mv in a terminal")
render_whats_happening("Same skill, new home. Inside the plugin it gets versioned and shared together with the hook and reviewer you add next.")
render_prompt("Prompt 3.1", "Move the Skill", f"""Move the folder .snowflake/cortex/skills/new-dbt-model into {PLUGIN_DIR}/skills/ so the skill ends up at {PLUGIN_DIR}/skills/new-dbt-model/SKILL.md.
Then delete the now-empty .snowflake folder. Don't change the skill's content. Do not use the cortex CLI or a terminal — move the files directly.""")
render_expected(f"`{PLUGIN_DIR}/skills/new-dbt-model/SKILL.md` exists, and `.snowflake/` is gone.")

# ---------------------------------------------------------------- Step 2
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
st.markdown("#### Step 6: Test the hook (facilitator demo)")
render_guide_ref("Create a Custom Plugin → Test the Hook", "facilitator demo: on most Tricon laptops the hook can't run, so watch the screen")
render_facilitator_demo(
    "show the hook blocking a production deploy",
    """On a typical Tricon Windows laptop the hook can't start, because `bash` isn't on CoCo's PATH. A hook that can't start is only logged, not blocking: it **fails open**.
That's the lesson: **guardrails need testing on the machines that will run them.**""",
    f"""
**Before the session** (2 min): on your Mac, open your own lab folder in CoCo Desktop, complete Module 3 (or paste its *Catch me up* prompt), and run the pre-flight check from the lab repo:
```
facilitator/check_demos.sh ~/Downloads/tricon-coco-lab <your-connection>
```
It must end in **ALL DEMO CHECKS PASSED**. It runs the hook exactly as CoCo Desktop calls it, from the project folder, and needs `bash` and `jq`.

**On screen:**
1. **Settings → Plugins → coco-de-guide**: show the card listing the skill, the **PreToolUse** hook and the agent.
2. Open `{PLUGIN_DIR}/hooks/validate-bash.sh` and read the one `grep` line aloud: *any dbt command with --target prod, --target=prod or -t prod is blocked.*
3. Start a **new chat** and paste the prompt below. It overrides AGENTS.md's "no terminal" rule for this one test; without that, CoCo may simply refuse, and the hook never gets a chance to fire.
4. CoCo tries the `bash` tool, and the hook stops it: **"[Hook] Tool execution blocked: direct production dbt runs are not allowed..."**. CoCo then explains it can't do that and points to CI/CD.
5. Say: *"The agent decided to run it. The hook said no. Prompts are suggestions; hooks are rules."*

**If CoCo refuses on its own instead** (it read AGENTS.md): that's guardrail layer one working. Say so, then show layer two directly in the terminal:
```
echo '{{"tool_input":{{"command":"dbt build --target prod"}}}}' | bash {PLUGIN_DIR}/hooks/validate-bash.sh; echo "exit=$?"
```
You get the block message and `exit=2`, which is the code CoCo treats as *block*.
""",
)
render_prompt("Prompt 3.5", "Try to Deploy to Production (facilitator only)", """This is a test of our production-safety hook. Use the bash tool to run exactly this command, and tell me what happens:
dbt build --target prod""")
render_expected("The facilitator's CoCo is **blocked** before the command runs, with a message that direct production dbt runs aren't allowed and to use CI/CD.")
render_guardrail("Even with clear instructions, agents generate actions on the fly. Hooks are the hard guardrail that holds no matter what the agent decides.")
render_explanation("Two limits of this hook (good discussion points)", """
- **It only blocks what it matches.** It catches `--target prod` and `--target=prod`, and the short flag `-t prod`. Every pattern you forget is a gap, so test guardrails like code.
- **Its path is relative to this project.** `hooks.json` runs `bash .cortex/plugins/coco-de-guide/hooks/validate-bash.sh`, which only resolves inside the lab folder. When a teammate installs the plugin from the Catalog (Module 4), it lives in their user plugin folder, so the script isn't found and the hook fails open. The CoCo docs don't document a plugin-root path variable, so for now **hooks are reliable only for plugins used from the project folder.**
""")
st.caption("The script itself is tested: run directly with bash, it blocks all three prod forms and allows `--target dev`.")

# ---------------------------------------------------------------- Step 7
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
render_catch_up(f"""Catch me up on Module 3: copy everything in solutions/m3_plugin/coco-de-guide/ (including the hidden .cortex-plugin folder) to {PLUGIN_DIR}/, and delete .snowflake/ if it exists. Then tell me to check Settings → Plugins.""")

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
