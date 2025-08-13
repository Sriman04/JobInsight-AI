# JobInsight AI

Welcome to **JobInsight AI**, a Streamlit-based application designed to provide AI-powered insights about companies and job roles. This tool leverages Google Custom Search API and Gemini AI to fetch and summarize data on company overviews, latest news, job requirements, and salary ranges.

## Overview

This project was developed to assist users in researching career opportunities by integrating web search capabilities with AI-driven summarization. The application allows users to input a company name and job role to receive detailed insights.

## API Keys Used

The application relies on the following APIs, each requiring an API key:

- **Google Custom Search JSON API**: Used to fetch web search results (e.g., company overviews, news, skills, and salary data). You need to obtain an API key and a Custom Search Engine (CSE) ID from the [Google Cloud Console](https://console.cloud.google.com/).
- **Google Gemini API**: Used for summarizing search results into concise insights. An API key is required, obtainable from the [Google AI Studio](https://aistudio.google.com/).

### Notes on API Keys
- API keys are stored in a `.env` file locally (e.g., `GOOGLE_API_KEY`, `GOOGLE_CSE_ID`, `GEMINI_API_KEY`) but are excluded from this repository via `.gitignore` for security.
- To use the app, you must generate your own API keys and configure them as described in the "Local Deployment" section.

## Development Process

1. **Setup Environment**:
   - Installed Python and set up a virtual environment.
   - Installed required libraries: `streamlit`, `requests`, `google-generativeai`, and `python-dotenv`.

2. **Code Development**:
   - Created `app.py` to build the Streamlit interface.
   - Implemented a search function using the Google Custom Search API.
   - Integrated Gemini AI for summarization.
   - Added custom CSS for a visually appealing black gradient background.

3. **Testing**:
   - Tested locally with sample inputs (e.g., "Google" and "Software Engineer").
   - Verified API responses and summarization output.

4. **Deployment to GitHub**:
   - Initialized a Git repository locally.
   - Committed files and pushed to GitHub using Git commands.

## Local Deployment

To run this project locally, follow these steps:

### Prerequisites
- Python 3.8 or higher.
- Git installed (download from [git-scm.com](https://git-scm.com/)).
- A GitHub account and a personal access token (create at [github.com/settings/tokens](https://github.com/settings/tokens) with "repo" scope).

### Steps

1. **Clone the Repository**
   Clone this repository to your local machine:
   git clone https://github.com/yourusername/ResearchAgent.git
   cd ResearchAgent


2. **Create a Virtual Environment (Optional but Recommended)**
   Set up a virtual environment:
   On Windows (CMD):
   python -m venv venv
   venv\Scripts\activate

   - On Mac/Linux:
  python3 -m venv venv
  source venv/bin/activate

  
3. **Install Dependencies**
   Install the required Python packages:
   pip install streamlit requests google-generativeai python-dotenv


4. **Configure API Keys**
- Create a `.env` file in the project directory.
- Add your API keys in the following format:
  GOOGLE_API_KEY=your_google_api_key
  GOOGLE_CSE_ID=your_cse_id
  GEMINI_API_KEY=your_gemini_api_key

- Obtain these keys from the Google Cloud Console and Google AI Studio, respectively.

5. **Run the Application**
  Launch the Streamlit app:
  streamlit run app.py

- Open your browser and go to `http://localhost:8501` to use the app.

### Troubleshooting
- **API Errors**: Ensure your API keys are valid and have sufficient quotas.
- **Module Not Found**: Verify all dependencies are installed.
- **Port Conflict**: If `localhost:8501` is unavailable, change the port with `streamlit run app.py --server.port 8502`.

## Contributing
Feel free to fork this repository, submit issues, or create pull requests to improve the project.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (create one if desired).

## Acknowledgements
- Built with [Streamlit](https://streamlit.io/).
- Powered by [Google Custom Search API](https://developers.google.com/custom-search/v1/overview) and [Gemini AI](https://ai.google.dev/).
- Thanks to the open-source community for tools and inspiration.
