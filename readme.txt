📄 AI Resume Analyzer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧠 Overview
An intelligent Resume Analysis and Job Matching platform built using Streamlit, 
LangChain, FAISS, and LLMs.

This application allows users and recruiters to:
  • Analyze resumes conversationally
  • Extract key insights instantly
  • Evaluate candidate-job fit efficiently


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 Features

📄 Resume Analysis (Chat-Based)
  • Upload a resume (PDF)
  • Ask questions like:
      - What are the candidate’s skills?
      - What is the experience?
      - Has the candidate done internships?
  • Get structured bullet-point answers
  • ChatGPT-style interface

🎯 Job Match Evaluation
  • Paste job description
  • Get:
      - Match Score
      - Matching Skills
      - Missing Skills
      - Suggestions to improve


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧠 How It Works (RAG Pipeline)

  PDF → Text → Chunking → Embeddings → FAISS Vector DB
                         ↓
              User Query → Similarity Search
                         ↓
                  Relevant Context
                         ↓
                    LLM (Groq)
                         ↓
                      Answer


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🛠️ Tech Stack

  • Frontend      → Streamlit
  • Framework     → LangChain
  • LLM           → Groq (LLaMA models)
  • Vector DB     → FAISS
  • Embeddings    → HuggingFace
  • PDF Parsing   → PyPDF


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📂 Project Structure

  resume-analyzer/
  │
  ├── app.py
  ├── requirements.txt
  ├── .gitignore
  └── .env   (local only)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️ Setup Instructions

1️⃣ Clone the repository
    git clone https://github.com/your-username/Resume-Analyser.git

2️⃣ Create virtual environment
    python -m venv venv
    venv\Scripts\activate

3️⃣ Install dependencies
    pip install -r requirements.txt

4️⃣ Add API key in .env
    GROQ_API_KEY=your_key_here

5️⃣ Run the app
    streamlit run app.py


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 Deployment

  • Streamlit Community Cloud (recommended)
  • Render / AWS (advanced)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Use Cases

  • 👨‍💼 Recruiters → Quick resume screening
  • 👩‍🎓 Students → Improve resumes
  • 🧠 HR Teams → Automate hiring workflow
  • 📊 Job Matching → Evaluate candidate fit


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 Future Improvements

  • Experience calculation (months + years)
  • Resume scoring system
  • Multi-resume comparison
  • Export report (PDF)
  • User authentication


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧑‍💻 Author

  Sushmita Dutta


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⭐ If you like this project, give it a star!


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 Interview One-Liner

"I built a Resume Analyzer using a RAG pipeline where resumes are converted 
into embeddings, stored in FAISS, and queried using similarity search. 
An LLM then generates structured responses based on retrieved context."