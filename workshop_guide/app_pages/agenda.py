import streamlit as st

st.title("Agenda")
st.markdown("About 90 minutes, hands-on. The facilitator works through each module on screen while you follow along.")

LAB = [
    ("0", "Setup: install CoCo Desktop, sign in, open the lab folder, first build", "10 min"),
    ("1", "Team rules: AGENTS.md, and an audit of the starter code", "20 min"),
    ("2", "Data quality tests that run on every build", "15 min"),
    ("3", "A reusable skill for new dbt models", "20 min"),
    ("4", "A read-only review agent, plus a demo of plugins and CI", "15 min"),
    ("★", "Optional automation showcase, then a recap and Build Week ideas", "10-20 min"),
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
