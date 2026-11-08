import streamlit as st

from components import (
    LAB_DB,
    attendee_schema,
    render_build_click,
    render_catch_up,
    render_check,
    render_expected,
    render_explanation,
    render_takeaway,
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

render_session_header("Module 2", "Tests & a Custom Skill", "25 min", "schema tests, a new-dbt-model skill, and a supplier_performance model built with it")

render_split(
    you=["Paste three prompts", "Review and **Keep** each file", "Click **Build** twice"],
    coco=["Writes data tests from what it already knows", "Writes your team's skill", "Follows the skill to build a new model, tests included"],
)

render_explanation("What is a Skill? (read this first)", """
**AGENTS.md** says *what* the project is. A **Skill** says *how* your team does a recurring task, step by step, the same way every time.

A skill is a folder with one required file, `SKILL.md`, in two parts:
1. **Front matter**: a `name` and a `description`. CoCo reads the description to decide *when* to use the skill on its own, so write it as a clear trigger.
2. **Body**: the conventions and steps to follow.

```
---
name: my-skill
description: Brief description of when this skill should be used.
---
# Instructions
Your workflow steps and conventions go here.
```

**Jeremiah's key insight:** skills encode what the model **can't** infer. CoCo already knows dbt and SQL. What it can't know are *your team's choices*: naming, testing standards, the steps in your order.
**Rule of thumb:** if you start a prompt with *"remember, we always..."*, that's a skill waiting to be written.

CoCo also ships **bundled skills** maintained by Snowflake (Dynamic Tables, Iceberg, dbt on Snowflake and more). Today you write a **custom** one.
""")

render_new_chat()

# ---------------------------------------------------------------- Step 1
st.markdown("#### Step 1: Add schema tests, without any skill")
render_guide_ref("Using CoCo Without a Skill → Add Schema Tests Without Any Skill", "the file lives at models/_schema.yml (no dbt/ folder)")
render_whats_happening("""Tests are rules the data must pass every time it builds, for example *every order key is unique* or *no customer is missing*.
You're not telling CoCo which columns are keys or how dbt tests work. This step shows how much it **already knows** before you write any skill.""")

PROMPT_2_1 = """Add schema tests to the existing models in this project.
Save the results in models/_schema.yml.
At a minimum, each model's primary key should have not_null and unique tests.
Add any other tests that make sense given the columns in each model.
For parameterized tests like accepted_values, nest all test parameters under an arguments: key."""
render_prompt("Prompt 2.1", "Add Schema Tests (No Skill)", PROMPT_2_1)
render_expected("A new `models/_schema.yml` with `not_null` and `unique` on `customer_key` and `order_key`, plus a few more tests. Click **Keep**.")
render_build_click("Build")
render_expected("**Success**, with every test passing (about 20, depending on what CoCo chose: for example 22 = 2 models + 20 tests).")

render_troubleshoot([
    ("A test on `order_status` fails", "TPC-H order statuses are **F, O, P**. Ask: *Fix the accepted_values for order_status to match the data.* The guide notes this: not every column that looks like a rule actually holds in TPC-H."),
    ("*takes no keyword argument 'arguments'*", "The Build ran on dbt **1.9**. Set **dbt Version 1.12.3** in the Build run options and click Build again. Don't change the file."),
    ("*dbt1308 ... account is empty* or *dbt1159*", "The Build ran on dbt **2.0**. Set **dbt Version 1.12.3** and click Build again."),
    ("Build says 0 tests", "The file must be `models/_schema.yml`. Ask CoCo to move it there, then Build again."),
])

render_takeaway(
    """Without being told the keys or how dbt tests work, CoCo wrote `models/_schema.yml` with around **20 tests**, for example:
- **not_null** and **unique** on the primary keys (`customer_key`, `order_key`)
- **accepted_values** on columns with a fixed list (market segment, region, order status, order priority)
- **relationships**: every `orders_summary.customer_key` must exist in `customers`

The exact number varies by run, because CoCo chooses the tests itself.

CoCo added a full set of tests without being told the primary keys, how `_schema.yml` is laid out, or which test types exist. It already knew.

But notice we had to name the file `_schema.yml` ourselves; left alone, CoCo picks `schema.yml`. Both are valid dbt; your team uses the underscore.
That's the point: **the model knows the tool, not your team's choices.** It doesn't know you always use `dbt build`, require primary-key tests, or route raw tables through `_sources.yml`. Without being told, it handles those inconsistently between sessions. That's what a skill fixes.""",
    """Tests are what make a table **certified**: bad data fails the build instead of reaching a report. With TPC-H it's sample data; at Tricon the same tests would protect occupancy, rent roll and NOI.
But notice that CoCo chose *its* tests. Your team's rules (primary-key tests are mandatory, always `dbt build`) need to be written down, which is the next step.""",
)


# ---------------------------------------------------------------- Step 2
st.markdown("#### Step 2: Write the custom skill")
render_guide_ref("Create a Custom Skill → Write the SKILL.md", "step 4 of the workflow asks you to click Build instead of running dbt in a terminal")
render_whats_happening("You're writing down your team's three conventions and four steps once. CoCo finds skills in the project's `.snowflake/cortex/skills/` folder automatically. There's no install or registration.")

PROMPT_2_2 = """Create a custom skill at .snowflake/cortex/skills/new-dbt-model/SKILL.md for creating
new dbt models in this project.

The skill should have exactly two sections:

# Conventions — a numbered list of these three rules:
1. Always use `dbt build` (not `dbt run`) so tests run together with compilation
2. Every model's primary key must have not_null and unique tests in _schema.yml
3. All raw tables must be referenced through _sources.yml using source() — never reference the source database directly in model SQL

# Workflow — a numbered list of these four steps:
1. Confirm which source table(s) to model — ask if not specified
2. Write the model SQL using source() references
3. Add the model entry to _schema.yml with a description and primary key tests
4. Ask me to click Build on the Project Action Bar, then read target/run_results.json and report the result (if it's missing, ask me to click Build again)

Use the name new-dbt-model. Write a one-sentence description that tells CoCo when
to invoke this skill. Keep the skill concise — no sub-steps, no examples, no error
handling instructions. The model is smart enough to infer the details."""
render_prompt("Prompt 2.2", "Create the new-dbt-model Skill", PROMPT_2_2)
st.markdown("Review it and click **Keep**. It should look something like this:")
st.code("""---
name: new-dbt-model
description: Create a new dbt model in this project. Use when adding a model for a new source table or analytical use case.
---

# Conventions
1. Always use `dbt build` (not `dbt run`) so tests run together with compilation.
2. Every model's primary key must have `not_null` and `unique` tests in `_schema.yml`.
3. Reference all raw tables through `_sources.yml`. Never reference the source database directly in model SQL.

# Workflow
1. Confirm which source table(s) to model — ask if not specified.
2. Write the model SQL in `models/<model_name>.sql` using `{{ source('<source>', '<table>') }}` references.
3. Add the model entry to `models/_schema.yml` with a description and tests for the primary key.
4. Ask me to click Build on the Project Action Bar, then read `target/run_results.json` and report the result.""", language="markdown")
render_expected("A new `.snowflake/cortex/skills/new-dbt-model/SKILL.md`. Type `/` in the chat box: **new-dbt-model** appears in the list.")

# ---------------------------------------------------------------- Step 3
render_takeaway(
    """A **skill** is a short Markdown file with your team's conventions and steps for one kind of task, here *building a new dbt model*. CoCo loads it automatically when a request matches its description.""",
    """This is how a standard stops being a wiki page nobody reads. Write it once, and every engineer and every CoCo session follows it the same way.
For Build Week, any task your team repeats (new model, new source, onboarding a Yardi table) is a good candidate for a skill.""",
)

st.markdown("#### Step 3: Invoke the skill to build a new model")
render_guide_ref("Create a Custom Skill → Invoke the Skill to Build a New Model")
render_whats_happening("""Now the payoff. You only describe the business ask: *a summary per supplier*. You don't repeat any rule.
CoCo matches your request to the skill's description, then follows its steps in order: pick the source tables, write the SQL with `source()`, add tests, ask you to build.""")

PROMPT_2_3 = """Use the new-dbt-model skill to create a supplier_performance model.
It should summarize performance metrics per supplier from the supplier and lineitem source tables.
Include total orders, total revenue, and average discount."""
render_prompt("Prompt 2.3", "Build a Model with the Skill", PROMPT_2_3)
st.markdown("Click **Keep** on each new or changed file. When CoCo asks:")
render_build_click("Build")
render_expected(f"Without being reminded, CoCo used `source()`, added `supplier_performance` to `_schema.yml` with primary-key tests, and reported a passing build. **{LAB_DB}.{attendee_schema()}.SUPPLIER_PERFORMANCE** now exists.")

render_troubleshoot([
    ("`/` doesn't list new-dbt-model", "The path must be exactly `.snowflake/cortex/skills/new-dbt-model/SKILL.md`. Then **File → Open Recent** → reopen the folder and start a new chat."),
    ("CoCo writes `SNOWFLAKE_SAMPLE_DATA` in the new model", "Ask: *Follow the new-dbt-model skill's conventions.*"),
    ("The build fails on supplier_performance", "Ask: *Read target/run_results.json, explain the error, and propose a fix.*"),
])
render_check("""Check Module 2, change nothing: models/_schema.yml has not_null and unique on every model's primary key; .snowflake/cortex/skills/new-dbt-model/SKILL.md exists; models/supplier_performance.sql uses source() only; the last build in target/run_results.json passed. PASS or FAIL for each.""")
render_catch_up("""Catch me up on Module 2: copy solutions/m2_schema.yml to models/_schema.yml and solutions/m2_skill/SKILL.md to .snowflake/cortex/skills/new-dbt-model/SKILL.md. Then run Prompt 2.3 using that skill.""")

render_takeaway(
    """You only described the business ask, *a summary per supplier*. CoCo matched it to the skill and followed every rule without being reminded: `source()`, primary-key tests in `_schema.yml`, `dbt build`.""",
    """Consistency at speed: a new model arrives already tested and already following the conventions, whoever (or whatever) wrote it. Reviewers spend their time on the business logic, not on style fixes.""",
)

render_explanation("Tip from the guide", """
Resist the urge to put too much into one skill. A focused skill for *"create a new dbt model"* is more useful than a sprawling one for *"do everything dbt"*.
Keep skills under ~500 lines, write the description as a clear trigger, and test by checking CoCo follows every convention without extra prompting.
""")

render_what_you_built([
    "models/_schema.yml: tests on every model, written from CoCo's own knowledge",
    "new-dbt-model: your team's conventions as a reusable skill",
    "supplier_performance: built to the standard just by asking for it",
])

render_presenter("""
**The story in one line:** "CoCo knows dbt. It doesn't know *your* rules. A skill teaches it your rules once."

**Beat 1 (Step 1):** point at the `_schema.yml` filename. We had to say it. That's the gap a skill closes.

**Beat 2 (Step 3):** read Prompt 2.3 aloud and show it contains **no** rules, then show the result follows all three.

**If someone asks why `dbt build` and not `dbt run`:** build runs the tests too, so bad data fails the build instead of reaching a report.
""")
