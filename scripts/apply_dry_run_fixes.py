"""Fixes from Kim Te's simplified-lab dry run (Nov 5). Run from the repo root."""
from pathlib import Path


def sub(f, a, b):
    p = Path(f)
    s = p.read_text()
    if b in s and a not in s:
        return  # already applied
    if a not in s:
        print("SKIP (already applied or changed):", f, a[:60].replace("\n", " "))
        return
    p.write_text(s.replace(a, b))


C = "workshop_guide/components.py"
M0 = "workshop_guide/app_pages/getting_started.py"
M1 = "workshop_guide/app_pages/m01_agents_md.py"
M2 = "workshop_guide/app_pages/m02_skill.py"
M3 = "workshop_guide/app_pages/m03_plugin.py"
M4 = "workshop_guide/app_pages/m04_share.py"
H = "workshop_guide/app_pages/help.py"
K = "lab_kit"

# ---------------- H1: pin dbt 1.12.3 and restore the guide's arguments: syntax
sub(C, 'GUIDE_URL =', 'DBT_VERSION = "1.12.3"\nGUIDE_URL =')
sub(C, '''At the **bottom** of the CoCo Desktop window: project **tricon_coco_lab**, profile **dev**, operation **{what}** → click it.
dbt runs **inside Snowflake**; nothing runs on your laptop. It takes about a minute, then the **Lineage** view opens.""")''',
    '''At the **bottom** of the CoCo Desktop window: project **tricon_coco_lab**, profile **dev**, operation **{what}**, and in the run options **dbt Version {DBT_VERSION}** → click it.
dbt runs **inside Snowflake**; nothing runs on your laptop. It takes about a minute, then the **Lineage** view opens.""")
        st.caption(f"Always pick dbt **{DBT_VERSION}**. The older 1.9 rejects the guide's test syntax, and 2.0 fails with this lab's profile.")''')
sub(M2, "This project's dbt runs inside Snowflake on dbt 1.9, so put test parameters like values: directly under the test name (no arguments: key).",
    "For parameterized tests like accepted_values, nest all test parameters under an arguments: key.")
sub(M2, "the file lives at models/_schema.yml, and the last line changes: dbt in Snowflake is version 1.9, which doesn't accept the guide's arguments: key",
    "the file lives at models/_schema.yml (no dbt/ folder)")
sub(M2, '''    ("*takes no keyword argument 'arguments'*", "dbt in Snowflake is 1.9 and doesn't accept the `arguments:` key. Ask: *Remove the arguments: wrapper from every test in _schema.yml and put the parameters directly under the test.* Then Build again."),''',
    '''    ("*takes no keyword argument 'arguments'*", "The Build ran on dbt **1.9**. In the Build run options pick **dbt Version 1.12.3** and click Build again. Don't change the file."),
    ("*dbt1159 Deprecated test arguments* or *dbt1308 ... account is empty*", "The Build ran on dbt **2.0**. Pick **dbt Version 1.12.3** and click Build again."),''')
sub(H, "| *takes no keyword argument 'arguments'* | dbt in Snowflake is 1.9: ask CoCo to remove the `arguments:` wrapper from the tests |",
    "| *takes no keyword argument 'arguments'* | The Build ran on dbt 1.9. Pick **dbt Version 1.12.3** in the Build run options |\n"
    "| *dbt1159 Deprecated test arguments* or *dbt1308 ... account is empty* | The Build ran on dbt 2.0. Pick **dbt Version 1.12.3** |")
S = Path(K, "solutions/m2_schema.yml")
s = S.read_text()
if "arguments:" not in s:
    s = s.replace("          - accepted_values:\n              values:",
                  "          - accepted_values:\n              arguments:\n                values:")
    s = s.replace("          - relationships:\n              to: ref('customers')\n              field: customer_key",
                  "          - relationships:\n              arguments:\n                to: ref('customers')\n                field: customer_key")
    assert s.count("arguments:") == 3
    S.write_text(s)

# ---------------- L6 + H1: AGENTS.md heading and pinned version
sub(f"{K}/solutions/m1_AGENTS.md", "# Project: Tricon CoCo Lab", "# Project: tricon_coco_lab")
sub(f"{K}/solutions/m1_AGENTS.md", "- Always use `dbt build`", "- Builds use dbt 1.12.3 (picked in the Build run options)\n- Always use `dbt build`")
sub(M1, '''st.code(f"""# Project: CoCo DE Guide''', '''st.code(f"""# Project: tricon_coco_lab''')

