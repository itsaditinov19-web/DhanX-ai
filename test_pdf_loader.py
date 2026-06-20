from modules.pdf_loader import load_pdfs

docs = load_pdfs()

print("Total PDFs loaded:", len(docs))

for doc in docs:

    print(
        doc["source"],
        len(doc["text"])
    )