import streamlit as st
from resume_matcher import rank_resume

st.title("📄 Resume Ranker App")
st.write("Upload your resume and job description to get a relevance score.")

resume = st.file_uploader("Upload Resume", type=["txt", "pdf"])
jd = st.file_uploader("Upload Job Description", type=["txt", "pdf"])

if resume and jd:
    resume_text = resume.read().decode("utf-8")
    jd_text = jd.read().decode("utf-8")
    
    score, matched_keywords, suggestions = rank_resume(resume_text, jd_text)
    
    st.metric(label="Relevance Score", value=f"{score}%")
    st.subheader("✅ Matched Keywords")
    st.write(matched_keywords)
    
    st.subheader("🛠️ Suggestions")
    st.write(suggestions)
