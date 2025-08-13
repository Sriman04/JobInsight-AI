import os
from dotenv import load_dotenv
import requests
import google.generativeai as genai
import streamlit as st

# Load environment variables from .env file (optional; falls back to hardcoded if .env not used)
load_dotenv()

# Get the API keys from the environment or use hardcoded values
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', "AIzaSyD4wFpsHb0b64wDeOg4QXOBjIvmdZQKOJA")
GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID', "d639341eff9d34467")
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', "AIzaSyA9DQ5C21gKVYZznzwmg6GjCagip2Ua6jo")
genai.configure(api_key=GEMINI_API_KEY)

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
        st.error(f"Search API Error: {response.status_code} - {response.text}")
        return []

# Summarize with Gemini
model = genai.GenerativeModel('gemini-1.5-flash')

def summarize(text, prompt):
    response = model.generate_content(f"{prompt}: {text}")
    return response.text

# Streamlit App Configuration
st.set_page_config(page_title="JobInsight AI", page_icon="🔍", layout="wide")

# Custom CSS for an attractive black background and updated layout
st.markdown("""
    <style>
    /* Black gradient background with subtle pattern */
    .main {
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
        color: #ffffff; /* Default text color for visibility */
        padding-top: 0; /* Remove extra top padding */
        text-align: center; /* Center all content */
    }
    /* Input styling with fixed 300px width and centered */
    .stTextInput > div > div > input {
        background-color: #333333;
        border-radius: 8px;
        border: 1px solid #555555; /* Neutral gray border */
        padding: 12px;
        color: #ffffff;
        font-size: 16px;
        margin-bottom: 15px; /* Space between fields */
        width: 300px; /* Fixed width for each field */
        display: inline-block; /* Allow side-by-side centering */
        margin: 0 10px; /* Space between fields */
    }
    /* Button styling, centered horizontally */
    .stButton > button {
        background: linear-gradient(45deg, #4CAF50, #2E7D32);
        color: white;
        border: none;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block; /* Align with fields */
        font-size: 18px;
        margin: 10px auto 0; /* Center button */
        cursor: pointer;
        border-radius: 12px;
        box-shadow: 0 6px 15px rgba(76, 175, 80, 0.4);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #45a049, #1b5e20); /* Darker green gradient */
        color: white; /* Explicitly set text color to white on hover */
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(76, 175, 80, 0.6);
    }
    /* Typography */
    h1 {
        color: #ffffff;
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-size: 3em;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.5);
    }
    h2 {
        color: #4CAF50;
        font-family: 'Arial', sans-serif;
        font-size: 1.8em;
        border-bottom: 2px solid #a777e3;
        padding-bottom: 5px;
    }
    .stSuccess {
        background-color: rgba(76, 175, 80, 0.2);
        padding: 10px;
        border-radius: 8px;
        color: #ffffff;
        font-weight: bold;
    }
    /* Animation for fade-in effect */
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    /* Ensure text visibility */
    .stMarkdown, .stWrite {
        color: #ffffff !important;
    }
    .stWarning {
        background-color: rgba(255, 165, 0, 0.2);
        color: #ffffff;
        padding: 10px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# App Title and Description
st.title("🔍 JobInsight AI: Your Career Research Companion")
st.markdown("🌟 Enter a company and job role to unlock AI-powered insights on overview, news, requirements, and salary. Powered by Google Search & Gemini AI. 🌟")

# Input Form with No Surrounding Divs
with st.form(key="research_form"):
    company = st.text_input("Company Name", placeholder="e.g., Google", help="Enter the name of the company")
    role = st.text_input("Job Role", placeholder="e.g., Software Engineer", help="Enter the job role you’re interested in")
    submit_button = st.form_submit_button(label="Submit")

# Process and Display Results on Submit
if submit_button:
    if not company or not role:
        st.warning("Please enter both company name and job role.")
    else:
        with st.spinner("🔍 Researching... Please wait a moment."):
            # Fetch Data
            overview_results = search(f"{company} company overview size domain")
            news_results = search(f"{company} latest news")
            skills_results = search(f"{role} skills and experience required at {company}")
            salary_results = search(f"{role} salary range at {company}")

            # Summarize
            overview_summary = summarize(' '.join([r.get('snippet', '') for r in overview_results]), "Summarize company size, domain, and overview")
            news_summary = summarize(' '.join([r.get('snippet', '') for r in news_results]), "Summarize latest news in 3 bullets")
            skills_summary = summarize(' '.join([r.get('snippet', '') for r in skills_results]), "Summarize skills and experience required")
            salary_summary = summarize(' '.join([r.get('snippet', '') for r in salary_results]), "Summarize salary range")

        # Display Report without Surrounding Divs
        st.header(f"Company Overview: {company}")
        st.write(overview_summary)

        st.header("Latest News")
        st.markdown(news_summary)

        st.header(f"{role} Requirements")
        st.write(skills_summary)

        st.header("Salary Range")
        st.write(salary_summary)

        # Add Success Message and Footer
        st.success("✅ Research complete!")
        st.markdown("---")
        st.caption("🌐 Built with Streamlit | Powered by Google Search & Gemini AI | © 2025 Sriman")

# Add a note for empty results
if submit_button and not overview_results:
    st.warning("⚠️ No overview results found. Try a different query or check API limits.")