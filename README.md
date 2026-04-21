# Cold Email Generator AI ✉️

An intelligent, AI-powered Streamlit web application that instantly scrapes job postings, extracts the role and required skills, matches them against your own portfolio, and generates personalized, professional cold outreach emails.

## 🚀 Key Features

*   **🌐 Instant Scraping:** Paste any job posting URL (Lever, Greenhouse, etc.) and seamlessly extract all details.
*   **🤖 AI Data Extraction:** Powered by LLaMA 3 (via Groq API), it intelligently identifies the Job Role, Experience required, and Technical Skills.
*   **🧩 Vector Portfolio Matching:** Uses **ChromaDB** to compare the required job skills with your own personal projects (from a CSV file) and injects the top-tier, relevant links directly into the pitch.
*   **🎨 Premium UI:** Full dark-mode UI redesign rendering an immersive, sleek user experience, complete with dynamic progress steps and clipboard features.
*   **🧑‍💼 Dynamic Profiles:** Inject your own custom Name, Job Role, and Company directly from the side panel layout. 

## ⚙️ Tech Stack

*   **Frontend:** Streamlit 
*   **LLM Provider:** Groq (LLaMA 3)
*   **Orchestration:** LangChain
*   **Vector Database:** ChromaDB
*   **Dependency Management:** Pipenv

## 📂 Project Setup

1. **Install Dependencies:**
   Ensure you have Python 3.10+ installed. Install the pipenv dependencies:
   ```bash
   pipenv install
   ```

2. **Add Your API Key:**
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   USER_AGENT="cold-email-generator/1.0"
   ```

3. **Customize Portfolio (Optional):**
   Update `sample_portfolio.csv` with your personal projects, tech skills, and GitHub/Portfolio links.

4. **Launch the App:**
   ```bash
   pipenv run streamlit run main.py
   ```

## ⚠️ Notes 
- The very first time you launch the app locally, ChromaDB will automatically download an 80MB embedding model. All future runs will be instant!
- If a URL fails to scrape, the site may be employing anti-bot technologies (e.g., standard LinkedIn/Indeed endpoints). Testing works flawlessly on direct career ATS platforms (Greenhouse, Lever) or smaller boards.
