import streamlit as st
import time
import re
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

# ================= PAGE =================
st.set_page_config(page_title="Resume Analyzer", page_icon="📄")

# ================= NAVBAR =================
st.markdown("""
<style>

.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    height: 55px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    display: flex;
    align-items: center;
    padding-left: 20px;
    color: white;
    font-size: 17px;
    font-weight: 500;
    z-index: 9999;
}

.block-container {
    padding-top: 80px !important;
}

 /* USER MESSAGE RIGHT */
[data-testid="stChatMessage"]:has(div[aria-label="user avatar"]) {
    flex-direction: row-reverse;
    text-align: right;
}


/* CARDS */
.card {
    padding: 30px;
    border-radius: 22px;
    height: 230px;
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0px 12px 30px rgba(0,0,0,0.1);
}

.card-title {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 12px;
}

.card-desc {
    font-size: 14px;
    color: #555;
    line-height: 1.6;
}

.left {
    background: linear-gradient(135deg, #eef2ff, #e0e7ff);
}

.right {
    background: linear-gradient(135deg, #fef3c7, #fde68a);

/* CENTER UPLOAD */
.center-upload {
    display: flex;
    justify-content: center;
}

</style>

<div class="navbar">
📄 Resume Analyzer
</div>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<h2 style='text-align:center;'>Resume Intelligence Platform</h2>
<p style='text-align:center; color:gray;'>
Analyze resumes and evaluate candidate-job fit using AI
</p>
""", unsafe_allow_html=True)

# ================= LLM =================
llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")

# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "db" not in st.session_state:
    st.session_state.db = None

if "mode" not in st.session_state:
    st.session_state.mode = None

# ================= DASHBOARD =================
if st.session_state.mode is None:

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📄 Resume Analysis", use_container_width=True):
            st.session_state.mode = "chat"
            st.rerun()

        st.markdown("""
        <div class="card left">
            <div class="card-title">Resume Analysis</div>
            <div class="card-desc">
                • Extract key skills and technologies<br>
                • Identify experience and projects<br>
                • Quickly understand candidate profile<br>
                • Ask questions like a recruiter
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("🎯 Job Match Evaluation", use_container_width=True):
            st.session_state.mode = "job"
            st.rerun()

        st.markdown("""
        <div class="card right">
            <div class="card-title">Job Match Evaluation</div>
            <div class="card-desc">
                • Compare resume with job description<br>
                • Detect missing skills automatically<br>
                • Get match score and insights<br>
                • Improve hiring decisions faster
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# ================= PROMPT =================
def build_prompt(context, question):
    return f"""
You are a Helpful resume analyzer.

RULES:
- Answer in bullet points
- Be concise
- Use only resume data

CRITICAL:
- If dates like "Aug 2023 – Present" exist:
    → Calculate experience duration
    → Convert to years/months
    → NEVER say 0 years

Example:
Aug 2023 – Present → ~1+ year

- Do NOT ignore dates
- Do NOT say "not mentioned" if inferable

Resume:
{context}

Question:
{question}

Answer:
"""
# ==================================================
# 📄 CHAT MODE
# ==================================================
if st.session_state.mode == "chat":

    st.subheader("Resume Analysis")

    # ===== CENTER UPLOAD =====
    st.markdown('<div class="center-upload">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    st.markdown('</div>', unsafe_allow_html=True)

    # ===== PROCESS =====
    if uploaded_file and st.session_state.db is None:

        with st.spinner("Processing..."):
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.read())

            docs = PyPDFLoader("temp.pdf").load()

            chunks = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50
            ).split_documents(docs)

            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            st.session_state.db = FAISS.from_documents(chunks, embeddings)

        st.success("Resume Analyzed Successfully ✅")

    # ===== CHAT =====
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"], unsafe_allow_html=True)

    user_input = st.chat_input("Ask about the resume...")

    if user_input and st.session_state.db:

        st.session_state.messages.append({"role": "user", "content": user_input})

            # ✅ SHOW USER MESSAGE (THIS WAS MISSING)
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            placeholder = st.empty()

            docs = st.session_state.db.as_retriever(k=8).invoke(user_input)
            context = "\n".join([d.page_content for d in docs])

            response = llm.invoke(build_prompt(context, user_input))

            response_text = response.content

            items = re.split(r"\n|•", response_text)
            clean_items = [i.replace("*", "").strip() for i in items if len(i.strip()) > 3]

            html = "<ul>"
            for item in clean_items:
                html += f"<li>{item}</li>"
            html += "</ul>"

            placeholder.markdown(html, unsafe_allow_html=True)

        st.session_state.messages.append({
            "role": "assistant",
            "content": html
        })
    # ===== BACK BUTTON (BOTTOM) =====
    if st.button("⬅ Back to Dashboard"):
        st.session_state.mode = None
        st.session_state.db = None
        st.session_state.messages = []
        st.rerun()


# ==================================================
# 🎯 JOB MODE
# ==================================================
if st.session_state.mode == "job":

    st.subheader("Job Match Evaluation")

    # ===== CENTER UPLOAD =====
    st.markdown('<div class="center-upload">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    st.markdown('</div>', unsafe_allow_html=True)

    job_desc = st.text_area("Paste Job Description")

    # ===== PROCESS =====
    if uploaded_file and st.session_state.db is None:

        with st.spinner("Processing..."):
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.read())

            docs = PyPDFLoader("temp.pdf").load()

            chunks = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50
            ).split_documents(docs)

            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            st.session_state.db = FAISS.from_documents(chunks, embeddings)

        st.success("Resume ready ✅")

    # ===== ANALYZE =====
    if st.button("Analyze") and job_desc and st.session_state.db:

        docs = st.session_state.db.as_retriever(k=6).invoke(job_desc)
        context = "\n".join([d.page_content for d in docs])

        prompt = f"""
Give bullet points:
- Match Score
- Matching Skills
- Missing Skills
- Suggestions

Resume:
{context}

Job:
{job_desc}
"""

        with st.spinner("Analyzing..."):
            response = llm.invoke(prompt)

        st.markdown(response.content)

    # ===== BACK BUTTON =====
    if st.button("⬅ Back to Dashboard"):
        st.session_state.mode = None
        st.session_state.db = None
        st.rerun()