from app.agents.scam_agent import run_scam_agent


if __name__ == "__main__":
    query = "Is an unofficial Hundi agent safe for sending money to Bangladesh?"

    result = run_scam_agent(query)

    print("\nSCAM AGENT RESPONSE:\n")
    print(result)