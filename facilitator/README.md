# Facilitator kit

Two lab steps are **facilitator demos**: attendees watch, they don't do them.

| Step | Why attendees don't do it | What you show |
|---|---|---|
| Module 3, Step 6: test the hook | On Tricon Windows laptops the hook can't start (`bash` isn't on CoCo's PATH), so it fails open | CoCo trying `dbt build --target prod` and the hook blocking it |
| Module 4, Part B: CI/CD | Needs a GitHub repo, secrets, and network access for GitHub's servers | `dbt-review` run headless, exactly as CI runs it, failing a planted violation |

The step-by-step runbooks are in the lab app, inside each step's **Facilitator runbook** expander.

## Before the session (on your demo laptop)

You need a lab folder that has finished Module 3, plus `bash`, `jq` and the CoCo CLI (`cortex`).

```bash
# Both demos, live (about 3 minutes). Works on a copy; never edits your folder.
facilitator/check_demos.sh ~/Downloads/tricon-coco-lab <your-connection> --with-pass

# Everything: app pages, kit ZIP, demo markings, workflow file, and both demos
.venv/bin/python facilitator/smoke_test.py --demos ~/Downloads/tricon-coco-lab <your-connection>
```

Both must end in **ALL ... PASSED**.

## Files

- `check_demos.sh`: runs the hook the way CoCo Desktop calls it (from the project folder, with a PreToolUse payload on stdin), then runs the headless review on a planted violation (`OVERALL: FAIL`) and on a clean copy (`OVERALL: PASS`).
- `smoke_test.py`: the full automated check.
- `pr-review.yml`: GitHub Actions workflow for the optional real CI run. Copy it to `.github/workflows/` in a repo with the lab folder at its root. It needs secrets `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER` and `SNOWFLAKE_PASSWORD` (a PAT), and an account network policy that allows `SNOWFLAKE.NETWORK_SECURITY.GITHUBACTIONS_GLOBAL`. Not yet run on GitHub.
