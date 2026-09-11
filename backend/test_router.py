from app.agents.router_agent import classify_intent


if __name__ == "__main__":
    queries = [
        "What is the USD to BDT remittance rate today?",
        "Is this remittance agent a scam?",
        "What is the safest way to send money to Bangladesh?",
        "What documents do I need for remittance?"
    ]

    for query in queries:
        result = classify_intent(query)

        print(f"Query: {query}")
        print(f"Route: {result}")
        print("-" * 50)