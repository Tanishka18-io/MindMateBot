import streamlit as st 
import pandas as pd
import os
import html
from utils import (
    load_json,
    save_mood,
    register_user,
    authenticate_user,
    save_user_journal,
    load_user_journal,
    get_user_journal_path,
)
from responses import get_active_listening, get_random_tip, get_random_prompt, crisis_disclaimer
from nlp_utils import detect_intent
import google.generativeai as genai
from dotenv import load_dotenv
from base64 import b64encode

# ---------------- CONFIG ----------------
st.set_page_config(page_title="MindMate", page_icon="🧠", layout="wide")

# ---------------- GEMINI SETUP ----------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- SESSION ----------------
if "username" not in st.session_state:
    st.session_state.username = None
if "daily_goal" not in st.session_state:
    st.session_state.daily_goal = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- BACKGROUND IMAGE HANDLING ----------------
def set_bg_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = b64encode(img_file.read()).decode()
    st.markdown(f"""
    <style>
    html, body, .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
        background-attachment: fixed;
        font-family: 'Comfortaa', sans-serif;
        font-weight: bold;
        font-size: 24px;
        color: #000000;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: #000000 !important;
        font-weight: 800 !important;
        text-shadow: 2px 2px 0px #FFFFFF, 5px 4px 0px rgba(0,0,0,0.15);
    }}
    .stTextInput > div > div > input,
    .stTextArea textarea,
    .stNumberInput input,
    .stSelectbox select,
    .stButton > button {{
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #000000 !important;
        border: 3px solid #000000 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        background-color: #F9F6EE !important;
        box-shadow: 2px 2px 12px rgba(0,0,0,0);
    }}
    </style>
    """, unsafe_allow_html=True)

# ---------------- BACKGROUND ASSIGNMENT ----------------
if not st.session_state.logged_in:
    set_bg_image("C:/Users/tanis/Desktop/mindmate/img.jpg")
else:
    set_bg_image("C:/Users/tanis/Desktop/mindmate/api.png")


def set_bg_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = b64encode(img_file.read()).decode()
        st.markdown(f"""
        <style>
        html, body, .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center center;
            background-attachment: fixed;
            font-family: 'Comfortaa', sans-serif;
            font-weight: bold;
            font-size: 24px;
            color: #000000;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #000000 !important;
            font-weight: 900 !important;
        }}
        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stNumberInput input,
        .stSelectbox select,
        .stButton > button {{
            font-size: 20px !important;
            font-weight: 600 !important;
            color: #000000 !important;
            border: 2px solid #000000 !important;
            border-radius: 12px !important;
            padding: 12px !important;
            background-color: #F9F6EE !important;
            box-shadow: 2px 2px 12px rgba(0,0,0,0);
        }}
        </style>
        """, unsafe_allow_html=True)
    # else:
        # st.warning(f"⚠️ Background image not found at: {image_path}")

# ---------------- LOGIN/REGISTER ----------------
if not st.session_state.logged_in:
    st.markdown('<div class="form-glass">', unsafe_allow_html=True)
    st.title("🧠 Welcome to MindMate")
    choice = st.radio("Choose an option", ["Login", "Register"])

    if "just_registered" in st.session_state and st.session_state.just_registered:
        choice = "Login"
        st.session_state.just_registered = False

    if choice == "Login":
        st.markdown("### 🔐 <strong>Login to Continue</strong>", unsafe_allow_html=True)
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")
        if st.button("Login"):
            if authenticate_user(username, password):
                st.success("✅ Login successful")
                st.session_state.username = username
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

    elif choice == "Register":
        st.markdown("### 📝 <strong>Register New Account</strong>", unsafe_allow_html=True)
        with st.form("register_form"):
            username = st.text_input("👤 Username")
            password = st.text_input("🔒 Password", type="password")
            email = st.text_input("📧 Email")
            age = st.number_input("🎂 Age", min_value=1, max_value=120)
            gender = st.selectbox("⚧️ Gender", ["Male", "Female", "Other"])
            height = st.number_input("📏 Height (cm)", min_value=30.0, max_value=250.0)
            weight = st.number_input("⚖️ Weight (kg)", min_value=1.0, max_value=300.0)
            disease = st.text_input("🦠 Known Disease (Optional)")
            medical_condition = st.text_input("🧬 Medical Condition (Optional)")
            submitted = st.form_submit_button("Register")

            if submitted:
                if register_user(username, password, email, age, gender, height, weight, disease, medical_condition):
                    st.success("✅ Registered! Redirecting to login...")
                    st.session_state["just_registered"] = True
                    st.rerun()
                else:
                    st.warning("⚠️ Username already exists")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ---------------- BACKGROUND ASSIGNMENT ----------------
if not st.session_state.logged_in:
    set_bg_image("C:/Users/tanis/Desktop/mindmate/img.jng")
