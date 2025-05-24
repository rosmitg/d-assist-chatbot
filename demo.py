import streamlit as st
from auth import check_credentials
from config import TOPICS
from state import init_state
from chat_engine import get_response
from sidebar import render_sidebar

st.set_page_config(page_title="Deloitte Chatbot", layout="centered")
init_state(st)

# --- Logout Logic ---
if st.session_state.logout_requested:
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

# --- Login ---
if not st.session_state.authenticated:
    st.title("🔐 Login to Deloitte Chatbot")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        role = check_credentials(username, password)
        if role:
            st.session_state.authenticated = True
            st.session_state.role = role
        else:
            st.error("Invalid credentials")
    st.stop()

role = st.session_state.role

# --- Topic Selection Page ---
if st.session_state.active_topic is None:
    col1, col2 = st.columns([5, 2])
    with col1:
        st.markdown("### 🤖 Deloitte Chatbot")
        st.markdown("**Your virtual Deloitte expert - Powering the next generation of client service.**", unsafe_allow_html=True)

    with col2:
        with st.form("logout_form"):
            st.markdown(f"👤 **{role.capitalize()}**", unsafe_allow_html=True)
            submitted = st.form_submit_button("🚪 Logout")
            if submitted:
                st.session_state.logout_requested = True
                st.stop()



    st.markdown("### 🧠 Chat Domains")
    topics = list(st.session_state.topics.items())
    cols = st.columns(2)

    for i, (topic, icon) in enumerate(topics):
        with cols[i % 2]:
            with st.form(f"form_{topic}"):
                st.markdown(
                    f"""
                    <div style='
                        border: 1px solid #e0e0e0;
                        border-radius: 12px;
                        padding: 20px;
                        margin-bottom: 15px;
                        background-color: #fafafa;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
                    '>
                        <h4 style='margin-top: 0;'>{icon} {topic}</h4>
                        <p style='color: #555; font-size: 13px;'>
                            Click below to enter this topic's chatbot session.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                submitted = st.form_submit_button("Open Chat")
                if submitted:
                    st.session_state.active_topic = topic
                    st.session_state.chat_histories.setdefault(topic, [])
                    st.session_state.uploaded_files.setdefault(topic, [])
                    st.session_state.file_suggestions.setdefault(topic, [])
                    st.rerun()

    # --- Add New Domain as a card ---
    with st.expander("➕ Add New Domain"):
        new_topic = st.text_input("Topic Name")
        new_icon = st.text_input("Emoji (e.g. 📚, 💬)")
        if st.button("Add Category") and new_topic and new_icon:
            st.session_state.topics[new_topic] = new_icon
            st.success(f"Added category: {new_icon} {new_topic}")

else:
    topic = st.session_state.active_topic
    icon = st.session_state.topics[topic]
    st.markdown(f"### {icon} {topic} Chat")

    if st.button("🔙 Back to Home"):
        st.session_state.active_topic = None
        st.stop()

    with st.sidebar:
        render_sidebar(topic, role)

    for sender, message in st.session_state.chat_histories[topic]:
        if sender == "user":
            with st.chat_message("user"):
                st.markdown(message)
        elif sender == "assistant":
            st.markdown(message, unsafe_allow_html=True)

    user_input = st.chat_input(f"Ask something about {topic.lower()}...")
    if user_input:
        st.session_state.chat_histories[topic].append(("user", user_input))
        response = get_response(user_input, topic)
        st.session_state.chat_histories[topic].append(("assistant", response))
        st.rerun()
