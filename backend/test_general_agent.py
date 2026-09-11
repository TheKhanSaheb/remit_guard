from app.agents.general_agent import run_general_agent


if __name__ == "__main__":
    query = "What documents are generally needed to send a remittance?"

    result = run_general_agent(query)

    print("\nGENERAL AGENT RESPONSE:\n")
    print(result)