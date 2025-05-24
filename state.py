# state.py

from config import TOPICS

def init_state(st):
    st.session_state.setdefault("authenticated", False)
    st.session_state.setdefault("role", None)
    st.session_state.setdefault("logout_requested", False)
    st.session_state.setdefault("active_topic", None)
    st.session_state.setdefault("chat_histories", {})
    st.session_state.setdefault("uploaded_files", {})
    st.session_state.setdefault("file_suggestions", {})
    st.session_state.setdefault("topics", TOPICS)
