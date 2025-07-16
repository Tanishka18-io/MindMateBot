import streamlit as st
import pandas as pd
import os
import html
from utils import load_json, save_mood
from responses import get_active_listening, get_random_tip, get_random_prompt, crisis_disclaimer, get_intent_response
from nlp_utils import detect_intent

# ---------------- CONFIG ----------------
st.set_page_config(page_title="MindMate", page_icon="🧠", layout="wide")

# ---------------- SESSION ----------------
if "username" not in st.session_state:
    st.session_state.username = ""
if "daily_goal" not in st.session_state:
    st.session_state.daily_goal = ""
if "greeted" not in st.session_state:
    st.session_state.greeted = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []

# ---------------- USER INPUT ----------------
if not st.session_state.username:
    with st.container():
        st.markdown("## 👋 Welcome to MindMate!")
        with st.form("username_form"):
            name_input = st.text_input("What should I call you?")
            submitted = st.form_submit_button("Continue")
            if submitted and name_input.strip():
                st.session_state.username = name_input.strip()
                st.rerun()

if st.session_state.username and not st.session_state.daily_goal:
    with st.container():
        with st.form("goal_form"):
            goal_input = st.text_input(f"🎯 Hi {st.session_state.username}, what's your goal for today?")
            submitted = st.form_submit_button("Set Goal")
            if submitted and goal_input.strip():
                st.session_state.daily_goal = goal_input.strip()
                st.rerun()

# ---------------- UI COLORS ----------------
theme = st.sidebar.radio("🧿 Choose Theme", ["Light", "Dark"])
if theme == "Dark":
    background = "#081c15"
    primary = "#52b788"
    input_bg = "#1b4332"
    text_color = "#d8f3dc"
    button_border = "#74c69d"
    journal_color = "#2d6a4f"
else:
    background = "#02c39a"
    primary = "#00a896"
    input_bg = "#f0f3bd"
    text_color = "#000000"
    button_border = "#05668d"
    journal_color = "#f0f3bd"

st.markdown(f"""
    <style>
    .stApp {{
        background: {background};
        color: {text_color};
        font-family: 'Segoe UI', sans-serif;
    }}
    textarea, .stTextInput > div > div > input {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 2px solid {primary} !important;
        border-radius: 10px;
        padding: 10px;
    }}
    button[kind="primary"] {{
        color: {button_border} !important;
        border: 2px solid {button_border} !important;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease-in-out;
    }}
    button[kind="primary"]:hover {{
        background-color: {primary} !important;
        color: white !important;
        transform: scale(1.05);
    }}
    .journal-entry {{
        background-color: {journal_color};
        padding: 15px;
        margin: 10px 0;
        border-left: 6px solid {primary};
        border-radius: 10px;
        color: {text_color};
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }}
    </style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    if st.session_state.username:
        st.markdown(f"👤 **User:** {st.session_state.username}")
    if st.session_state.daily_goal:
        st.markdown(f"🎯 **Goal:** {st.session_state.daily_goal}")
    st.markdown("---")
    st.markdown("Made with ❤️ for mental wellness")

# ---------------- TITLE ----------------
st.title("🧠 MindMate – Your AI Therapeutic Companion")

if st.session_state.username and not st.session_state.greeted:
    st.success(f"🌞 Welcome back, {st.session_state.username}!")
    if st.session_state.daily_goal:
        st.info(f"🎯 Today's goal: {st.session_state.daily_goal}")
    st.session_state.greeted = True

# ---------------- DATA ----------------
tips = load_json("data/cbt_tips.json")
prompts = load_json("data/prompts.json")

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["💬 Chat", "📓 Journal"])

# ---------------- CHAT ----------------
with tab1:
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("You:", "")
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        if user_input.lower().startswith("mood:"):
            mood = user_input.split(":", 1)[-1].strip()
            save_mood(mood)
            response = f"Mood recorded: **{mood}**"
        else:
            intent = detect_intent(user_input)
            reply = get_intent_response(intent)
            reply = reply.replace("{name}", st.session_state.username)
            listening = get_active_listening()
            tip = get_random_tip(tips)
            prompt = get_random_prompt(prompts)
            response = f"{reply}\n\n{listening}\n\n**Tip:** {tip}\n\n**Prompt:** {prompt}\n\n{crisis_disclaimer()}"

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("MindMate", response))

    st.markdown("### 🗨️ Chat History")
    for sender, message in st.session_state.chat_history:
        safe_msg = html.escape(message).encode('utf-16', 'surrogatepass').decode('utf-16')
        st.markdown(f"**{sender}:** {safe_msg}")

# ---------------- JOURNAL ----------------
with tab2:
    st.subheader("📝 Journal your thoughts")
    entry = st.text_area("Write here:")
    if st.button("💾 Save Entry"):
        if entry.strip():
            with open("data/journal.txt", "a", encoding="utf-8") as f:
                f.write(f"{entry.strip()}\n---\n")
            st.success("Entry saved!")

    if os.path.exists("data/journal.txt"):
        with open("data/journal.txt", "r", encoding="utf-8") as f:
            all_entries = f.read().split("---")
            all_entries = [e.strip() for e in all_entries if e.strip()]

        st.subheader("📚 Your Entries")
        for i, e in enumerate(reversed(all_entries[-5:])):
            col1, col2 = st.columns([6, 1])
            with col1:
                new_text = st.text_area(f"Entry {i+1}", e, key=f"entry_{i}")
            with col2:
                if st.button("🗑️ Delete", key=f"del_{i}"):
                    index_to_remove = all_entries.index(e)
                    all_entries.pop(index_to_remove)
                    with open("data/journal.txt", "w", encoding="utf-8") as f:
                        f.write("\n---\n".join(all_entries))
                    st.rerun()
                if st.button("✅ Update", key=f"upd_{i}"):
                    index_to_update = all_entries.index(e)
                    all_entries[index_to_update] = new_text
                    with open("data/journal.txt", "w", encoding="utf-8") as f:
                        f.write("\n---\n".join(all_entries))
                    st.success("Entry updated!")
                    st.rerun()

# ---------------- SENTIMENT ----------------
# with tab3:
#     if os.path.exists("data/sentiment_log.csv"):
#         df = pd.read_csv("data/sentiment_log.csv")
#         if not df.empty:
#             st.subheader("📊 Sentiment Trends")
#             st.bar_chart(df['sentiment'].value_counts())
#         else:
#             st.info("No data available yet.")
#     else:
#         st.info("Start chatting to generate sentiment data.")
