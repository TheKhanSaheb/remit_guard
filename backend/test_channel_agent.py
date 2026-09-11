from app.agents.channel_agent import run_channel_agent


if __name__ == "__main__":
    query = "What is the safest way to send money to Bangladesh?"

    result = run_channel_agent(query)

    print("\nCHANNEL AGENT RESPONSE:\n")
    print(result)