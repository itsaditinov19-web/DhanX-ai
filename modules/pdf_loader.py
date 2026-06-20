import fitz
import os


def load_pdfs(pdf_folder="pdfs"):

    documents = []

    for filename in os.listdir(pdf_folder):

        if filename.endswith(".pdf"):

            path = os.path.join(
                pdf_folder,
                filename
            )

            try:

                print(f"Loading {filename}...")

                doc = fitz.open(path)

                print(f"Pages: {len(doc)}")

                text = ""

                for page in doc:

                    page_text = page.get_text()

                    if page_text:

                        text += page_text + "\n"

                documents.append(
                    {
                        "source": filename,
                        "text": text
                    }
                )

            except Exception as e:

                print(
                    f"Error reading {filename}: {e}"
                )

    return documents