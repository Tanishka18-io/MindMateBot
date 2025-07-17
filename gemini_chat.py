import google.generativeai as genai

# 🔐 Use your actual API key here
genai.configure(api_key="AIzaSyCbdrPBd7tm7hrsC_nkqM8Rd7ud1_D1F98")

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("How can I manage stress better?")
print(response.text)
