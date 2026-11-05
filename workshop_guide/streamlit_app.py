import importlib
from pathlib import Path

import streamlit as st

import components

# Streamlit Cloud hot-reloads this file on each push but keeps imported modules cached;
# reload so pages never see an older components.py than this file expects.
importlib.reload(components)

from components import (
    LAB_DB,
    PERSISTED_KEYS,
    attendee_schema,
    is_session_complete,
    raw_initials,
    setup_complete,
)

_DIR = Path(__file__).parent


def _title(key: str, label: str) -> str:
    check = " :green[:material/check_circle:]" if is_session_complete(key) else ""
    return f"{key}. {label}{check}"


def _sync_to_url():
    for k in PERSISTED_KEYS:
        v = st.session_state.get(k)
        if v:
            st.query_params[k] = v
        elif k in st.query_params:
            del st.query_params[k]


# Restore sidebar values after a browser refresh (they're kept in the URL, never anything secret).
for _k in PERSISTED_KEYS:
    if _k not in st.session_state and _k in st.query_params:
        st.session_state[_k] = st.query_params[_k]


st.set_page_config(
    page_title="Tricon CoCo Lab",
    page_icon=":material/engineering:",
    layout="wide",
)

st.logo(
    str(_DIR / "static" / "snowflake_full_logo.png"),
    icon_image=str(_DIR / "static" / "snowflake_logo.png"),
)

with st.sidebar:
    st.markdown("**Your initials**")
    st.caption("The only thing you need to type. It fills in your schema in every script and prompt. Your lab download is made with them. Nothing is saved.")
    st.text_input(
        "Your initials",
        key="initials",
        max_chars=4,
        placeholder="e.g. CJW",
        label_visibility="collapsed",
        help="Use 3 letters: first, middle and last initial (2-4 letters, no digits or spaces). They name your own schema, TPCH_<initials>. If setup says they're taken, add a letter and download the kit again. Press Enter to apply.",
        on_change=_sync_to_url,
    )
    if setup_complete():
        st.success(f"Your schema everywhere: **`{LAB_DB}.{attendee_schema()}`**", icon=":material/check_circle:")
    elif raw_initials():
        st.error("Initials must be 2-4 letters only (no digits, spaces or full names), e.g. CJW.", icon=":material/error:")
    else:
        st.warning("Type your initials (3 letters, e.g. CJW) so every step is ready to copy.", icon=":material/edit:")

page = st.navigation(
    {
        "": [
            st.Page("app_pages/home.py", title="Home", icon=":material/home:"),
            st.Page("app_pages/agenda.py", title="Agenda", icon=":material/calendar_today:"),
        ],
        "Data Engineering with CoCo (Jeremiah Hansen's guide)": [
            st.Page("app_pages/getting_started.py", title=_title("0", "Setup"), icon=":material/rocket_launch:"),
            st.Page("app_pages/m01_agents_md.py", title=_title("1", "AGENTS.md"), icon=":material/description:"),
            st.Page("app_pages/m02_skill.py", title=_title("2", "Tests & Custom Skill"), icon=":material/auto_fix_high:"),
            st.Page("app_pages/m03_plugin.py", title=_title("3", "Plugin, Hook & Subagent"), icon=":material/extension:"),
            st.Page("app_pages/m04_share.py", title=_title("4", "Plugin Catalog & CI/CD"), icon=":material/sync_alt:"),
        ],
        "Optional": [
            st.Page("app_pages/showcase.py", title="Automation Showcase", icon=":material/bolt:"),
        ],
        "Reference": [
            st.Page("app_pages/help.py", title="Help & Troubleshooting", icon=":material/support:"),
        ],
    },
    position="sidebar",
    expanded=True,
)

page.run()
