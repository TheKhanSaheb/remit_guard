from app.graph import app_graph


if __name__ == "__main__":
    queries = [
        "What is the USD to BDT remittance rate today?",
        "Is Hundi a safe way to send money?",
        "What is the safest way to send money to Bangladesh?",
        "What documents are generally needed to send a remittance?",
    ]

    for query in queries:
        print("\n" + "=" * 70)
        print(f"USER: {query}")
        print("=" * 70)

        result = app_graph.invoke({
            "user_query": query
        })

        print(f"ROUTE: {result['route']}")
        print("\nRESPONSE:")
        print(result["final_response"])