"""
app.py
------
LearnLite — Your Personal AI Learning Assistant

Run with:
    streamlit run app.py
"""

import streamlit as st
from prompts import build_messages, SECTION_HEADINGS
from granite_client import chat_completion

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="LearnLite – AI Learning Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Custom CSS — clean, minimal, educational feel
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Slightly increase base font size for readability */
    html, body, [class*="css"] { font-size: 15px; }

    /* Give the main content area breathing room */
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    /* Style the tab bar */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        padding: 6px 18px;
        border-radius: 6px 6px 0 0;
        font-weight: 500;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Response parser
# Splits the raw Granite reply on the five section headings from prompts.py.
# ---------------------------------------------------------------------------

def parse_response(raw: str) -> dict:
    """
    Walk through the raw text line by line and bucket content under each
    known heading. Falls back gracefully if a section is missing.
    """
    sections = {key: "" for key in SECTION_HEADINGS}
    markers  = {heading.strip(): key for key, heading in SECTION_HEADINGS.items()}

    current_key = None
    buffer: list[str] = []

    for line in raw.splitlines():
        stripped = line.strip()
        if stripped in markers:
            # Flush the previous buffer
            if current_key is not None:
                sections[current_key] = "\n".join(buffer).strip()
            current_key = markers[stripped]
            buffer = []
        else:
            buffer.append(line)

    # Flush the final section
    if current_key is not None:
        sections[current_key] = "\n".join(buffer).strip()

    # If nothing parsed, surface the full response so it isn't silently lost
    if not any(sections.values()):
        sections["explanation"] = raw.strip()

    return sections


# ---------------------------------------------------------------------------
# Session-state helpers
# ---------------------------------------------------------------------------

def clear_state() -> None:
    """Wipe results from session state (bound to the Clear button)."""
    for key in ("result", "raw_response", "last_level"):
        st.session_state.pop(key, None)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("📚 LearnLite")
st.markdown("##### Your Personal AI Learning Assistant")
st.markdown(
    "Turn complex academic content into clear explanations that match your learning level.  \n"
    "Paste any academic text, pick your level, and let **IBM Granite** do the rest."
)
st.divider()

# ---------------------------------------------------------------------------
# Input columns
# ---------------------------------------------------------------------------
col_text, col_controls = st.columns([3, 1], gap="large")

with col_text:
    st.markdown("#### Academic Content")
    academic_text = st.text_area(
        label="Academic Content",
        label_visibility="collapsed",
        placeholder=(
            "Paste your academic text here…\n\n"
            "Example: 'Photosynthesis is the process by which green plants "
            "use sunlight to synthesise nutrients from carbon dioxide and water…'"
        ),
        height=240,
        key="academic_text_input",
    )

with col_controls:
    st.markdown("#### Learning Level")
    level = st.radio(
        label="Learning level",
        label_visibility="collapsed",
        options=["Beginner", "Intermediate", "Advanced", "Expert"],
        index=0,
        key="level_radio",
    )

    st.markdown("---")

    run_button = st.button(
        "✨ Simplify Content",
        type="primary",
        use_container_width=True,
    )
    st.button(
        "🗑️ Clear",
        type="secondary",
        use_container_width=True,
        on_click=clear_state,
    )

    st.markdown("")
    st.caption(
        "Powered by **IBM Granite**  \n"
        "via IBM watsonx.ai"
    )

# ---------------------------------------------------------------------------
# AI generation
# ---------------------------------------------------------------------------
if run_button:
    if not academic_text or not academic_text.strip():
        st.warning("⚠️ Please paste some academic text before clicking **Simplify Content**.")
    else:
        with st.spinner("IBM Granite is analysing your content…"):
            try:
                messages     = build_messages(academic_text.strip(), level)
                raw_response = chat_completion(messages)
                result       = parse_response(raw_response)

                st.session_state["result"]       = result
                st.session_state["raw_response"] = raw_response
                st.session_state["last_level"]   = level

            except EnvironmentError as env_err:
                st.error(f"⚙️ **Configuration error:** {env_err}")
                st.info(
                    "**Local development:** copy `.env.example` to `.env`, fill in "
                    "your IBM watsonx.ai credentials, then restart with "
                    "`streamlit run app.py`.  \n"
                    "**Streamlit Cloud:** add the four keys to your app's "
                    "**Settings → Secrets** panel."
                )
                st.stop()

            except RuntimeError as rt_err:
                st.error(f"🌐 **API error:** {rt_err}")
                st.stop()

            except Exception as exc:
                st.error(f"❌ **Unexpected error:** {exc}")
                st.stop()

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
if "result" in st.session_state:
    result     = st.session_state["result"]
    last_level = st.session_state.get("last_level", level)

    st.divider()
    st.markdown(f"### Results — *{last_level}* level")

    tab_explain, tab_terms, tab_examples, tab_summary, tab_quiz = st.tabs(
        ["💡 Explanation", "📖 Key Terms", "🔗 Examples", "📝 Summary", "❓ Quiz"]
    )

    with tab_explain:
        st.markdown("#### Simplified Explanation")
        content = result.get("explanation", "")
        if content:
            st.markdown(content)
        else:
            st.info("No explanation was returned. Try again or rephrase your input.")

    with tab_terms:
        st.markdown("#### Key Terms")
        content = result.get("key_terms", "")
        if content:
            st.markdown(content)
        else:
            st.info("No key terms were returned.")

    with tab_examples:
        st.markdown("#### Relatable Examples")
        content = result.get("examples", "")
        if content:
            st.markdown(content)
        else:
            st.info("No examples were returned.")

    with tab_summary:
        st.markdown("#### Summary")
        content = result.get("summary", "")
        if content:
            st.markdown(content)
        else:
            st.info("No summary was returned.")

    with tab_quiz:
        st.markdown("#### Quiz Questions")
        content = result.get("quiz", "")
        if content:
            st.markdown(content)
        else:
            st.info("No quiz questions were returned.")

    with st.expander("🔍 Raw AI Response (debug)", expanded=False):
        st.text(st.session_state.get("raw_response", ""))

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.divider()
st.markdown(
    "<p style='text-align:center; color:#888; font-size:0.82rem;'>"
    "LearnLite · Powered by <strong>IBM Granite</strong> via IBM watsonx.ai"
    "</p>",
    unsafe_allow_html=True,
)
