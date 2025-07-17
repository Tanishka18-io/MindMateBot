


# import streamlit as st
# import pandas as pd
# import os
# import html
# from utils import load_json, save_mood
# from responses import get_active_listening, get_random_tip, get_random_prompt, crisis_disclaimer
# from nlp_utils import detect_intent
# import google.generativeai as genai
# from dotenv import load_dotenv
# from streamlit.components.v1 import html as st_html

# # ---------------- CONFIG ----------------
# st.set_page_config(page_title="MindMate", page_icon="🧠", layout="wide")

# # ---------------- GEMINI SETUP ----------------
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# # ---------------- SESSION ----------------
# if "username" not in st.session_state:
#     st.session_state.username = ""
# if "daily_goal" not in st.session_state:
#     st.session_state.daily_goal = ""
# if "greeted" not in st.session_state:
#     st.session_state.greeted = False
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "journal_entries" not in st.session_state:
#     st.session_state.journal_entries = []

# # ---------------- THEME ----------------


# import streamlit as st

# # Theme toggle
# theme = st.sidebar.radio("🗿 Choose Theme", ["Light", "Dark"])
# show_sidebar = st.sidebar.checkbox("📂 Toggle Sidebar", value=True)

# if theme == "Dark":
#     background = "#121212"
#     primary = "#00cec9"
#     input_bg = "#1e1e1e"
#     text_color = "#f5f5f5"
#     button_border = "#00cec9"
#     journal_color = "#2c2c2c"
#     highlight_color = "#81ecec"
# else:
#     background = "#f0f3f4"
#     primary = "#0984e3"
#     input_bg = "#ffffff"
#     text_color = "#2d3436"
#     button_border = "#74b9ff"
#     journal_color = "#dfe6e9"
#     highlight_color = "#0984e3"

# # Hide sidebar if toggled off
# if not show_sidebar:
#     st.markdown(
#         """<style>
#         section[data-testid="stSidebar"] {
#             display: none !important;
#         }
#         </style>""", unsafe_allow_html=True
#     )

# # Apply the style
# st.markdown(f"""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@400;600&display=swap');

#     html, body, .stApp {{
#         font-family: 'Comfortaa', sans-serif;
#         background-color: {background};
#         color: {text_color};
#         transition: background-color 0.8s ease, color 0.8s ease;
#         scroll-behavior: smooth;
#     }}

#     .stTextInput, .stTextArea textarea {{
#         background-color: {input_bg} !important;
#         color: {text_color} !important;
#         border: 2px solid {primary} !important;
#         border-radius: 15px;
#         padding: 12px;
#         transition: all 0.3s ease-in-out;
#         box-shadow: 0 4px 10px rgba(0,0,0,0.1);
#     }}

#     .stTextInput:hover, .stTextArea:hover textarea {{
#         transform: scale(1.02);
#         box-shadow: 0 8px 18px rgba(0,0,0,0.2);
#     }}

#     button[kind="primary"] {{
#         background-color: {primary} !important;
#         color: white !important;
#         border-radius: 15px;
#         padding: 0.6em 1.2em;
#         font-weight: 600;
#         font-size: 1rem;
#         transition: transform 0.3s ease, background-color 0.4s ease;
#         box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
#     }}

#     button[kind="primary"]:hover {{
#         transform: scale(1.05);
#         background-color: {highlight_color} !important;
#         box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
#     }}

#     .journal-entry {{
#         background-color: {journal_color};
#         padding: 20px;
#         margin: 15px 0;
#         border-left: 5px solid {primary};
#         border-radius: 15px;
#         color: {text_color};
#         box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
#         transition: all 0.3s ease-in-out;
#         animation: fadeInUp 0.5s ease;
#     }}

#     .journal-entry:hover {{
#         box-shadow: 0 8px 18px rgba(0, 0, 0, 0.2);
#         transform: scale(1.01);
#     }}

#     .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
#         color: {primary};
#         font-weight: 700;
#         text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
#         transition: all 0.5s ease;
#         animation: popFade 1s ease;
#     }}

#     .highlight {{
#         color: {highlight_color};
#         font-weight: 600;
#     }}

#     @keyframes fadeInUp {{
#         from {{
#             opacity: 0;
#             transform: translateY(20px);
#         }}
#         to {{
#             opacity: 1;
#             transform: translateY(0);
#         }}
#     }}

#     @keyframes popFade {{
#         0% {{
#             transform: scale(0.95);
#             opacity: 0;
#         }}
#         100% {{
#             transform: scale(1);
#             opacity: 1;
#         }}
#     }}

#     .chat-bubble {{
#         padding: 15px;
#         margin: 10px 0;
#         border-radius: 15px;
#         animation: fadeInUp 0.4s ease;
#     }}

