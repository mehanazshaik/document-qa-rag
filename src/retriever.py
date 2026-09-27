import os
import pickle
import faiss

from sentence_transformers import SentenceTransformer

VECTOR_STORE_FOLDER = "vector_store"
INDEX_FILE = os.path.join(VECTOR_STORE_FOLDER, "index.faiss")
METADATA_FILE = os.path.join(VECTOR_STORE_FOLDER, "metadata.pkl")

MODEL_NAME = "all-MiniLM-L6-v2"
DEFAULT_TOP_K = 5

print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)
print("Embedding model loaded.")


def load_vector_store():
    index = faiss.read_index(INDEX_FILE)

    with open(METADATA_FILE, "rb") as file:
        chunks = pickle.load(file)

    return index, chunks


def retrieve_documents(question, top_k=DEFAULT_TOP_K):

    index, chunks = load_vector_store()

    question_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    scores, indices = index.search(question_embedding, top_k)

    results = []

    for i in range(len(indices[0])):

        chunk_index = indices[0][i]

        result = {
            "score": float(scores[0][i]),
            "text": chunks[chunk_index]["text"],
            "source": chunks[chunk_index]["source"],
            "page": chunks[chunk_index]["page"],
            "chunk_id": chunks[chunk_index]["chunk_id"]
        }

        results.append(result)

    return results


if __name__ == "__main__":

    question = input("Enter your question: ")

    results = retrieve_documents(question, top_k=5)

    print()
    print("=" * 60)
    print("RETRIEVED DOCUMENTS")
    print("=" * 60)

    for number, result in enumerate(results, start=1):

        print()
        print("Result:", number)
        print("Score:", round(result["score"], 4))
        print("Source:", result["source"])
        print("Page:", result["page"])
        print("Chunk ID:", result["chunk_id"])

        print()
        print("Text:")
        print(result["text"][:500])

        print("-" * 60)
