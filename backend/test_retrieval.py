from app.tools.vectorstore_tool import retrieve_relevant_chunks


questions = [
    "What is hundi?",
    "What laws in Bangladesh address money laundering?",
    "What are the risks associated with Hundi or Hawala?",
]


if __name__ == "__main__":
    for question in questions:
        print("\n" + "=" * 80)
        print("QUESTION:", question)
        print("=" * 80)

        result = retrieve_relevant_chunks(question, k=4)

        print(result)