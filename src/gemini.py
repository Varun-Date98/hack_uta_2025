import json
import google.generativeai as genai


with open("./secrets.json") as f:
    secrets = json.load(f)

genai.configure(api_key=secrets["gemini-api-key"])
# print(list(genai.list_models()))

model = genai.GenerativeModel("gemini-1.5-pro")
response = model.generate_content("Give sentiment of this text 'I love New York!'")
print(response.text)