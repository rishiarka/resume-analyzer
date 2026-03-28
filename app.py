import streamlit as st
import PyPDF2
import re

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }
    .stTextArea textarea {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.title("🧠 Resume Analyzer")
st.caption("Instantly evaluate how well your resume matches a job role")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
job_desc = st.text_area("Paste Job Description")

def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

def analyze_resume(resume_text, job_desc):
    resume_words = set(re.findall(r'\w+', resume_text.lower()))
    job_words = set(re.findall(r'\w+', job_desc.lower()))

    common = resume_words.intersection(job_words)

    score = int((len(common) / len(job_words)) * 100) if job_words else 0
    missing = job_words - resume_words

    return score, list(common), list(missing)

if uploaded_file and job_desc:
    if st.button("Analyze Resume"):
        with st.spinner("Analyzing..."):
            resume_text = extract_text(uploaded_file)

            score, matched, missing = analyze_resume(resume_text, job_desc)

            st.subheader("📊 Match Score")
            st.progress(score / 100)

            if score > 75:
                st.success(f"🔥 Strong Match: {score}%")
            elif score > 50:
                st.warning(f"⚠️ Average Match: {score}%")
            else:
                st.error(f"❌ Weak Match: {score}%")

            st.subheader("✅ Matched Skills")
            st.write(" ".join([f"`{word}`" for word in matched[:15]]))

            st.subheader("❌ Missing Skills")
            st.write(" ".join([f"`{word}`" for word in missing[:15]]))

            st.info("Tip: Add missing keywords to improve your resume.")