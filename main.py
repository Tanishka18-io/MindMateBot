# main.py

from responses import get_empathetic_reply, get_active_listening, crisis_disclaimer
from utils import load_json, get_random_tip, get_random_prompt, save_mood

# Load CBT tips and journaling prompts from JSON files
tips = load_json("data/cbt_tips.json")
prompts = load_json("data/prompts.json")

print("🧠 MindMate – Your Offline Mental Wellness Companion")
print("Type 'exit' to end the chat.")
print("You can log your mood anytime using: mood: happy | mood: anxious | etc.\n")

message_count = 0  # to track when to show journaling prompt

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("MindMate: Take care of yourself. Remember, you are never alone.")
        break

    # Mood logging (e.g., mood: sad)
    if user_input.lower().startswith("mood:"):
        mood = user_input.split(":", 1)[-1].strip()
        if mood:
            save_mood(mood)
            print("MindMate: Thanks for sharing. I've saved your mood for today.")
        else:
            print("MindMate: Please specify your mood after 'mood:'.")
        continue

    # 1. Get response based on emotion keywords
    reply = get_empathetic_reply(user_input)

    # 2. Get active listening phrase
    listening = get_active_listening()

    # 3. Pick a random CBT tip
    tip = get_random_tip(tips)

    # 4. Crisis disclaimer
    disclaimer = crisis_disclaimer()

    # Print the response
    print("\nMindMate:", reply)
    print("MindMate:", listening)
    print("MindMate Tip:", tip)
    print(disclaimer)

    # 5. Journaling prompt every 3 messages
    message_count += 1
    if message_count % 3 == 0:
        prompt = get_random_prompt(prompts)
        print("\n📝 Journaling Prompt:", prompt)