else:
    set_bg_image("C:/Users/tanis/Desktop/mindmate/api.png")

# ---------------- LOGIN/REGISTER ----------------
if not st.session_state.logged_in:
    st.markdown('<div class="form-glass">', unsafe_allow_html=True)
    st.title("🧠 Welcome to MindMate")
    choice = st.radio("Choose an option", ["Login", "Register"])

    if "just_registered" in st.session_state and st.session_state.just_registered:
        choice = "Login"
        st.session_state.just_registered = False

    if choice == "Login":
        st.markdown("### 🔐 <strong>Login to Continue</strong>", unsafe_allow_html=True)
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")
        if st.button("Login"):
            if authenticate_user(username, password):
                st.success("✅ Login successful")
                st.session_state.username = username
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

    elif choice == "Register":
        st.markdown("### 📝 <strong>Register New Account</strong>", unsafe_allow_html=True)
        with st.form("register_form"):
            username = st.text_input("👤 Username")
            password = st.text_input("🔒 Password", type="password")
            email = st.text_input("📧 Email")
            age = st.number_input("🎂 Age", min_value=1, max_value=120)
            gender = st.selectbox("⚧️ Gender", ["Male", "Female", "Other"])
            height = st.number_input("📏 Height (cm)", min_value=30.0, max_value=250.0)
            weight = st.number_input("⚖️ Weight (kg)", min_value=1.0, max_value=300.0)
            disease = st.text_input("🦠  Disease (Optional)")
            medical_condition = st.text_input("🧬 Medical Condition (Optional)")
            submitted = st.form_submit_button("Register")

            if submitted:
                if register_user(username, password, email, age, gender, height, weight, disease, medical_condition):
                    st.success("✅ Registered! Redirecting to login...")
                    st.session_state["just_registered"] = True
                    st.rerun()
                else:
                    st.warning("⚠️ Username already exists")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()
# ---------------- MAIN UI ----------------
st.title(":brain: MindMate – Your AI Therapeutic Companion")

# ---------------- LOGOUT ----------------
if st.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.daily_goal = ""
    st.session_state.chat_history = []
    st.rerun()

# ---------------- GOAL SETUP ----------------
if not st.session_state.daily_goal:
    with st.form("goal_form"):
        goal_input = st.text_input(f"🎯 Hi {st.session_state.username}, what's your goal for today?")
        submitted = st.form_submit_button("Set Goal")
        if submitted and goal_input.strip():
            st.session_state.daily_goal = goal_input.strip()
            st.rerun()

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📓 Journal", "📄 Health Report Analysis"])

# ---------------- CHAT TAB ----------------
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
                reply = reply.replace("{name}", st.session_state.username)
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

# ---------------- JOURNAL TAB ----------------
with tab2:
    st.subheader(":memo: Journal your thoughts")
    entry = st.text_area("Write here:")
    if st.button("📂 Save Entry"):
        if entry.strip():
            save_user_journal(st.session_state.username, entry)
            st.success("Entry saved!")

    all_entries = load_user_journal(st.session_state.username)

    if all_entries:
        st.subheader(":books: Your Entries")
        for i, e in enumerate(reversed(all_entries[-5:])):
            col1, col2 = st.columns([6, 1])
            with col1:
                new_text = st.text_area(f"Entry {i+1}", e, key=f"entry_{i}")
            with col2:
                if st.button("🖑️ Delete", key=f"del_{i}"):
                    all_entries.pop(all_entries.index(e))
                    with open(get_user_journal_path(st.session_state.username), "w", encoding="utf-8") as f:
                        f.write("\n---\n".join(all_entries))
                    st.rerun()
                if st.button("✅ Update", key=f"upd_{i}"):
                    all_entries[all_entries.index(e)] = new_text
                    with open(get_user_journal_path(st.session_state.username), "w", encoding="utf-8") as f:
                        f.write("\n---\n".join(all_entries))
                    st.success("Entry updated!")
                    st.rerun()

# ---------------- REPORT UPLOAD TAB ----------------
with tab3:
    st.subheader("📄 Upload a Health Report for AI Insights")
    uploaded_file = st.file_uploader("Upload Report (PDF or TXT)", type=["pdf", "txt"])

    if uploaded_file:
        import PyPDF2

        if uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        else:
            text = uploaded_file.read().decode("utf-8")

        st.text_area("📋 Extracted Text", text, height=200)

        if st.button("🧠 Analyze with Gemini"):
            try:
                prompt = f"You are a medical assistant. Analyze this health report and provide:\n\n1. Overview of the content\n2. Disease explanation\n3. Symptoms\n4. Wellness tips\n\nReport:\n{text}"
                analysis = gemini_model.generate_content(prompt)
                st.markdown("### 🧾 Gemini Report Summary")
                st.markdown(analysis.text)
            except Exception as e:
                st.error(f"❌ Gemini Analysis Error: {str(e)}")
