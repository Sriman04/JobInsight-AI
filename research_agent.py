import os
from dotenv import load_dotenv
import requests  # For API calls
import google.generativeai as genai  # For Gemini

# Load environment variables from .env file
load_dotenv()

# Get the API keys from the environment
GOOGLE_API_KEY = "AIzaSyD4wFpsHb0b64wDeOg4QXOBjIvmdZQKOJA"
GOOGLE_CSE_ID = "d639341eff9d34467"
GEMINI_API_KEY = "AIzaSyA9DQ5C21gKVYZznzwmg6GjCagip2Ua6jo"
genai.configure(api_key=GEMINI_API_KEY)

# Handle Inputs
company = input("Enter company name: ")
role = input("Enter job role: ")

# Define Search Function (Using Google Custom Search JSON API)
def search(query):
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_CSE_ID,
        'q': query,
        'num': 10  # Number of results (max 10 per request)
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('items', [])  # List of search results
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

# Fetch Data
# Company overview
overview_results = search(f"{company} company overview size domain")
news_results = search(f"{company} latest news")

# Role details
skills_results = search(f"{role} skills and experience required at {company}")
salary_results = search(f"{role} salary range at {company}")

# Summarize with Gemini
model = genai.GenerativeModel('gemini-1.5-flash')

def summarize(text, prompt):
    response = model.generate_content(f"{prompt}: {text}")
    return response.text

# Example
overview_summary = summarize(' '.join([r.get('snippet', '') for r in overview_results]), "Summarize company size, domain, and overview")
news_summary = summarize(' '.join([r.get('snippet', '') for r in news_results]), "Summarize latest news in 3 bullets")
skills_summary = summarize(' '.join([r.get('snippet', '') for r in skills_results]), "Summarize skills and experience required")
salary_summary = summarize(' '.join([r.get('snippet', '') for r in salary_results]), "Summarize salary range")

# Output the Report
print(f"## Company Overview: {company}")
print(overview_summary)
print("\n## Latest News")
print(news_summary)
print(f"\n## {role} Requirements")
print(skills_summary)
print("\n## Salary Range")
print(salary_summary)