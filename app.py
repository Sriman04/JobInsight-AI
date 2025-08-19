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
        color: #ffffff;
        padding-top: 0;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    /* Container for the form with reduced width */
    .stForm {
        max-width: 500px !important;
        margin: 0 auto !important;
        background-color: rgba(45, 45, 45, 0.8);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    
    /* Remove all borders and outlines from input fields */
    .stTextInput > div {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }
    
    .stTextInput > div > div {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #333333 !important;
        border-radius: 8px !important;
        border: 1px solid #555555 !important;
        padding: 12px !important;
        color: #ffffff !important;
        font-size: 16px !important;
        margin-bottom: 15px !important;
        width: 100% !important;
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Remove focus outline and red border */
    .stTextInput > div > div > input:focus {
        border: 1px solid #4CAF50 !important;
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.3) !important;
    }
    
    .stTextInput > div > div > input:focus-visible {
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.3) !important;
    }
    
    /* Remove any red outline/border on focus */
    .stTextInput div[data-testid="stTextInput"] > div {
        border: none !important;
        outline: none !important;
    }
    
    .stTextInput div[data-testid="stTextInput"]:focus-within {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Button styling, centered horizontally */
    .stButton > button {
        background: linear-gradient(45deg, #4CAF50, #2E7D32) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        text-align: center !important;
        text-decoration: none !important;
        display: block !important;
        font-size: 18px !important;
        margin: 20px auto 0 !important;
        cursor: pointer !important;
        border-radius: 12px !important;
        box-shadow: 0 6px 15px rgba(76, 175, 80, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 150px !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #45a049, #1b5e20) !important;
        color: white !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(76, 175, 80, 0.6) !important;
    }
    
    /* Import Montserrat font */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800&display=swap');
    
    /* Typography */
    h1 {
        color: #ffffff;
        text-align: center;
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        font-size: 3em;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    
    h2 {
        color: #4CAF50;
        font-family: 'Arial', sans-serif;
        font-size: 1.8em;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 5px;
    }
    
    .stSuccess {
        background-color: rgba(76, 175, 80, 0.2);
        padding: 10px;
        border-radius: 8px;
        color: #ffffff;
        font-weight: bold;
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
    
    /* Center the main content */
    .block-container {
        max-width: 800px;
        margin: 0 auto;
        padding-top: 2rem;
    }
    
    /* Input labels styling */
    .stTextInput label {
        color: #ffffff !important;
        font-weight: 500 !important;
        margin-bottom: 5px !important;
    }
    </style>
""", unsafe_allow_html=True)

# App Title and Description
st.title("JobInsight AI: Your Career Research Companion")
st.markdown("Enter a company and job role to unlock AI-powered insights on overview, news, requirements, and salary. Powered by Google Search & Gemini AI")

# Input Form with centered layout
with st.form(key="research_form"):
    company = st.text_input("Company Name", placeholder="e.g., Google", help="Enter the name of the company")
    role = st.text_input("Job Role", placeholder="e.g., Software Engineer", help="Enter the job role you're interested in")
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

        # Display Report
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
