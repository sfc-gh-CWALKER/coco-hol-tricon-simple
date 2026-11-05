"""Automated smoke test for the simplified Tricon lab. Run from the repo root:

    .venv/bin/python facilitator/smoke_test.py                        # app + kit + demo markings (no Snowflake)
    .venv/bin/python facilitator/smoke_test.py --demos <lab> <conn>    # also runs check_demos.sh (about 3 min)
"""
import io
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "workshop_guide"
sys.path.insert(0, str(APP))

from streamlit.testing.v1 import AppTest  # noqa: E402

import components  # noqa: E402

failures = []


def check(ok, label):
    print(("  PASS  " if ok else "  FAIL  ") + label)
    if not ok:
        failures.append(label)


print("== Pages render (with and without initials)")
pages = ["streamlit_app.py"] + sorted(str(p.relative_to(APP)) for p in (APP / "app_pages").glob("*.py"))
for page in pages:
    for initials in ("", "KT"):
        at = AppTest.from_file(str(APP / page), default_timeout=60)
        at.session_state["initials"] = initials
        at.run()
        check(not at.exception, f"{page} [{initials or 'no initials'}]")

print("== Lab kit ZIP")
names = zipfile.ZipFile(io.BytesIO(components._kit_zip("KT", components._kit_version()))).namelist()
zf = zipfile.ZipFile(io.BytesIO(components._kit_zip("KT", components._kit_version())))
check(all("<INITIALS>" not in zf.read(n).decode() for n in names), "every file personalized")
for required in ("dbt_projects_profiles.yml", ".vscode/settings.json", "scripts/setup.sql",
                 "solutions/m2_skill/SKILL.md", "solutions/m3_plugin/coco-de-guide/.cortex-plugin/plugin.json",
                 "solutions/m3_plugin/coco-de-guide/hooks/hooks.json", "solutions/m3_plugin/coco-de-guide/agents/dbt-review.md"):
    check(f"{components.KIT_NAME}/{required}" in names, f"kit contains {required}")
check(zf.read(f"{components.KIT_NAME}/solutions/m2_schema.yml").decode().count("arguments:") == 3,
      "m2_schema.yml uses the guide's arguments: syntax (needs dbt 1.12.3)")

print("== Facilitator demos are marked 'watch, don't do'")
for page, marker in (("m03_plugin.py", "show the hook blocking"), ("m04_share.py", "run dbt-review exactly as CI does")):
    src = (APP / "app_pages" / page).read_text()
    check("render_facilitator_demo(" in src and marker in src, f"{page}: facilitator runbook present")
check("Prompt 3.5" not in components.SESSION_PROMPTS["3"], "facilitator-only Prompt 3.5 isn't required to complete Module 3")
check(components.DBT_VERSION == "1.12.3", "Build cards pin dbt 1.12.3")

print("== Workflow file")
wf = (ROOT / "facilitator" / "pr-review.yml").read_text()
check("--plugin-dir .cortex/plugins/coco-de-guide" in wf and 'grep -q "OVERALL: PASS"' in wf,
      "pr-review.yml runs dbt-review headless and fails the check unless OVERALL: PASS")
try:
    import yaml
    try:
        steps = yaml.safe_load(wf)["jobs"]["review"]["steps"]
        check(len(steps) == 6, "pr-review.yml is valid YAML with 6 steps")
    except yaml.YAMLError as e:
        check(False, f"pr-review.yml is valid YAML ({str(e).splitlines()[0]})")
except ImportError:
    print("  SKIP  YAML parse (pyyaml not installed)")

if "--demos" in sys.argv:
    lab, conn = sys.argv[sys.argv.index("--demos") + 1: sys.argv.index("--demos") + 3]
    print("== Facilitator demos, live (check_demos.sh)")
    result = subprocess.run([str(ROOT / "facilitator" / "check_demos.sh"), lab, conn, "--with-pass"], capture_output=True, text=True)
    print("\n".join("    " + line for line in result.stdout.splitlines()))
    check(result.returncode == 0, "check_demos.sh: ALL DEMO CHECKS PASSED")

print(f"== {'ALL SMOKE TESTS PASSED' if not failures else str(len(failures)) + ' FAILED: ' + '; '.join(failures)}")
sys.exit(1 if failures else 0)
