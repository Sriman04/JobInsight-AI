import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', "AIzaSyA9DQ5C21gKVYZznzwmg6GjCagip2Ua6jo")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model and generate content
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Summarize AI in a few words")
print(response.text)