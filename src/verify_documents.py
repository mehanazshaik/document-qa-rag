import fitz
import os


DATA_FOLDER = "data"


def count_words(text):
    words = text.split()
    return len(words)


def verify_documents():

    print("=" * 60)
    print("DOCUMENT VERIFICATION")
    print("=" * 60)

    files = os.listdir(DATA_FOLDER)

    pdf_files = []

    for file in files:
        if file.endswith(".pdf"):
            pdf_files.append(file)

    if len(pdf_files) == 0:
        print("No PDF files found.")
        return

    for file in pdf_files:

        file_path = os.path.join(DATA_FOLDER, file)

        document = fitz.open(file_path)

        total_words = 0

        for page in document:

            text = page.get_text()

            total_words = total_words + count_words(text)

        page_count = len(document)

        print()
        print("File:", file)
        print("Pages:", page_count)
        print("Words:", total_words)

        if page_count >= 2 or total_words >= 500:
            print("Status: PASS")
        else:
            print("Status: CHECK")

        document.close()

    print()
    print("=" * 60)
    print("Verification completed.")
    print("=" * 60)


if __name__ == "__main__":
    verify_documents()