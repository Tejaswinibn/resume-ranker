import nltk

# Automatically download NLTK data if not present
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')  # if you're using WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def clean_text(text):
    return re.sub(r"[^a-zA-Z0-9 ]", "", text.lower())

def rank_resume(resume_text, jd_text):
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_clean, jd_clean])

    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    percentage = round(score * 100, 2)

    resume_tokens = set(resume_clean.split()) - stop_words
    jd_tokens = set(jd_clean.split()) - stop_words
    matched = resume_tokens.intersection(jd_tokens)
    suggestions = jd_tokens - resume_tokens

    return percentage, list(matched), list(suggestions)[:10]
