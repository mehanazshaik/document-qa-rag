from vector_store import build_vector_store


def main():
    print("=" * 60)
    print("DOCUMENT INDEXING")
    print("=" * 60)

    print()
    print("Starting document indexing...")
    print()

    build_vector_store()

    print()
    print("Indexing completed successfully.")
    print("The vector store is ready for querying.")


if __name__ == "__main__":
    main()