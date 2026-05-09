import faiss
import pickle
import numpy as np

from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)

# Load FAISS index
index = faiss.read_index(
    "embeddings/faiss.index"
)

# Load metadata
with open(
    "embeddings/metadata.pkl",
    "rb"
) as f:

    metadata = pickle.load(f)


def retrieve_assessments(
    query,
    analysis,
    top_k=10
):

    # Convert query to embedding
    query_embedding = model.encode([query])

    # Search FAISS
    distances, indices = index.search(
        np.array(query_embedding),
        top_k
    )

    scored_results = []

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        item = metadata[idx]

        # Ignore weak matches
        if distance > 2.0:
            continue

        bonus = 0

        # Keyword overlap scoring
        for skill in item["skills"]:

            if skill.lower() in query.lower():
                bonus += 1

        # Technical preference
        if (
            analysis["needs_coding"]
            and item["test_type"] == "K"
        ):
            bonus += 2

        # Personality preference
        if (
            analysis["needs_personality"]
            and item["test_type"] == "P"
        ):
            bonus += 2

        # Final ranking score
        final_score = (
            float(distance) - bonus
        )

        scored_results.append(
            (final_score, item)
        )

    # Sort by best score
    scored_results.sort(
        key=lambda x: x[0]
    )

    final_results = []

    added_names = set()

    for score, item in scored_results:

        # Avoid duplicates
        if item["name"] in added_names:
            continue

        added_names.add(
            item["name"]
        )

        final_results.append(item)

    return final_results[:5]