import os
import pickle
import faiss

from ingest import load_documents
from chunker import create_chunks
from embedder import create_embeddings


VECTOR_STORE_FOLDER = "vector_store"
INDEX_FILE = os.path.join(VECTOR_STORE_FOLDER, "index.faiss")
METADATA_FILE = os.path.join(VECTOR_STORE_FOLDER, "metadata.pkl")


def build_vector_store():
    print("Loading documents...")

    documents = load_documents()

    print("Creating chunks...")

    chunks = create_chunks(documents)

    print("Creating embeddings...")

    embeddings = create_embeddings(chunks)

    print("Creating FAISS index...")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    os.makedirs(VECTOR_STORE_FOLDER, exist_ok=True)

    faiss.write_index(index, INDEX_FILE)

    with open(METADATA_FILE, "wb") as file:
        pickle.dump(chunks, file)

    print()
    print("=" * 60)
    print("VECTOR STORE CREATED")
    print("=" * 60)

    print("Total chunks:", len(chunks))
    print("Embedding dimension:", dimension)
    print("FAISS vectors:", index.ntotal)

    print()
    print("Index saved to:", INDEX_FILE)
    print("Metadata saved to:", METADATA_FILE)

    print("=" * 60)


if __name__ == "__main__":
    build_vector_store()