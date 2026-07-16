"""GUPPI slice 1: Streamlit chat → LiteLLM → Ollama, traced in LangSmith, persisted to SQLite.

Run: streamlit run app.py
Prereqs: Ollama running with the model pulled (`ollama pull llama3.2`); LANGSMITH_API_KEY set.
"""
import litellm
import streamlit as st

import store

MODEL = "ollama/llama3.2"

# D6: LangSmith via LiteLLM's built-in callback — logs prompt/params, response, latency,
# tokens, model name at the model-call level. No custom instrumentation.
litellm.success_callback = ["langsmith"]

store.init()

st.title("GUPPI")

# Sidebar: durable structured memory, queried by field from SQLite (not this session's log).
with st.sidebar:
    st.header("Memory")
    st.dataframe(store.recent(), use_container_width=True)

# In-session conversation so the thread renders across Streamlit reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Say something"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    resp = litellm.completion(model=MODEL, messages=st.session_state.messages)
    reply = resp.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

    store.add(MODEL, prompt, reply)
    st.rerun()  # refresh the sidebar memory panel with the new row
