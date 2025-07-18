import io
import streamlit as st
import chardet
import PyPDF2
from resume_matcher import rank_resume

st.title("📄 Resume Ranker App")
st.write("Upload your resume and job description (TXT or PDF) to see the relevance score.")

def read_uploaded_file(uploaded_file):
    """Return text from a Streamlit UploadedFile (TXT or PDF)."""
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        text = "".join(page.extract_text() or "" for page in reader.pages)
        return text

    # Treat everything else as raw bytes, then detect encoding
    raw = uploaded_file.getvalue()
    enc = chardet.detect(raw)["encoding"] or "utf-8"
    return raw.decode(enc, errors="ignore")

resume = st.file_uploader("📄 Upload Resume", type=["txt", "pdf"])
jd      = st.file_uploader("📝 Upload Job Description", type=["txt", "pdf"])

if resume and jd:
    resume_text = read_uploaded_file(resume)
    jd_text     = read_uploaded_file(jd)

    score, matched_keywords, suggestions = rank_resume(resume_text, jd_text)

    st.metric("Relevance Score", f"{score:.1f}%")
    st.subheader("✅ Matched Keywords")
    st.write(", ".join(matched_keywords) if matched_keywords else "—")

    st.subheader("💡 Suggestions")
    st.write(suggestions or "No suggestions – great match! 🎉")
