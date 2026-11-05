import streamlit as st

st.title("Tricon AI Workshop: CoCo Hands-On Lab")
st.markdown("Use Cortex Code (CoCo) to set team standards, add data quality checks and build reusable automations, **without installing anything but CoCo Desktop**.")

st.space("small")
col1, col2, col3 = st.columns(3)
col1.metric("Modules", "4 + showcase")
col2.metric("You install", "1 app")
col3.metric("Lab time", "~90 min")
st.space("small")

st.markdown("#### How this lab works")
with st.container(border=True):
    st.markdown("""
This is **Jeremiah Hansen's Snowflake guide, [Data Engineering with CoCo](https://www.snowflake.com/en/developers/guides/data-engineering-with-coco/)**, same modules, same order, nearly the same prompts, made simpler to set up:

- **You** sign in, open the lab folder, paste prompts, approve changes, and click **Build**.
- **CoCo** writes the files, checks the data, explains results, and checks its own work.
- **dbt runs inside Snowflake**, so there's no Git, Python, dbt or terminal on your laptop. Windows and Mac follow the same steps.
- Every step shows **which guide section it matches**, a plain-language **What's happening**, a **Check it** prompt and a **Catch me up** prompt.
""")

st.markdown("#### The rule for every automation")
with st.container(border=True):
    st.markdown("""
**Agents propose. People approve. Guardrails hold.**
You work only in your own schema, CoCo shows every change before saving it, a hook blocks production commands, and the review agent can read but never edit.
""")

st.markdown("#### What you'll build")
st.markdown("""
| Module | Guide section | What you build | Time |
|---|---|---|---|
| 0 | Setup · What is Cortex Code? | Sign in, open the folder, first build | 10 min |
| 1 | Create an AGENTS.md | Project context + an audit that fixes the starter code | 15 min |
| 2 | What is a Skill? · Create a Custom Skill | Schema tests, a **new-dbt-model** skill, a model built with it | 25 min |
| 3 | What is a Plugin? · Create a Custom Plugin | **coco-de-guide** plugin: skill + prod-safety **hook** + **dbt-review** subagent | 25 min |
| 4 | Plugin Catalog · CI/CD | Publish to the **Plugins Catalog**; CI/CD as a live demo | 20 min |
| ★ | Optional | Automation showcase: pipeline health, sensitive data, KPI report, warehouse advice | 20 min |

**What's different from the guide:** no fork/clone, PAT or dbt profile (one ZIP instead); you click **Build** instead of typing `dbt build`; the reviewer reads build results instead of a git diff; CI/CD is demonstrated rather than hands-on.
""")
st.info(":material/arrow_back: Start by typing your **initials** in the sidebar, then open **0. Setup**.")
