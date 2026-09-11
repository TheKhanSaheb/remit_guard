from app.llm import fallback_llm


if __name__ == "__main__":
    response = fallback_llm.invoke(
        "In one short paragraph, explain what international remittance means."
    )

    print("\nGROQ TEST RESPONSE:\n")
    print(response.content)