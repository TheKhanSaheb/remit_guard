def aggregate_response(state: dict) -> dict:
    result = (
        state.get("rate_result")
        or state.get("scam_result")
        or state.get("channel_result")
        or state.get("general_result")
    )

    if not result:
        return {
            "summary": "No response was generated.",
            "recommendation": "",
            "safety_warnings": [],
            "what_to_verify": [],
            "sources": [],
        }

    # Extract source URLs mentioned by the agent
    sources = []

    for line in result.splitlines():
        if "http://" in line or "https://" in line:
            parts = line.split("http", 1)

            if len(parts) == 2:
                url = "http" + parts[1].strip()

                if url.startswith("http"):
                    sources.append(url)

    # Remove duplicate sources
    sources = list(dict.fromkeys(sources))

    return {
        "summary": result,
        "recommendation": (
            "Verify the final rate, fees, recipient amount, "
            "and legality before sending money."
        ),
        "safety_warnings": [
            "Do not send money through unknown or unauthorized intermediaries.",
            "Do not share OTPs, passwords, or sensitive account credentials.",
        ],
        "what_to_verify": [
            "Exchange rate",
            "Transaction fees",
            "Final recipient amount",
            "Legitimate remittance channel",
        ],
        "sources": sources,
    }