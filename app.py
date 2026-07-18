"""GUPPI slice 1: Streamlit chat → LiteLLM → Ollama, traced in LangSmith, persisted to SQLite.

Run: streamlit run app.py
Prereqs: Ollama running with the model pulled (`ollama pull llama3.2`); a .env with
LANGSMITH_API_KEY, LANGSMITH_TRACING=true, LANGSMITH_PROJECT (loaded at startup).
"""
import litellm
import streamlit as st
from dotenv import load_dotenv

import agent
import store

load_dotenv()  # ponytail: standard local-dev secret loading — reads LANGSMITH_* from a .env file

MODEL = agent.MODEL  # single source of truth for the model tag (agent owns the loop + model)

# D6: LangSmith via LiteLLM's built-in callback — logs prompt/params, response, latency,
# tokens, model name at the model-call level. No custom instrumentation.
litellm.success_callback = ["langsmith"]
# Streamlit is sync, so LiteLLM's periodic async flush task never starts ("no running event
# loop"); a single call would queue the trace and never send it. batch_size=1 flushes each
# call immediately. ponytail: fine for a single-user local app; raise it if call volume ever
# makes per-call POSTs a bottleneck.
litellm.langsmith_batch_size = 1

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

    reply = agent.reply(st.session_state.messages)  # recall loop: may call the recall tool mid-turn

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

    store.add(MODEL, prompt, reply)
    st.rerun()  # refresh the sidebar memory panel with the new row
