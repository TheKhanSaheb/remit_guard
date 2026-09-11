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

    return {
        "summary": result,
        "recommendation": "",
        "safety_warnings": [],
        "what_to_verify": [],
        "sources": [],
    }