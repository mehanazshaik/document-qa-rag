from ingest import load_documents


CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def create_chunks(documents):

    all_chunks = []

    chunk_id = 0

    for document in documents:

        words = document["text"].split()

        start = 0

        while start < len(words):

            end = start + CHUNK_SIZE

            chunk_words = words[start:end]

            chunk_text = " ".join(chunk_words)

            chunk = {
                "chunk_id": chunk_id,
                "text": chunk_text,
                "source": document["source"],
                "page": document["page"]
            }

            all_chunks.append(chunk)

            chunk_id = chunk_id + 1

            start = start + (CHUNK_SIZE - CHUNK_OVERLAP)

    return all_chunks


if __name__ == "__main__":

    documents = load_documents()

    chunks = create_chunks(documents)

    print("=" * 60)
    print("CHUNKING")
    print("=" * 60)

    print("Total pages:", len(documents))
    print("Total chunks:", len(chunks))

    print()

    for chunk in chunks[:5]:

        print("Chunk ID:", chunk["chunk_id"])
        print("Source:", chunk["source"])
        print("Page:", chunk["page"])
        print("Number of words:", len(chunk["text"].split()))

        print("Text preview:")
        print(chunk["text"][:300])

        print("-" * 60)