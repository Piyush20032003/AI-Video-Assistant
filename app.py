import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import extract_meeting_insights
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

# ---------------------------------------------------------------- page setup
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .block-container {padding-top: 2rem; max-width: 1100px;}
        .hero {
            padding: 1.4rem 1.6rem; border-radius: 16px; margin-bottom: 1.2rem;
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
        }
        .hero h1 {margin: 0; font-size: 1.9rem; color: white;}
        .hero p {margin: .3rem 0 0 0; opacity: .9;}
        div[data-testid="stMetric"] {
            border: 1px solid rgba(128,128,128,.25);
            padding: .6rem .9rem; border-radius: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------ session state
defaults = {"result": None, "messages": [], "source_label": ""}
for key, val in defaults.items():
    st.session_state.setdefault(key, val)


# ----------------------------------------------------------------- pipeline
def run_pipeline(source: str, status) -> dict:
    status.update(label="Downloading / preparing audio...")
    chunks = process_input(source)

    status.update(label="Transcribing audio...")
    transcript = transcribe_all(chunks=chunks)

    status.update(label="Generating title...")
    title = generate_title(transcript)

    status.update(label="Summarizing...")
    summary = summarize(transcript)

    status.update(label="Extracting action items...")
    action_items = extract_meeting_insights(transcript)

    status.update(label="Building chat index (RAG)...")
    rag_chain = build_rag_chain(transcript)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "rag_chain": rag_chain,
    }


def render_value(value):
    """Render str / list / dict returned by the LLM nicely."""
    if value is None or value == "":
        st.info("Nothing found.")
    elif isinstance(value, str):
        st.markdown(value)
    elif isinstance(value, (list, tuple)):
        for item in value:
            if isinstance(item, dict):
                st.json(item)
            else:
                st.markdown(f"- {item}")
    elif isinstance(value, dict):
        st.json(value)
    else:
        st.write(value)


def to_text(value) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        return "\n".join(f"- {v}" for v in value)
    return str(value)


# ------------------------------------------------------------------ sidebar
with st.sidebar:
    st.header("📥 Input")
    mode = st.radio("Source type", ["YouTube URL", "Upload file"], horizontal=True)

    source = None
    if mode == "YouTube URL":
        url = st.text_input("YouTube URL", placeholder="https://youtube.com/watch?v=...")
        source = url.strip() or None
        st.session_state.source_label = source or ""
    else:
        uploaded = st.file_uploader(
            "Audio / video file",
            type=["mp3", "wav", "m4a", "mp4", "mkv", "mov", "webm", "ogg"],
        )
        if uploaded is not None:
            suffix = os.path.splitext(uploaded.name)[1]
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp.write(uploaded.getbuffer())
            tmp.close()
            source = tmp.name
            st.session_state.source_label = uploaded.name

    analyze = st.button(
        "🚀 Analyze", type="primary", use_container_width=True, disabled=source is None
    )

    if st.session_state.result and st.button("🗑️ Reset", use_container_width=True):
        st.session_state.result = None
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Transcribe → Summarize → Extract action items → Chat with your video.")

# --------------------------------------------------------------------- hero
st.markdown(
    """
    <div class="hero">
        <h1>🎬 AI Video Assistant</h1>
        <p>Turn any meeting or video into a transcript, summary, action items, and a chat you can query.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- run
if analyze and source:
    st.session_state.messages = []
    with st.status("Starting...", expanded=True) as status:
        try:
            st.session_state.result = run_pipeline(source, status)
            status.update(label="Done!", state="complete", expanded=False)
        except Exception as e:
            st.session_state.result = None
            status.update(label="Failed", state="error")
            st.error(f"Something went wrong: {e}")

# ---------------------------------------------------------------- results
result = st.session_state.result

if result is None:
    st.info("👈 Paste a YouTube URL or upload a file in the sidebar, then click **Analyze**.")
else:
    st.subheader(result["title"])
    if st.session_state.source_label:
        st.caption(f"Source: {st.session_state.source_label}")

    transcript = result["transcript"]
    c1, c2, c3 = st.columns(3)
    c1.metric("Transcript words", f"{len(transcript.split()):,}")
    c2.metric("Characters", f"{len(transcript):,}")
    c3.metric("Est. read time", f"{max(1, len(transcript.split()) // 200)} min")

    tab_sum, tab_act, tab_chat, tab_tr = st.tabs(
        ["📝 Summary", "✅ Action Items", "💬 Chat", "📄 Transcript"]
    )

    with tab_sum:
        with st.container(border=True):
            render_value(result["summary"])
        st.download_button(
            "⬇️ Download summary", to_text(result["summary"]), file_name="summary.txt"
        )

    with tab_act:
        with st.container(border=True):
            render_value(result["action_items"])
        st.download_button(
            "⬇️ Download action items",
            to_text(result["action_items"]),
            file_name="action_items.txt",
        )

    with tab_chat:
        st.caption("Ask anything about the video or meeting.")
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if question := st.chat_input("Ask a question about this video..."):
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        answer = to_text(ask_question(result["rag_chain"], question))
                    except Exception as e:
                        answer = f"Error: {e}"
                st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

    with tab_tr:
        search = st.text_input("🔎 Search in transcript", placeholder="Type a keyword...")
        if search:
            hits = [
                line
                for line in transcript.replace(". ", ".\n").split("\n")
                if search.lower() in line.lower()
            ]
            st.write(f"{len(hits)} matching sentence(s)")
            for h in hits:
                st.markdown(f"- {h.strip()}")
        else:
            st.text_area("Full transcript", transcript, height=420)
        st.download_button("⬇️ Download transcript", transcript, file_name="transcript.txt")