import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load catalog
with open("data/shl_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Create searchable text
texts = []

for item in catalog:
    combined = (
        item.get("name", "") + " " +
        item.get("description", "") + " " +
        " ".join(item.get("skills", []))
    )
    texts.append(combined)

# TF-IDF vectorizer
vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(texts)

def retrieve_assessments(query, top_k=5):

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(query_vector, X)[0]

    ranked_indices = similarities.argsort()[::-1]

    results = []

    for idx in ranked_indices[:top_k]:
        item = catalog[idx]

        results.append({
            "name": item.get("name"),
            "url": item.get("url"),
            "test_type": item.get("test_type")
        })

    return results