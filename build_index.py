import json
import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)

# Load catalog
with open("data/shl_catalog.json", "r") as f:
    catalog = json.load(f)

texts = []

for item in catalog:

    text = (
        item["name"] + " " +
        item["description"] + " " +
        " ".join(item["skills"])
    )

    texts.append(text)

# Create embeddings
embeddings = model.encode(texts)

# FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(
    np.array(embeddings)
)

# Save index
faiss.write_index(
    index,
    "embeddings/faiss.index"
)

# Save metadata
with open(
    "embeddings/metadata.pkl",
    "wb"
) as f:

    pickle.dump(catalog, f)

print("FAISS index created successfully.")