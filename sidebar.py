# sidebar.py

import streamlit as st

def render_sidebar(topic, role):
    st.markdown("### 📚 Trained Files")

    # Ensure session state keys are initialized
    st.session_state.uploaded_files.setdefault(topic, [])
    st.session_state.chat_histories.setdefault(topic, [])
    st.session_state.file_suggestions.setdefault(topic, [])

    search_query = st.text_input("🔍 Search files...")
    files = st.session_state.uploaded_files[topic]

    # Inject demo files if empty
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

    # File search filter
    filtered_files = [
        f for f in files if search_query.lower() in f["name"].lower()
    ] if search_query else files

    # Ask buttons
    for f in filtered_files:
        if st.button(f"📘{f['name']}", key=f"{topic}_{f['name']}"):
            st.session_state.chat_histories[topic].append(("user", f"What’s in {f['name']}?"))
            st.session_state.chat_histories[topic].append(("assistant", f"🦙 Here's a mock summary of {f['name']}."))

    # Staff suggestion form
    if role == "staff":
        st.divider()
        st.markdown("### 💡 Suggest a File for This Topic")
        with st.form(f"suggest_form_{topic}"):
            file = st.file_uploader("Upload your file", key=f"upload_{topic}")
            comment = st.text_area("Comment or reason for suggestion", key=f"comment_{topic}")
            if st.form_submit_button("Submit Suggestion"):
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

    # Admin direct upload
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
