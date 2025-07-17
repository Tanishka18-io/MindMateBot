import google.generativeai as genai

# 🔐 Use your actual API key here
genai.configure(api_key="key")

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("How can I manage stress better?")
print(response.text)