# ---------------- H2/H3 + L2: hook test is a facilitator demo; say why
sub(M3, '''render_guide_ref("Create a Custom Plugin → Test the Hook")
render_whats_happening("You deliberately ask for something dangerous. Type it in the **chat**, not a terminal. The hook should stop CoCo before the command runs.")''',
    '''render_guide_ref("Create a Custom Plugin → Test the Hook", "facilitator demo: on most Tricon laptops the hook can't run, so watch the screen")
render_whats_happening("The facilitator deliberately asks CoCo for something dangerous. The hook should stop CoCo **before** the command runs.")
st.warning(""":material/cast: **Watch the facilitator's screen for this step.** On a typical Tricon Windows laptop the hook can't start: `bash` isn't on CoCo's PATH. A hook that can't start is only logged, not blocking. It **fails open**. And because this lab has no local dbt, a real attempt would just say *dbt is not recognized*, which doesn't look like a guardrail either.
That's the lesson: **guardrails need testing on the machines that will run them.**""")''')
sub(M3, '''render_prompt("Prompt 3.5", "Try to Deploy to Production", "Run dbt build --target prod")''',
    '''render_prompt("Prompt 3.5", "Try to Deploy to Production (facilitator)", "Run dbt build --target prod")''')
sub(M3, '''st.caption("Windows: the hook runs with `bash`. If your laptop doesn't have it, CoCo may report a hook error instead of the block message. Watch the facilitator's screen for this one step.")''',
    '''render_explanation("Two limits of this hook (good discussion points)", """
- **It only blocks what it matches.** It catches `--target prod` and `--target=prod`, and the short flag `-t prod`. Every pattern you forget is a gap, so test guardrails like code.
- **Its path is relative to this project.** `hooks.json` runs `bash .cortex/plugins/coco-de-guide/hooks/validate-bash.sh`, which only resolves inside the lab folder. When a teammate installs the plugin from the Catalog (Module 4), it lives in their user plugin folder, so the script isn't found and the hook fails open. The CoCo docs don't document a plugin-root path variable, so for now **hooks are reliable only for plugins used from the project folder.**
""")
st.caption("Check it yourself on any machine with bash: the hook script blocks when run directly. Try it in Help after the lab.")''')

# ---------------- M2: manifest prompt uses exactly the solution's fields
sub(M3, '''render_prompt("Prompt 3.2", "Create the Manifest", f"""Consult the CoCo Desktop plugin
documentation at https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop/plugins
for the correct plugin.json schema and file structure.

Create a CoCo plugin manifest''', '''render_prompt("Prompt 3.2", "Create the Manifest", f"""Create a CoCo plugin manifest''')
sub(M3, '''- hooks: pointing to ./hooks/hooks.json

Also create''', '''- hooks: pointing to ./hooks/hooks.json
Use exactly these fields, with these values.

Also create''')
sub(M3, '''render_guide_ref("Create a Custom Plugin → Create the Plugin Manifest")
render_whats_happening("`plugin.json` is the plugin's label: its name, version, and where to find its skills, agents and hooks. Asking CoCo to read the docs first means it uses the current format.")''',
    '''render_guide_ref("Create a Custom Plugin → Create the Plugin Manifest", "no 'consult the docs' line: the docs page doesn't list every field, so the prompt gives the exact manifest")
render_whats_happening("`plugin.json` is the plugin's label: its name, version, and where to find its skills, agents and hooks.")''')

# ---------------- M3/M4: dbt-review handles missing results and Build remediation
sub(M3, '''- Read target/run_results.json to see whether the last build and its tests passed
- Verify that each convention from the new-dbt-model skill is met
- Produce a concise PASS/FAIL report per convention with specific remediation steps for any failures
- Never edit files''', '''- Read target/run_results.json to see whether the last build and its tests passed. If the file doesn't exist, report that check as N/A: "no build results yet: click Build", not FAIL
- Verify that each convention from the new-dbt-model skill is met
- Produce a concise PASS/FAIL report per convention with specific remediation steps for any failures
- For build fixes, the remediation is "click Build on the Project Action Bar"; never suggest dbt terminal commands
- Never edit files''')
sub(f"{K}/solutions/m3_plugin/coco-de-guide/agents/dbt-review.md", '''3. Output one Markdown table''', '''   - **Build**: read target/run_results.json. If it doesn't exist, mark this N/A with "no build results yet: click Build" (not FAIL).
3. For any build fix, the remediation is "click Build on the Project Action Bar". Never suggest dbt terminal commands.
4. Output one Markdown table''')
sub(f"{K}/solutions/m3_plugin/coco-de-guide/agents/dbt-review.md", '''4. End with "Overall''', '''5. End with "Overall''')
sub(M3, '''render_expected("A table per model (`customers`, `orders_summary`, `supplier_performance`) ending in an overall **PASS**, or specific fixes for anything that breaks a convention.")''',
    '''render_expected("A table per model (`customers`, `orders_summary`, `supplier_performance`) ending in an overall **PASS**, or specific fixes for anything that breaks a convention. If you haven't built since catching up, the build check shows **N/A: click Build**. Click Build and run the review again.")''')