#     .chat-bubble.user {{
#         background-color: #ffeaa7;
#         color: #2d3436;
#         align-self: flex-end;
#     }}

#     .chat-bubble.bot {{
#         background-color: #a29bfe;
#         color: white;
#     }}
#     </style>
# """, unsafe_allow_html=True)


# # ---------------- UI ----------------
# with st.sidebar:
#     if st.session_state.username:
#         st.markdown(f"👤 **User:** {st.session_state.username}")
#     if st.session_state.daily_goal:
#         st.markdown(f"🎯 **Goal:** {st.session_state.daily_goal}")
#     st.markdown("---")
#     st.markdown("Made with ❤️ for mental wellness")

# st.title(":brain: MindMate – Your AI Therapeutic Companion")

# # ---------------- User Info Collection ----------------
# if not st.session_state.username:
#     with st.form("username_form"):
#         st.markdown("## 👋 Welcome to MindMate!")
#         name_input = st.text_input("What should I call you?")
#         submitted = st.form_submit_button("Continue")
#         if submitted and name_input.strip():
#             st.session_state.username = name_input.strip()
#             st.rerun()

# if st.session_state.username and not st.session_state.daily_goal:
#     with st.form("goal_form"):
#         goal_input = st.text_input(f"🎯 Hi {st.session_state.username}, what's your goal for today?")
#         submitted = st.form_submit_button("Set Goal")
#         if submitted and goal_input.strip():
#             st.session_state.daily_goal = goal_input.strip()
#             st.rerun()

# # ---------------- Tabs ----------------
# tab1, tab2 = st.tabs(["💬 Chat", "📓 Journal"])

# # ---------------- Chat ----------------
# with tab1:
#     with st.form("chat_form", clear_on_submit=True):
#         user_input = st.text_input("You:", "")
#         submitted = st.form_submit_button("Send")

#     if submitted and user_input:
#         if user_input.lower().startswith("mood:"):
#             mood = user_input.split(":", 1)[-1].strip()
#             save_mood(mood)
#             response = f"Mood recorded: **{mood}**"
#         else:
#             try:
#                 gemini_response = gemini_model.generate_content(user_input)
#                 reply = gemini_response.text
#             except Exception as e:
#                 reply = f"⚠️ Error: {str(e)}"

#             listening = get_active_listening()
#             tip = get_random_tip(load_json("data/cbt_tips.json"))
#             prompt = get_random_prompt(load_json("data/prompts.json"))
#             response = f"{reply}\n\n{listening}\n\n**Tip:** {tip}\n\n**Prompt:** {prompt}\n\n{crisis_disclaimer()}"

#         st.session_state.chat_history.append(("You", user_input))
#         st.session_state.chat_history.append(("MindMate", response))

#     st.markdown("### 🔨 Chat History")
#     for sender, message in st.session_state.chat_history:
#         safe_msg = html.escape(message).encode('utf-16', 'surrogatepass').decode('utf-16')
#         st.markdown(f"**{sender}:** {safe_msg}")

# # ---------------- Journal ----------------
# with tab2:
#     st.subheader(":memo: Journal your thoughts")
#     entry = st.text_area("Write here:")
#     if st.button("💾 Save Entry"):
#         if entry.strip():
#             with open("data/journal.txt", "a", encoding="utf-8") as f:
#                 f.write(f"{entry.strip()}\n---\n")
#             st.success("Entry saved!")

#     if os.path.exists("data/journal.txt"):
#         with open("data/journal.txt", "r", encoding="utf-8") as f:
#             all_entries = f.read().split("---")
#             all_entries = [e.strip() for e in all_entries if e.strip()]

#         st.subheader(":books: Your Entries")
#         for i, e in enumerate(reversed(all_entries[-5:])):
#             col1, col2 = st.columns([6, 1])
#             with col1:
#                 new_text = st.text_area(f"Entry {i+1}", e, key=f"entry_{i}")
#             with col2:
#                 if st.button("🗑️ Delete", key=f"del_{i}"):
#                     all_entries.pop(all_entries.index(e))
#                     with open("data/journal.txt", "w", encoding="utf-8") as f:
#                         f.write("\n---\n".join(all_entries))
#                     st.rerun()
#                 if st.button("✅ Update", key=f"upd_{i}"):
#                     all_entries[all_entries.index(e)] = new_text
#                     with open("data/journal.txt", "w", encoding="utf-8") as f:
#                         f.write("\n---\n".join(all_entries))
#                     st.success("Entry updated!")
#                     st.rerun()


import streamlit as st
import pandas as pd
import os
import html
from utils import load_json, save_mood
from responses import get_active_listening, get_random_tip, get_random_prompt, crisis_disclaimer
from nlp_utils import detect_intent
import google.generativeai as genai
from dotenv import load_dotenv

