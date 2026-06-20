from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

index = faiss.read_index(
    "data/vector.index"
)
print("Index dimension:", index.d)
print("Model dimension:", model.get_sentence_embedding_dimension())

with open(
    "data/chunks.pkl",
    "rb"
) as f:

    chunk_data = pickle.load(f)

print(
    f"Loaded {len(chunk_data)} chunks"
)


def semantic_search(
    question,
    top_k=20
):

    query_embedding = model.encode(

        [question],

        convert_to_numpy=True
    )

    distances, indices = index.search(

        query_embedding.astype(
            "float32"
        ),

        top_k
    )

    results = []

    for idx in indices[0]:

        results.append(
            chunk_data[idx]
        )

    return results