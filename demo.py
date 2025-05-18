import streamlit as st

st.set_page_config(page_title="LLaMA Chatbot", layout="centered")

# --- LOGIN AUTHENTICATION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None

if not st.session_state.authenticated:
    st.title("🔐 Login to LLaMA Chatbot")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login = st.button("Login")

    if login:
        if username == "admin" and password == "admin":
            st.session_state.authenticated = True
            st.session_state.role = "admin"
        elif username == "staff" and password == "staff":
            st.session_state.authenticated = True
            st.session_state.role = "staff"
        else:
            st.error("Invalid credentials")
    st.stop()

role = st.session_state.role

# --- SESSION SETUP ---
if "active_topic" not in st.session_state:
    st.session_state.active_topic = None
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {}
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}
if "file_suggestions" not in st.session_state:
    st.session_state.file_suggestions = {}
if "topics" not in st.session_state:
    st.session_state.topics = {
        "Tax Deductions": "💼",
        "Policy Query": "📜",
        "Crypto Tax": "🪙"
    }

# --- ADMIN FEATURES ON LANDING PAGE ---
if st.session_state.active_topic is None:
    st.title("🤖 Deloitte  Chatbot Prototype")

    if role == "admin":
        st.markdown("👤 **You are logged in as: Admin**")
        #st.markdown("### 🛠️ Admin Tools")
        admin_option = st.radio("Choose an admin action:", ["TaxChat Domains", "Add New Domain", "View Suggested Uploads"])

        if admin_option == "Add New Domain":
            st.subheader("➕ Add New Chat Topic")
            new_topic = st.text_input("Topic Name")
            new_icon = st.text_input("Emoji (e.g. 📚, 💬)")
            if st.button("Add Category") and new_topic and new_icon:
                st.session_state.topics[new_topic] = new_icon
                st.success(f"Added category: {new_icon} {new_topic}")

        elif admin_option == "View Suggested Uploads":
            st.subheader("📥 All Suggested File Uploads")
            has_suggestions = False
            for topic, suggestions in st.session_state.file_suggestions.items():
                if suggestions:
                    has_suggestions = True
                    with st.expander(f"{topic}"):
                        for i, s in enumerate(suggestions):
                            st.markdown(f"**#{i+1}** — Submitted by: `{s['submitted_by']}`")
                            if s["file"]:
                                st.markdown(f"- File Name: `{s['file']}`")
                            if s["comment"]:
                                st.markdown(f"- Comment: {s['comment']}")
                            st.markdown(f"- Status: `{s['status']}`")
                            st.divider()
            if not has_suggestions:
                st.info("📭 No file suggestions yet.")

        else:  # TaxChat Domains
            
            st.markdown("### 🧠 TaxChat Domains:")
            for topic, icon in st.session_state.topics.items():
                if st.button(f"{icon} {topic}"):
                    st.session_state.active_topic = topic
                    st.session_state.chat_histories.setdefault(topic, [])
                    st.session_state.uploaded_files.setdefault(topic, [])
                    st.session_state.file_suggestions.setdefault(topic, [])

    else:
        st.markdown("👤 **You are logged in as: Staff**")
        st.markdown("### 🧠 TaxChat Domains:")
        for topic, icon in st.session_state.topics.items():
            if st.button(f"{icon} {topic}"):
                st.session_state.active_topic = topic
                st.session_state.chat_histories.setdefault(topic, [])
                st.session_state.uploaded_files.setdefault(topic, [])
                st.session_state.file_suggestions.setdefault(topic, [])

else:
    topic = st.session_state.active_topic
    icon = st.session_state.topics[topic]
    st.markdown(f"### {icon} {topic} Chat")

    if st.button("🔙 Back to Home"):
        st.session_state.active_topic = None
        st.stop()

    # --- SIDEBAR (TRAINED FILES + FILE SUGGESTION FORM) ---
    with st.sidebar:
        st.markdown("### 📚 Trained Files")
        search_query = st.text_input("🔍 Search files...")
        files = st.session_state.uploaded_files[topic]

        # Inject demo files if none
        if not files:
            demo_files = {
                "Tax Deductions": [
                    "freelancer_expenses_2023.pdf", "home_office_claim.txt",
                    "deductible_items_list.md", "land_tax.pdf", "vehicle_expense_summary.txt"
                ],
                "Policy Query": [
                    "remote_work_policy.pdf", "expense_guidelines.txt",
                    "employee_handbook.md", "leave_policy_2023.pdf"
                ],
                "Crypto Tax": [
                    "crypto_gain_summary_2023.pdf", "binance_transactions.txt",
                    "wallet_report.md", "staking_taxation_guide.pdf"
                ]
            }
            st.session_state.uploaded_files[topic] = [
                {"name": name, "content": b""}
                for name in demo_files.get(topic, [])
            ]
            files = st.session_state.uploaded_files[topic]

        filtered_files = [f for f in files if search_query.lower() in f["name"].lower()] if search_query else files

        with st.container():
            scrollable_area = st.container()
            for f in filtered_files:
                if scrollable_area.button(f"📘 Ask about: {f['name']}", key=f"{topic}_sidebar_{f['name']}"):
                    st.session_state.chat_histories[topic].append(("user", f"What’s in {f['name']}?"))
                    st.session_state.chat_histories[topic].append(("assistant", f"🦙 Here's a mock summary of {f['name']}."))

        if role == "staff":
            st.divider()
            st.markdown("### 💡 Suggest a File for This Topic")
            with st.form(f"suggest_form_{topic}"):
                file = st.file_uploader("Upload your file", key=f"upload_{topic}")
                comment = st.text_area("Comment or reason for suggestion", key=f"comment_{topic}")
                submitted = st.form_submit_button("Submit Suggestion")

                if submitted:
                    if not file:
                        st.warning("Please upload a file.")
                    else:
                        st.success("Submitted to admin!")
                        st.session_state.file_suggestions[topic].append({
                            "file": file.name,
                            "link": None,
                            "comment": comment,
                            "submitted_by": role,
                            "status": "pending",
                            "admin_comment": ""
                        })

        elif role == "admin":
            st.divider()
            st.markdown("### 📤 Upload New File to Train This Topic")
            new_file = st.file_uploader("Upload a file to add directly", key=f"admin_upload_{topic}")
            if new_file:
                st.session_state.uploaded_files[topic].append({
                    "name": new_file.name,
                    "content": new_file.read()
                })
                st.success(f"File `{new_file.name}` added to topic: {topic}")

    # --- CHAT HISTORY ---
    for role_msg, msg in st.session_state.chat_histories[topic]:
        with st.chat_message(role_msg):
            st.markdown(msg)

    # --- INPUT BOX ---
    user_input = st.chat_input(f"Ask something about {topic.lower()}...")
    if user_input:
        st.session_state.chat_histories[topic].append(("user", user_input))
        st.session_state.chat_histories[topic].append(("assistant", f"🦙 LLaMA says: Here's a mock response to '{user_input}'."))

