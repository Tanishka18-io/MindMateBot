import spacy
import json
import os

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Path to intent data file
INTENT_DATA_PATH = "data/intent_data.json"

# Default patterns in case file is missing or corrupted
DEFAULT_PATTERNS = {
    "sadness": ["I feel sad", "I'm down", "I'm crying", "I lost someone"],
    "anxiety": ["I'm anxious", "I'm worried", "I can't breathe", "I feel nervous"],
    "stress": ["I'm stressed", "Too much work", "I can't focus", "Overwhelmed"],
    "gratitude": ["I'm thankful", "I appreciate", "grateful for"],
    "motivation": ["I want to try", "Can I do it?", "I'm ready", "I feel hopeful"],
    "loneliness": ["I'm alone", "Nobody understands", "I feel isolated"],
    "greeting": ["hello", "hi", "hey", "good morning"]
}

# Load intent patterns from JSON file or fallback
if os.path.exists(INTENT_DATA_PATH):
    try:
        with open(INTENT_DATA_PATH, "r", encoding="utf-8") as f:
            INTENT_PATTERNS = json.load(f)
            if not INTENT_PATTERNS:
                INTENT_PATTERNS = DEFAULT_PATTERNS
    except (json.JSONDecodeError, ValueError):
        INTENT_PATTERNS = DEFAULT_PATTERNS
else:
    INTENT_PATTERNS = DEFAULT_PATTERNS

# Flatten intent patterns for matching
ALL_PHRASES = []
for intent, patterns in INTENT_PATTERNS.items():
    for phrase in patterns:
        ALL_PHRASES.append((phrase.lower(), intent))

# NLP-based simple intent matcher
def detect_intent(user_input):
    doc = nlp(user_input.lower())
    input_text = doc.text

    for pattern, intent in ALL_PHRASES:
        if pattern in input_text:
            return intent
    return "default"
