print("APP.PY IS EXECUTING")
import streamlit as st
from agents.manager import Manager
from memory.database import initialize_database
from ui.styles import load_css

import asyncio

# from speech_to_text import listen
# from tts import speak

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

#load_css()

# -------------------------
# Initialize Manager
# -------------------------
initialize_database()
manager = Manager()

# -------------------------
# Session State
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:

    st.markdown("# 🤖 AI Assistant")

    st.caption("Multi-Agent Voice Assistant")

    st.divider()

    # -----------------------------
    # Chat Controls
    # -----------------------------
    st.subheader("💬 Chat")

    if st.button("🆕 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # -----------------------------
    # Voice
    # -----------------------------
    st.subheader("🎤 Voice")

    voice_enabled = st.toggle(
        "Enable Voice",
        value=True,
        disabled=True
    )

    st.divider()

    # -----------------------------
    # Statistics
    # -----------------------------
    st.subheader("📊 Statistics")

    st.metric(
        "Messages",
        len(st.session_state.messages)
    )

    st.divider()

    # -----------------------------
    # About
    # -----------------------------
    st.subheader("ℹ About")

    st.caption("Version 1.0")

    st.caption("Built with")

    st.write("• Streamlit")

    st.write("• Groq")

    st.write("• Multi-Agent AI")

    st.write("• Whisper")

    st.divider()

    st.caption("👨‍💻 Developed by Chaithra")

# -------------------------
# Main Page
# -------------------------
st.markdown(
    """
    <div class="main-title">
        🤖 AI Voice Assistant
    </div>

    <div class="subtitle">
        Multi-Agent • Voice Enabled • Powered by Groq
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Display Chat
# -------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Voice Input Button
# -----------------------------
prompt = None

if st.button("🎤 Speak"):

    with st.spinner("Loading microphone..."):

        from speech_to_text import listen

        prompt, language = listen()

        st.success(f"You said: {prompt}")

# -------------------------
# Chat Input
# -------------------------
typed_prompt = st.chat_input("Ask me anything...")

if typed_prompt:
    prompt = typed_prompt

if prompt:

    # Show User
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):
            response = manager.process(prompt)


            answer = response["response"]

            st.markdown(answer)

            #asyncio.run(speak(answer))

            # ----------------------------
            # Execution Details
            # ----------------------------
            with st.expander("🔍 Execution Details", expanded=False):

                for i, step in enumerate(response["plan"], start=1):

                    st.markdown(f"### Step {i}")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("**Agent**")
                        st.success(step["agent"])

                    with col2:
                        if step.get("tool"):
                            st.write("**Tool**")
                            st.info(step["tool"])

                    if step.get("action"):
                        st.write("**Action**")
                        st.code(step["action"])

                    if step.get("parameters"):
                        st.write("**Parameters**")
                        st.json(step["parameters"])

                st.divider()

                st.subheader("Result")

                for result in response["results"]:

                    if result["status"] == "success":
                        st.success(result["result"])
                    else:
                        st.error(result)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )