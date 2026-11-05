import streamlit as st

st.title("Agenda")
st.markdown("About 2 hours, hands-on, in the same order as Jeremiah Hansen's *Data Engineering with CoCo* guide. The facilitator works through each module on screen while you follow along.")

LAB = [
    ("0", "Setup and What is Cortex Code? Sign in, open the lab folder, first build", "10 min"),
    ("1", "Create an AGENTS.md, then audit and fix the starter code", "15 min"),
    ("2", "Schema tests without a skill, then the new-dbt-model skill", "25 min"),
    ("3", "Plugin: move the skill in, add a prod-safety hook and a dbt-review subagent", "25 min"),
    ("4", "Publish to the Plugins Catalog; CI/CD live demo", "20 min"),
    ("★", "Optional automation showcase, recap and Build Week ideas", "10-20 min"),
]
with st.container(border=True):
    for key, title, dur in LAB:
        c1, c2 = st.columns([1, 8])
        c1.markdown(f"**{key}**")
        c2.markdown(f"{title} :gray-badge[{dur}]")

st.markdown("#### Before the lab")
st.markdown("""
- Install **CoCo Desktop** (Windows: the User installer needs no admin rights).
- Check you can sign in to the lab Snowflake account with your Tricon login.
- That's it: no Git, Python or dbt.
""")
