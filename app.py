import streamlit as st
from agents.manager import Manager

import asyncio

# from speech_to_text import listen
# from tts import speak

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🤖",
    layout="wide"
)

# -------------------------
# Initialize Manager
# -------------------------
@st.cache_resource
def load_manager():
    return Manager()

manager = load_manager()

# -------------------------
# Session State
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# Sidebar
# -------------------------
with st.sidebar:

    st.title("🤖 AI Voice Assistant")

    st.write("### Features")
    st.header("Project Status")

    st.success("Phase 1 ✔ Chatbot")

    st.success("Phase 2 ✔ Memory")

    st.success("Phase 3 ✔ Speech to Text")

    st.success("Phase 4 ✔ Text to Speech")

    st.success("Phase 5 ✔ Tools")

    st.success("Phase 6 ✔ Multi-Agent")

    st.info("Phase 7 🔄 Streamlit UI")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("Developed by Chaithra")

    st.caption("Groq • Streamlit • Multi-Agent AI")

# -------------------------
# Main Page
# -------------------------
st.title("🤖 AI Voice Assistant")

st.caption("Powered by Groq + Multi-Agent AI")

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