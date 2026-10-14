from app.schemas import GymScenario, GymChoice

_SCENARIOS = [
    {
        "id": "collect-request",
        "title": "A collect request disguised as receiving money",
        "description": "A stranger says they are sending you ₹2,000. A UPI notification appears asking you to approve a collect request and enter your UPI PIN to receive it.",
        "category": "upi_collect_request",
        "choices": [
            {"id": "approve", "text": "Approve the request and enter my PIN to receive the money."},
            {"id": "decline", "text": "Decline it. A collect request can take money from me; I will verify independently."},
            {"id": "share_pin", "text": "Send the PIN to the person so they can complete the transfer."},
        ],
        "correct_choice": "decline",
        "feedback": "A collect request is a request for you to pay; do not approve it just to receive money.",
        "safe_action": "Decline the unexpected request and check your official payment app directly.",
    },
    {
        "id": "electricity-threat",
        "title": "Electricity disconnection threat",
        "description": "Someone calls claiming to be from the electricity department. They say your power will be disconnected in 10 minutes unless you scan a QR code and pay a verification fee.",
        "category": "authority_and_urgency",
        "choices": [
            {"id": "pay-now", "text": "Pay immediately because the caller sounds official."},
            {"id": "verify", "text": "End the call and verify with the electricity provider using an official contact I find myself."},
            {"id": "ask-caller", "text": "Ask the caller to send another payment link."},
        ],
        "correct_choice": "verify",
        "feedback": "Threats plus urgency and a pay-first demand are warning signs. Use an independently found official contact.",
        "safe_action": "End the call and check your bill or provider's official app/website.",
    },
    {
        "id": "fake-customer-care",
        "title": "A fake customer-care number",
        "description": "You search online for bank customer care. A person on a number from an unknown search result asks you to install a screen-sharing app to issue a refund.",
        "category": "remote_access",
        "choices": [
            {"id": "install", "text": "Install the app and follow their instructions."},
            {"id": "verify", "text": "Do not install it. End the call and use the number printed on my bank card or official website."},
            {"id": "share-otp", "text": "Share the OTP so the refund can be processed."},
        ],
        "correct_choice": "verify",
        "feedback": "Do not install remote-access apps or share OTPs at a caller's request.",
        "safe_action": "Disconnect and contact the bank using an independently verified official channel.",
    },
]


def public_scenarios() -> list[GymScenario]:
    # Correct answers are intentionally not returned before an attempt.
    return [
        GymScenario(id=s["id"], title=s["title"], description=s["description"],
                    choices=[GymChoice(**c) for c in s["choices"]], category=s["category"])
        for s in _SCENARIOS
    ]


def evaluate_attempt(scenario_id: str, choice_id: str) -> dict | None:
    scenario = next((s for s in _SCENARIOS if s["id"] == scenario_id), None)
    if not scenario:
        return None
    if not any(c["id"] == choice_id for c in scenario["choices"]):
        return {"invalid_choice": True}
    correct = choice_id == scenario["correct_choice"]
    return {
        "correct": correct,
        "points": 10 if correct else 0,
        "feedback": ("Correct. " if correct else "That choice could put your money or device at risk. ") + scenario["feedback"],
        "safe_action": scenario["safe_action"],
    }
