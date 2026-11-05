import io
import re
import zipfile
from pathlib import Path

import streamlit as st

# Prompt ids per module; a module shows a check in the sidebar once all are done.
SESSION_PROMPTS = {
    "0": ["Prompt 0.1"],
    "1": ["Prompt 1.1", "Prompt 1.2"],
    "2": ["Prompt 2.1", "Prompt 2.2", "Prompt 2.3"],
    "3": ["Prompt 3.1", "Prompt 3.2", "Prompt 3.3", "Prompt 3.4", "Prompt 3.5", "Prompt 3.6"],
    "4": ["Prompt 4.1"],
}

# Shared objects, created once by the workshop admin. Same as the original lab.
LAB_ROLE = "DEMO_ROLE"
LAB_WH = "DEMO_WH"
LAB_DB = "DEMO_DB"
KIT_NAME = "tricon-coco-lab"
ORIGINAL_APP = "https://coco-hol-tricon-de-gejm3sg47ufychnq9jpkqg.streamlit.app/"
GUIDE_URL = "https://www.snowflake.com/en/developers/guides/data-engineering-with-coco/"
MIN_COCO_NOTE = "the latest CoCo Desktop (Help → Check for Updates)"

INITIALS_PLACEHOLDER = "<INITIALS>"
PERSISTED_KEYS = ("initials",)

_KIT_DIR = Path(__file__).resolve().parent.parent / "lab_kit"


def raw_initials() -> str:
    return st.session_state.get("initials", "").strip().upper()


def initials_valid() -> bool:
    """2-4 letters, nothing else (the schema name is built from it)."""
    return bool(re.fullmatch(r"[A-Z]{2,4}", raw_initials()))


def attendee_initials() -> str:
    return raw_initials() if initials_valid() else ""


def setup_complete() -> bool:
    return initials_valid()


def attendee_schema() -> str:
    return f"TPCH_{attendee_initials() or INITIALS_PLACEHOLDER}"


def personalize(text: str) -> str:
    initials = attendee_initials()
    return text.replace(INITIALS_PLACEHOLDER, initials) if initials else text


@st.cache_data(show_spinner=False)
def _kit_zip(initials: str) -> bytes:
    """The lab folder, with this attendee's initials already in every file."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(_KIT_DIR.rglob("*")):
            if path.is_dir() or path.name == ".DS_Store":
                continue
            text = path.read_text(encoding="utf-8").replace(INITIALS_PLACEHOLDER, initials)
            # LF line endings and a top-level folder, so Windows and macOS unzip identically.
            arc = f"{KIT_NAME}/{path.relative_to(_KIT_DIR).as_posix()}"
            zf.writestr(arc, text.replace("\r\n", "\n"))
    return buf.getvalue()


def render_kit_download(key: str = "kit"):
    if not setup_complete():
        st.warning("Type your initials in the sidebar first. The download is made for you, with your initials already filled in.", icon=":material/arrow_back:")
        return
    st.download_button(
        f":material/download: Download {KIT_NAME}.zip (for {attendee_initials()})",
        data=_kit_zip(attendee_initials()),
        file_name=f"{KIT_NAME}-{attendee_initials()}.zip",
        mime="application/zip",
        type="primary",
        key=key,
    )


# ---------------------------------------------------------------- progress

def _done_store() -> dict:
    if "_done" not in st.session_state:
        st.session_state["_done"] = {}
    return st.session_state["_done"]


def _prompt_key(prompt_id: str) -> str:
    return prompt_id.replace(" ", "_").replace(".", "_")


def _on_toggle(prompt_id: str):
    key = _prompt_key(prompt_id)
    _done_store()[key] = st.session_state[f"_cb_{key}"]


def is_session_complete(session_key: str) -> bool:
    prompts = SESSION_PROMPTS.get(session_key, [])
    store = _done_store()
    return len(prompts) > 0 and all(store.get(_prompt_key(p), False) for p in prompts)


# ---------------------------------------------------------------- building blocks

def render_session_header(label: str, title: str, duration: str, outcome: str):
    st.title(f"{label}: {title}")
    col1, col2 = st.columns(2)
    col1.markdown(f":material/schedule: **{duration}**")
    col2.markdown(f":material/flag: **You'll have**: {outcome}")
    st.space("small")


def render_split(you: list[str], coco: list[str]):
    """Who does what in this module. Business users read the left column; CoCo does the right."""
    col1, col2 = st.columns(2)
    with col1.container(border=True):
        st.markdown("##### :material/person: You do")
        for item in you:
            st.markdown(f"- {personalize(item)}")
    with col2.container(border=True):
        st.markdown("##### :material/smart_toy: CoCo does")
        for item in coco:
            st.markdown(f"- {personalize(item)}")


def render_new_chat():
    st.info(":material/add_comment: **Start a new chat** for this module: the **+** at the top of the CoCo chat panel (right side).")


def render_prompt(prompt_id: str, title: str, prompt_text: str):
    key = _prompt_key(prompt_id)
    cb_key = f"_cb_{key}"
    store = _done_store()
    if cb_key not in st.session_state:
        st.session_state[cb_key] = store.get(key, False)
    with st.container(border=True):
        header_col, check_col = st.columns([5, 1])
        with header_col:
            st.markdown(f"#### :material/chat: {prompt_id} - {title}")
        with check_col:
            st.checkbox("Done", key=cb_key, on_change=_on_toggle, args=(prompt_id,))
        st.caption("Copy (icon at the top right of the box), paste into the CoCo chat, press Enter. Approve when CoCo asks.")
        st.code(personalize(prompt_text), language="text", wrap_lines=True)


def render_build_click(what: str = "Build"):
    """The one dbt action people do by hand: dbt runs in Snowflake, started from the Project Action Bar."""
    with st.container(border=True):
        st.markdown(f"""##### :material/play_circle: You click: **{what}** on the Project Action Bar
