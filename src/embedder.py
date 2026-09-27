from sentence_transformers import SentenceTransformer
from ingest import load_documents
from chunker import create_chunks

MODEL_NAME = "all-MiniLM-L6-v2"


def create_embeddings(chunks):
    model = SentenceTransformer(MODEL_NAME)

    texts = []

    for chunk in chunks:
        texts.append(chunk["text"])

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings


if __name__ == "__main__":
    documents = load_documents()
    chunks = create_chunks(documents)

    print("=" * 60)
    print("EMBEDDING GENERATION")
    print("=" * 60)

    print("Total chunks:", len(chunks))
    print("Loading embedding model...")

    embeddings = create_embeddings(chunks)

    print()
    print("Embedding generation completed.")
    print("Number of embeddings:", len(embeddings))
    print("Embedding dimension:", embeddings.shape[1])
    print("Embedding shape:", embeddings.shape)

    print()
    print("First embedding preview:")
    print(embeddings[0][:10])

    print("=" * 60)