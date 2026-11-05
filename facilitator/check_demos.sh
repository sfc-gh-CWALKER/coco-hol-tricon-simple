#!/bin/bash
# Facilitator pre-flight for the two "watch, don't do" demos in the simplified Tricon lab.
#   1. Module 3, Step 6: the prod-safety hook blocks `dbt ... --target prod`
#   2. Module 4, Part B: dbt-review run headless, exactly as CI runs it, fails a planted violation
#
# Usage:  facilitator/check_demos.sh <lab-folder> <snowflake-connection> [--with-pass]
#   <lab-folder>  your tricon-coco-lab folder after Module 3 (contains .cortex/plugins/coco-de-guide)
#   --with-pass   also check that a clean copy reviews as OVERALL: PASS (adds about a minute)
#
# Works on a throwaway copy of the folder: never edits your lab folder or touches Snowflake objects.
set -u
LAB="${1:?lab folder}"; CONN="${2:?snowflake connection name}"; WITH_PASS="${3:-}"
PLUGIN=".cortex/plugins/coco-de-guide"
REVIEW_PROMPT="Use the dbt-review agent to review the models in this project. Do not change any files. End your reply with exactly one line: OVERALL: PASS or OVERALL: FAIL"
fails=0
ok()   { echo "  PASS  $1"; }
bad()  { echo "  FAIL  $1"; fails=$((fails + 1)); }

echo "== Prerequisites"
for tool in bash jq cortex; do command -v "$tool" >/dev/null && ok "$tool on PATH" || bad "$tool missing (needed for the demo)"; done
[ -f "$LAB/$PLUGIN/.cortex-plugin/plugin.json" ] && ok "plugin present in $LAB/$PLUGIN" \
  || { bad "no plugin at $LAB/$PLUGIN: finish Module 3 (or paste its Catch me up prompt) first"; exit 1; }

WORK=$(mktemp -d)/lab
cp -R "$LAB" "$WORK"
cd "$WORK" || exit 1

echo "== Demo 1: prod-safety hook (run the way CoCo Desktop calls it, from the project folder)"
HOOK_CMD=$(jq -r '.hooks.PreToolUse[0].hooks[0].command' "$PLUGIN/hooks/hooks.json")
MATCHER=$(jq -r '.hooks.PreToolUse[0].matcher' "$PLUGIN/hooks/hooks.json")
[ "$MATCHER" = "bash" ] && ok "matcher is \"bash\" (lowercase)" || bad "matcher is \"$MATCHER\"; CoCo tool names are lowercase, so it never fires"
hook() {  # $1 = command CoCo is about to run; prints the exit code
  jq -nc --arg c "$1" --arg cwd "$PWD" \
    '{session_id:"preflight",cwd:$cwd,hook_event_name:"PreToolUse",tool_name:"bash",tool_input:{command:$c}}' \
    | sh -c "$HOOK_CMD" >/dev/null 2>/tmp/hook_err.$$
  echo $?
}
for c in "dbt build --target prod" "dbt build --target=prod" "dbt build -t prod"; do
  [ "$(hook "$c")" = 2 ] && ok "blocks: $c" || bad "did NOT block: $c"
done
grep -q "not allowed" /tmp/hook_err.$$ && ok "block message shown to CoCo: $(head -c 70 /tmp/hook_err.$$)..." || bad "no block message on stderr"
for c in "dbt build --target dev" "dbt test --select prod_orders" "ls models"; do
  [ "$(hook "$c")" = 0 ] && ok "allows: $c" || bad "wrongly blocked: $c"
done
rm -f /tmp/hook_err.$$

review() {  # $1 = label; prints the OVERALL verdict
  rm -f review.md target -r 2>/dev/null
  cortex --print "$REVIEW_PROMPT" --plugin-dir "$PLUGIN" --connection "$CONN" -o review.md >/dev/null 2>&1
  grep -Eo "OVERALL: (PASS|FAIL)" review.md 2>/dev/null | tail -1
}

echo "== Demo 2: CI review, headless (same command the GitHub workflow runs; about 1 minute)"
cat > models/bad_orders.sql <<'SQL'
SELECT o_orderkey AS order_key, o_totalprice AS total_price
FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS
SQL
verdict=$(review planted)
[ "$verdict" = "OVERALL: FAIL" ] && ok "planted violation caught: $verdict" || bad "expected OVERALL: FAIL, got '${verdict:-nothing}' (see $WORK/review.md)"
grep -q "bad_orders" review.md 2>/dev/null && ok "review names models/bad_orders.sql" || bad "review doesn't mention bad_orders"
[ -f models/bad_orders.sql ] && grep -q SNOWFLAKE_SAMPLE_DATA models/bad_orders.sql && ok "reviewer changed nothing (read-only)" || bad "reviewer edited files"
cp review.md "$WORK/../review_planted.md"

if [ "$WITH_PASS" = "--with-pass" ]; then
  rm -f models/bad_orders.sql
  verdict=$(review clean)
  [ "$verdict" = "OVERALL: PASS" ] && ok "clean project: $verdict" || bad "clean project expected OVERALL: PASS, got '${verdict:-nothing}'"
fi

echo "== Result"
echo "  Sample CI comment: $WORK/../review_planted.md"
if [ "$fails" = 0 ]; then echo "  ALL DEMO CHECKS PASSED"; else echo "  $fails CHECK(S) FAILED"; fi
exit "$fails"