# ---------------- CONFIG ----------------
st.set_page_config(page_title="MindMate", page_icon="🧠", layout="wide")

# ---------------- GEMINI SETUP ----------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

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

# ---------------- FORCE LIGHT THEME + HIDE SIDEBAR ----------------
st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        display: none !important;
    }

    @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@400;600&display=swap');

    html, body, .stApp {
        font-family: 'Comfortaa', sans-serif;
        background-color: #f4f6f8;
        color: #2d3436;
        transition: background-color 0.8s ease, color 0.8s ease;
        scroll-behavior: smooth;
    }

    .stTextInput, .stTextArea textarea {
        background-color: #ffffff !important;
        color: #2d3436 !important;
        border: 2px solid #0984e3 !important;
        border-radius: 15px;
        padding: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        transition: all 0.3s ease-in-out;
    }

    .stTextInput:hover, .stTextArea:hover textarea {
        transform: scale(1.02);
        box-shadow: 0 8px 18px rgba(0,0,0,0.1);
    }

    button[kind="primary"] {
        background-color: #0984e3 !important;
        color: white !important;
        border-radius: 15px;
        padding: 0.6em 1.2em;
        font-weight: 600;
        font-size: 1rem;
        transition: transform 0.3s ease, background-color 0.4s ease;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
    }

    button[kind="primary"]:hover {
        transform: scale(1.05);
        background-color: #74b9ff !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }

    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #0984e3;
        font-weight: 700;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        animation: fadeInUp 0.6s ease;
    }

    .journal-entry {
        background-color: #dfe6e9;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #0984e3;
        border-radius: 15px;
        color: #2d3436;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        animation: fadeInUp 0.4s ease;
    }

    .journal-entry:hover {
        transform: scale(1.01);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .chat-bubble {
        padding: 15px;
        margin: 10px 0;
        border-radius: 15px;
        animation: fadeInUp 0.4s ease;
    }

    .chat-bubble.user {
        background-color: #ffeaa7;
        color: #2d3436;
        align-self: flex-end;
    }

    .chat-bubble.bot {
        background-color: #a29bfe;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- MAIN UI ----------------
st.title(":brain: MindMate – Your AI Therapeutic Companion")

# ---------------- User Info ----------------
if not st.session_state.username:
    with st.form("username_form"):
        st.markdown("## 👋 Welcome to MindMate!")
        name_input = st.text_input("What should I call you?")
        submitted = st.form_submit_button("Continue")
        if submitted and name_input.strip():
            st.session_state.username = name_input.strip()
            st.rerun()

if st.session_state.username and not st.session_state.daily_goal:
    with st.form("goal_form"):
        goal_input = st.text_input(f"🎯 Hi {st.session_state.username}, what's your goal for today?")
        submitted = st.form_submit_button("Set Goal")
        if submitted and goal_input.strip():
            st.session_state.daily_goal = goal_input.strip()
            st.rerun()

# ---------------- Tabs ----------------
tab1, tab2 = st.tabs(["💬 Chat", "📓 Journal"])

# ---------------- Chat Tab ----------------
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
            try:
                gemini_response = gemini_model.generate_content(user_input)
                reply = gemini_response.text
            except Exception as e:
                reply = f"⚠️ Error: {str(e)}"

            listening = get_active_listening()
            tip = get_random_tip(load_json("data/cbt_tips.json"))
            prompt = get_random_prompt(load_json("data/prompts.json"))
            response = f"{reply}\n\n{listening}\n\n**Tip:** {tip}\n\n**Prompt:** {prompt}\n\n{crisis_disclaimer()}"

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("MindMate", response))

    st.markdown("### 🔨 Chat History")
    for sender, message in st.session_state.chat_history:
        safe_msg = html.escape(message).encode('utf-16', 'surrogatepass').decode('utf-16')
        st.markdown(f"**{sender}:** {safe_msg}")

# ---------------- Journal Tab ----------------
with tab2:
    st.subheader(":memo: Journal your thoughts")
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

        st.subheader(":books: Your Entries")
        for i, e in enumerate(reversed(all_entries[-5:])):
            col1, col2 = st.columns([6, 1])
            with col1:
                new_text = st.text_area(f"Entry {i+1}", e, key=f"entry_{i}")
            with col2:
                if st.button("🗑️ Delete", key=f"del_{i}"):
                    all_entries.pop(all_entries.index(e))
                    with open("data/journal.txt", "w", encoding="utf-8") as f:
                        f.write("\n---\n".join(all_entries))
                    st.rerun()
                if st.button("✅ Update", key=f"upd_{i}"):
                    all_entries[all_entries.index(e)] = new_text
                    with open("data/journal.txt", "w", encoding="utf-8") as f:
                        f.write("\n---\n".join(all_entries))
                    st.success("Entry updated!")
                    st.rerun()

