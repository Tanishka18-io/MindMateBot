import random

# Predefined intent responses
INTENT_RESPONSES = {
    "stress": "Take a deep breath. You're doing your best.",
    "sadness": "I'm here for you. It's okay to feel sad sometimes.",
    "motivation": "You are stronger than you think. Keep going!",
    "gratitude": "That's beautiful. Gratitude fuels happiness!",
    "anxiety": "Try grounding yourself. Focus on your breath.",
    "greeting": "Hey there {name}, I'm here to support you 💙",
    "loneliness": "I'm here for you. You're valued and not alone.",
    "default": "Tell me more about how you're feeling..."
}

# ✅ ORIGINAL function (already used in your code)
def get_response_by_intent(intent):
    return INTENT_RESPONSES.get(intent, INTENT_RESPONSES["default"])

# ✅ ADD THIS FUNCTION for compatibility with app.py
def get_intent_response(intent):
    return get_response_by_intent(intent)

# Returns a random active listening line
def get_active_listening():
    responses = [
        "I hear you. You're not alone.",
        "Thanks for opening up. I'm listening.",
        "You're doing your best, and that’s enough.",
        "It's okay to feel this way. I'm here for you.",
    ]
    return random.choice(responses)

# Picks a random mindfulness or CBT tip
def get_random_tip(tips=None):
    fallback = [
        "Take a short mindful walk.",
        "Try writing down 3 things you’re grateful for.",
        "Breathe in deeply, hold, and slowly exhale.",
        "Stretch gently and unclench your jaw.",
    ]
    if tips:
        return random.choice(tips)
    return random.choice(fallback)

# Picks a random journaling prompt
def get_random_prompt(prompts=None):
    fallback = [
        "What are you feeling right now?",
        "What’s one thing that made you smile today?",
        "What’s something you wish others understood?",
        "Write a letter to your future self.",
    ]
    if prompts:
        return random.choice(prompts)
    return random.choice(fallback)

# Always shows this at the end of messages
def crisis_disclaimer():
    return "\n\n⚠️ *This is not medical advice. Please consult a professional if you're in crisis.*"
