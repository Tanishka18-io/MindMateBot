import json
import os
from datetime import datetime

# Load a JSON file
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

# Save user mood into CSV
def save_mood(mood, path="data/moods.csv"):
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()},{mood}\n")

# Save journal entry to file
def save_journal(entry, path="data/journal.txt"):
    if entry.strip():
        with open(path, "a", encoding="utf-8") as f:
            f.write(entry.strip() + "\n---\n")

# Load all journal entries
def load_journal(path="data/journal.txt"):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().split("---")
            return [e.strip() for e in content if e.strip()]
    return []





import hashlib
import json
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists("data/users.json"):
        return {}
    with open("data/users.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open("data/users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def register_user(username, password, email, age, gender, height, weight, disease, medical_condition):
    users = load_users()
    if username in users:
        return False
    users[username] = {
        "password": hash_password(password),
        "email": email,
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "disease": disease,
        "medical_condition": medical_condition
    }
    save_users(users)
    return True

def authenticate_user(username, password):
    users = load_users()
    user = users.get(username)
    if not user or not isinstance(user, dict):
        return False
    return user["password"] == hash_password(password)


    import os

def get_user_journal_path(username):
    os.makedirs("data/journals", exist_ok=True)
    return os.path.join("data/journals", f"{username}_journal.txt")

def save_user_journal(username, entry):
    journal_path = get_user_journal_path(username)
    with open(journal_path, "a", encoding="utf-8") as f:
        f.write(f"{entry.strip()}\n---\n")

def load_user_journal(username):
    journal_path = get_user_journal_path(username)
    if not os.path.exists(journal_path):
        return []
    with open(journal_path, "r", encoding="utf-8") as f:
        entries = f.read().split("---")
        return [e.strip() for e in entries if e.strip()]


