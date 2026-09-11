from app.agents.rate_agent import run_rate_agent


if __name__ == "__main__":
    query = "USD to BDT remittance rate via bKash today"

    print("\n" + "=" * 60)
    print("                 REMITGUARD")
    print("            Rate Comparator Agent")
    print("=" * 60)

    print(f"\n🔎 Query: {query}")
    print("\n⏳ Searching for latest exchange rates...\n")

    result = run_rate_agent(query)

    print("-" * 60)
    print("💱 LATEST REMITTANCE RATE")
    print("-" * 60)

    print(result)

    print("\n" + "=" * 60)
    print("                 END RESULT")
    print("=" * 60)