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
