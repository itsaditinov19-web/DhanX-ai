import os
import pickle
import faiss

from modules.pdf_loader import load_pdfs
from modules.chunker import create_chunks
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)
print("Loading PDFs...")

documents = load_pdfs()

all_chunks = []

for doc in documents:

    chunks = create_chunks(
        doc["text"]
    )

    for chunk in chunks:

        all_chunks.append({

            "source": doc["source"],

            "text": chunk
        })

print(
    f"Total Chunks: {len(all_chunks)}"
)

texts = [

    chunk["text"]

    for chunk in all_chunks
]

print(
    "Creating embeddings..."
)

embeddings = model.encode(

    texts,

    convert_to_numpy=True
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)

index.add(
    embeddings.astype("float32")
)

os.makedirs(
    "data",
    exist_ok=True
)

faiss.write_index(
    index,
    "data/vector.index"
)

with open(
    "data/chunks.pkl",
    "wb"
) as f:

    pickle.dump(
        all_chunks,
        f
    )

print("\nSUCCESS")
print("Saved:")
print("data/vector.index")
print("data/chunks.pkl")