sub(f"{K}/solutions/m2_skill/SKILL.md", "4. Ask me to run Build on the Project Action Bar, then read `target/run_results.json` and report the result.",
    "4. Ask me to click Build on the Project Action Bar (dbt 1.12.3), then read `target/run_results.json` and report the result. If it's missing, say the build didn't finish and ask me to click Build again.")
sub(M2, '''4. Ask me to click Build on the Project Action Bar, then read target/run_results.json and report the result''',
    '''4. Ask me to click Build on the Project Action Bar, then read target/run_results.json and report the result (if it's missing, ask me to click Build again)''')
sub(M2, '''4. Ask me to click Build on the Project Action Bar, then read `target/run_results.json` and report the result.""", language="markdown")''',
    '''4. Ask me to click Build on the Project Action Bar, then read `target/run_results.json` and report the result.""", language="markdown")''')

# ---------------- M1 (catalog): Tricon-style URI and CoCo version
sub(M4, '''Publishing creates a `CORTEX EXTENSION` object in your **personal database**:
`USER$<YOUR_USERNAME>.SKILL_SHARING.COCO_DE_GUIDE`, with a share link like
`snow://skill_catalog/USER$<YOUR_USERNAME>.SKILL_SHARING.COCO_DE_GUIDE/versions/version$1/`''',
    '''Publishing creates a `CORTEX EXTENSION` object in your **personal database**. At Tricon, usernames are email addresses, so the database name has an `@` in it and needs double quotes:
`"USER$KTE@TRICONHOMES.COM".SKILL_SHARING.COCO_DE_GUIDE` (yours uses your email), with a share link like
`snow://skill_catalog/"USER$KTE@TRICONHOMES.COM".SKILL_SHARING.COCO_DE_GUIDE/versions/version$1/`
Copy the link CoCo gives you exactly, quotes included. Email-style links need **CoCo Desktop 1.21.3 or later**.''')
sub(M4, '''render_expected("CoCo reports a **share URI** starting with `snow://skill_catalog/USER$...SKILL_SHARING.COCO_DE_GUIDE/versions/version$1/`. Copy it somewhere.")''',
    '''render_expected("CoCo reports a **share URI** like `snow://skill_catalog/\\"USER$<you>@TRICONHOMES.COM\\".SKILL_SHARING.COCO_DE_GUIDE/versions/version$1/`. Copy it exactly, quotes included.")''')
sub(M4, '''    ("No Publish button on the card", "Update CoCo Desktop (Help → Check for Updates)."),''',
    '''    ("No Publish button on the card, or the link with `@` in it doesn't import", "Update CoCo Desktop to **1.21.3 or later** (Help → Check for Updates)."),''')
sub(C, 'MIN_COCO_NOTE = "the latest CoCo Desktop (Help → Check for Updates)"',
    'MIN_COCO_NOTE = "CoCo Desktop 1.21.3 or later (Help → Check for Updates)"')

# ---------------- L1: setup reports leftover tables
sub(f"{K}/scripts/setup.sql", "  orders INTEGER;\n", "  orders INTEGER;\n  leftover INTEGER;\n")
sub(f"{K}/scripts/setup.sql", "  SELECT COUNT(*) INTO :orders FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS;\n  RETURN 'READY: DEMO_DB.' || schema_name || ' for ' || me || ' (sample data: ' || orders || ' orders)';",
    "  SELECT COUNT(*) INTO :orders FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS;\n"
    "  SELECT COUNT(*) INTO :leftover FROM DEMO_DB.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = :schema_name;\n"
    "  RETURN 'READY: DEMO_DB.' || schema_name || ' for ' || me || ' (sample data: ' || orders || ' orders; '\n"
    "    || CASE WHEN leftover = 0 THEN 'empty schema, a fresh start' ELSE leftover || ' tables from an earlier run, rebuilt on your next Build' END || ')';")
sub(M0, '''render_expected(f"**READY** and the schema **{LAB_DB}.{attendee_schema()}**.")''',
    '''render_expected(f"**READY** and the schema **{LAB_DB}.{attendee_schema()}**, ending in *empty schema, a fresh start*. Ran the lab before? It says how many tables are left over; the next Build rebuilds them.")''')

# ---------------- L4: Windows nested folder in the main step
sub(M0, '''1. **Unzip** it (Windows: right-click → **Extract All**; macOS: double-click). Put it somewhere simple, like Documents.
2. In CoCo Desktop: **File → Open Folder** → choose the **`{KIT_NAME}`** folder itself (the one that contains `dbt_project.yml`).''',
    '''1. **Unzip** it (Windows: right-click → **Extract All**; macOS: double-click). Put it somewhere simple, like Documents.
2. In CoCo Desktop: **File → Open Folder** → choose the **`{KIT_NAME}`** folder that contains `dbt_project.yml`.
   **Windows:** *Extract All* makes a folder inside a folder (`{KIT_NAME}\\\\{KIT_NAME}`). Open the **inner** one.''')

print("all fixes applied")