At the **bottom** of the CoCo Desktop window: project **tricon_coco_lab**, profile **dev**, operation **{what}** → click it.
dbt runs **inside Snowflake**; nothing runs on your laptop. It takes about a minute, then the **Lineage** view opens.""")


def render_expected(text: str):
    st.success(personalize(f":material/check_circle: **You should see:** {text}"))


def render_check(prompt_text: str):
    """Self-check prompt: CoCo verifies the module and answers PASS/FAIL."""
    with st.expander(":material/fact_check: Not sure it worked? Ask CoCo to check"):
        st.code(personalize(prompt_text), language="text", wrap_lines=True)


def render_catch_up(prompt_text: str):
    with st.expander(":material/fast_forward: Behind or stuck? Catch me up"):
        st.caption("Copies the finished answer for this module from the `solutions/` folder, so you can keep going with everyone else.")
        st.code(personalize(prompt_text), language="text", wrap_lines=True)


def render_troubleshoot(rows: list[tuple[str, str]], title: str = "Something different? Fixes"):
    with st.expander(f":material/build: {title}"):
        table = "| If you see | Do this |\n|---|---|\n" + "\n".join(f"| {s} | {f} |" for s, f in rows)
        st.markdown(personalize(table))


def render_explanation(title: str, body: str):
    with st.expander(f":material/school: {title}", expanded=False):
        st.markdown(personalize(body))


def render_guardrail(text: str):
    st.warning(f":material/verified_user: **A person approves.** {text}")


def render_what_you_built(items: list[str]):
    st.markdown("##### :material/check_circle: What you built")
    for item in items:
        st.markdown(f"- :green-badge[Done] {personalize(item)}")


def render_guide_ref(section: str, change: str = ""):
    """Ties a step to the matching section of Jeremiah Hansen's guide, so presenters stay in sync."""
    note = f" · :orange[Simplified: {change}]" if change else " · same as the guide"
    st.caption(f":material/menu_book: Guide: [{section}]({GUIDE_URL}){note}")


def render_whats_happening(text: str):
    """Plain-language explanation for people new to dbt or coding agents."""
    st.info(personalize(f":material/lightbulb: **What's happening:** {text}"))


def render_presenter(notes: str):
    with st.expander(":material/record_voice_over: Presenter notes"):
        st.markdown(personalize(notes))
