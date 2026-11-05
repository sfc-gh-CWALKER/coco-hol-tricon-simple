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
- **You** do a few things by hand: sign in, open the lab folder, paste prompts, approve changes, and click **Build**.
- **CoCo** does the technical work: writes the files, checks the data, explains results, and checks its own work.
- **dbt runs inside Snowflake**, so there's no Git, Python, dbt or terminal on your laptop. Windows and Mac follow the same steps.
- Every module has a **Check it** prompt (CoCo tells you PASS/FAIL) and a **Catch me up** prompt if you fall behind.
""")

st.markdown("#### The rule for every automation")
with st.container(border=True):
    st.markdown("""
**Agents propose. People approve. Nothing touches production.**
You work only in your own schema, CoCo shows every change before saving it, and the review agent in Module 4 can read but never edit.
""")

st.markdown("#### What you'll build")
st.markdown("""
| Module | What | Time |
|---|---|---|
| 0 | Setup: sign in, open the folder, first build | 10 min |
| 1 | **AGENTS.md**: team rules CoCo follows every session | 20 min |
| 2 | **Data quality tests** that run on every build | 15 min |
| 3 | A reusable **skill** for building new models | 20 min |
| 4 | A read-only **review agent** | 15 min |
| ★ | Optional showcase: pipeline health, sensitive-data sweep, HTML KPI report, warehouse advice | 20 min |
""")
st.info(":material/arrow_back: Start by typing your **initials** in the sidebar, then open **0. Setup**.")
