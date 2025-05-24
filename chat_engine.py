# chat_engine.py
from config import PRE_SAVED_ANSWERS

def get_response(user_input, topic):
    q = user_input.strip().lower()
    answers = PRE_SAVED_ANSWERS.get(topic, {})

    if q in answers:
        a = answers[q]
        confidence = a.get("confidence", 0.92)

        return (
            #f"**🧠 Answer:**\n\n"
            f"{a['response']}\n\n"
            f"**📄 Source:** `{a['source']}`\n"
            f"**🔖 Reference:** {a['section']}\n\n"
            f"*🤖 Confidence: {int(confidence * 100)}%*"
        )
    else:
        return "I don’t have knowledge on that topic yet. Please try asking something else or check back later."
