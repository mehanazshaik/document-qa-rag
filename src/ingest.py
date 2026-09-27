import os
import pymupdf


DATA_FOLDER = "data"


def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF page by page.
    """

    document = pymupdf.open(file_path)

    pages = []

    for page_number in range(len(document)):

        page = document[page_number]

        text = page.get_text()

        text = text.strip()

        if text:
            page_data = {
                "text": text,
                "source": os.path.basename(file_path),
                "page": page_number + 1
            }

            pages.append(page_data)

    document.close()

    return pages


def load_documents():

    all_pages = []

    for file_name in os.listdir(DATA_FOLDER):

        if file_name.endswith(".pdf"):

            file_path = os.path.join(DATA_FOLDER, file_name)

            pages = extract_text_from_pdf(file_path)

            all_pages.extend(pages)

    return all_pages


if __name__ == "__main__":

    documents = load_documents()

    print("=" * 60)
    print("DOCUMENT INGESTION")
    print("=" * 60)

    print("Total pages extracted:", len(documents))

    print()

    for document in documents[:5]:

        print("Source:", document["source"])
        print("Page:", document["page"])
        print("Text preview:")
        print(document["text"][:300])
        print("-" * 60)