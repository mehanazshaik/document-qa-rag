from retriever import retrieve_documents
from generator import generate_answer


def main():

    print("=" * 60)
    print("DOCUMENT Q&A BOT")
    print("=" * 60)

    print("Type 'exit' to stop.")
    print()

    while True:

        question = input("Ask a question: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if question.strip() == "":
            print("Please enter a question.")
            print()
            continue

        print()
        print("Searching documents...")

        results = retrieve_documents(question, top_k=5)

        print("Generating answer...")

        answer = generate_answer(question, results)

        print()
        print("=" * 60)
        print("ANSWER")
        print("=" * 60)
        print(answer)

        print()
        print("=" * 60)
        print("RETRIEVED SOURCES")
        print("=" * 60)

        for result in results:
            print(
                f"- {result['source']}, "
                f"Page {result['page']}, "
                f"Score {result['score']:.4f}"
            )

        print()


if __name__ == "__main__":
    main()