# mcp_server/tools/job_matcher.py

import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
    return text.lower().strip()


def match_resume_to_job(job_description: str, resume_rows: list):
    try:
        # Convert incoming resume list into DataFrame
        df = pd.DataFrame(resume_rows)
        if df.empty or "content" not in df.columns:
            return {"error": "Invalid or missing resume content."}

        # Clean text for each block
        job_desc_clean = clean_text(job_description)
        df["cleaned"] = df["content"].apply(clean_text)

        # Build combined TF-IDF matrix
        all_text = [job_desc_clean] + df["cleaned"].tolist()
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_text)

        # Calculate cosine similarity between job and each resume block
        job_vec = tfidf_matrix[0:1]
        resume_vecs = tfidf_matrix[1:]
        similarities = cosine_similarity(job_vec, resume_vecs).flatten()

        # Add scores and return top-matching rows
        df["score"] = similarities
        df_sorted = df.sort_values(by="score", ascending=False)
        top_matches = df_sorted[df_sorted["score"] > 0.05].drop(columns=["cleaned"]).to_dict(orient="records")

        return {"matches": top_matches}

    except Exception as e:
        return {"error": str(e)}