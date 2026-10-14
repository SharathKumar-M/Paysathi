from __future__ import annotations

from urllib.parse import parse_qs, urlparse
from app.services.i18n import MESSAGE_COPY, PAY_GUARD_COPY, localize_signals
from app.schemas import (
    MessageExplainResponse,
    ParsedPayment,
    PayGuardRequest,
    PayGuardResponse,
    SafetySignal,
)

# These rules are intentionally transparent and conservative. A lack of flags is NOT proof of safety.
RULES: list[tuple[str, tuple[str, ...], int, str, str, str]] = [
    (
        "credential_request",
        ("share your otp", "tell me your otp", "send me the otp", "share otp", "share your pin", "tell me your pin", "upi pin to receive", "enter pin to receive", "give me your upi pin", "install anydesk", "install teamviewer", "remote access", "screen sharing app", "otp बताओ", "ओटीपी बताएं", "अपना ओटीपी बताएं", "पिन बताएं", "अपना पिन बताएं", "पासवर्ड बताएं", "ओटीपी साझा करें", "otp ಹೇಳಿ", "ಒಟಿಪಿ ಹೇಳಿ", "ಪಿನ್ ಹೇಳಿ", "ನಿಮ್ಮ ಪಿನ್ ನೀಡಿ", "ಒಟಿಪಿ ಹಂಚಿಕೊಳ್ಳಿ", "ಸ್ಕ್ರೀನ್ ಶೇರಿಂಗ್", "ರಿಮೋಟ್ ಆಕ್ಸೆಸ್"),
        100,
        "Request for a secret or remote access",
        "Someone appears to be asking for an OTP, PIN, or remote access. These details can let them take control of your money or device.",
        "high",
    ),
    (
        "collect_request",
        ("collect request", "approve to receive", "accept to receive money", "receive money by entering pin", "to get refund enter pin", "request money from you", "कलेक्ट रिक्वेस्ट", "कलेक्ट अनुरोध", "पैसे पाने के लिए पिन", "पैसे प्राप्त करने के लिए पिन", "ಹಣ ಪಡೆಯಲು ಪಿನ್", "ಹಣ ಸ್ವೀಕರಿಸಲು ಪಿನ್", "ಕಲೆಕ್ಟ್ ರಿಕ್ವೆಸ್ಟ್"),
        75,
        "Possible collect-request trick",
        "A collect request asks you to approve sending money; it is not how you accept money into your account.",
        "high",
    ),
    (
        "secrecy",
        ("don't tell anyone", "do not tell anyone", "keep this secret", "don't tell your family", "do not tell your family", "nobody should know", "keep it confidential", "किसी को मत बताना", "परिवार को मत बताना", "गुप्त रखें", "किसी को न बताएं", "ಯಾರಿಗೂ ಹೇಳಬೇಡಿ", "ಕುಟುಂಬಕ್ಕೆ ಹೇಳಬೇಡಿ", "ಇದನ್ನು ರಹಸ್ಯವಾಗಿಡಿ"),
        30,
        "Request for secrecy",
        "A request to hide a payment from family or trusted people is a warning sign.",
        "high",
    ),
    (
        "urgency",
        ("immediately", "right now", "within 10 minutes", "within ten minutes", "urgent", "hurry", "today or else", "last chance", "account will be blocked", "pension will be stopped", "electricity will be disconnected", "तुरंत", "अभी", "10 मिनट में", "खाता बंद", "पेंशन बंद", "बिजली काट", "जल्दी करें", "ತಕ್ಷಣ", "ಈಗಲೇ", "10 ನಿಮಿಷಗಳಲ್ಲಿ", "ಖಾತೆ ಬ್ಲಾಕ್", "ಪಿಂಚಣಿ ನಿಲ್ಲಿಸಲಾಗುತ್ತದೆ", "ವಿದ್ಯುತ್ ಕಡಿತ", "ಬೇಗ ಮಾಡಿ"),
        25,
        "Pressure to act quickly",
        "The message or story pressures you to act quickly instead of checking the request independently.",
        "warning",
    ),
    (
        "authority_impersonation",
        ("rbi officer", "reserve bank officer", "police officer", "bank officer", "government officer", "pension department", "customs officer", "income tax officer", "court officer", "kyc team", "electricity department", "बैंक अधिकारी", "सरकारी अधिकारी", "पुलिस अधिकारी", "आरबीआई", "पेंशन विभाग", "बिजली विभाग", "बैंक कर्मचारी", "सरकारी कर्मचारी", "ಬ್ಯಾಂಕ್ ಅಧಿಕಾರಿ", "ಸರ್ಕಾರಿ ಅಧಿಕಾರಿ", "ಪೊಲೀಸ್ ಅಧಿಕಾರಿ", "ಆರ್‌ಬಿಐ", "ಪಿಂಚಣಿ ಇಲಾಖೆ", "ವಿದ್ಯುತ್ ಇಲಾಖೆ"),
        20,
        "Possible authority impersonation",
        "The story invokes a bank, government, police, or utility authority. The claim cannot be verified from this text alone.",
        "warning",
    ),
    (
        "pay_first_verify_later",
        ("verification fee", "pension verification", "pay first", "pay to receive", "release your prize", "refund fee", "unlock your account", "unblock pension", "kyc fee", "security fee", "pay to avoid arrest", "pay to avoid disconnection", "सत्यापन शुल्क", "पेंशन सत्यापन", "पहले भुगतान करें", "पैसे पाने के लिए भुगतान", "खाता अनब्लॉक", "केवाईसी शुल्क", "जुर्माना भरें", "इनाम पाने के लिए शुल्क", "ಪರಿಶೀಲನೆ ಶುಲ್ಕ", "ಪಿಂಚಣಿ ಪರಿಶೀಲನೆ", "ಮೊದಲು ಪಾವತಿಸಿ", "ಹಣ ಪಡೆಯಲು ಪಾವತಿಸಿ", "ಖಾತೆ ಅನ್ಲಾಕ್", "ಕೆವೈಸಿ ಶುಲ್ಕ", "ದಂಡ ಪಾವತಿಸಿ"),
        30,
        "Payment required before verification",
        "A demand for money to unlock a benefit, avoid a threat, or complete an unverified process is suspicious.",
        "high",
    ),
    (
        "otp_topic",
        ("otp", "one time password", "one-time password", "ओटीपी", "ಒಟಿಪಿ"),
        5,
        "OTP mentioned",
        "Never share an OTP with another person. Enter it only in the official service where you initiated the action.",
        "info",
    ),
]

SUSPICIOUS_URL_MARKERS = ("bit.ly/", "tinyurl.com/", "cutt.ly/", "shorturl.at/", "t.co/")
REAL_ALERT_MARKERS = ("debited", "credited", "transaction alert", "account balance", "payment successful", "payment received", "statement generated")
PROMOTION_MARKERS = ("cashback", "special offer", "voucher", "discount", "limited offer", "congratulations", "you won", "free gift", "reward points")


def parse_upi_qr(payload: str | None) -> ParsedPayment:
    if not payload:
        return ParsedPayment(raw_payload_received=False)
    parsed = urlparse(payload.strip())
    # UPI QR commonly uses upi://pay?pa=...&pn=...&am=...&cu=INR&tn=...
    if parsed.scheme.lower() not in {"upi", "http", "https"}:
        return ParsedPayment(scheme=parsed.scheme or None, raw_payload_received=True)
    params = parse_qs(parsed.query)
    amount = None
    amount_values = params.get("am", [])
    if amount_values:
        try:
            amount = float(amount_values[0])
        except (TypeError, ValueError):
            amount = None
    return ParsedPayment(
        scheme=parsed.scheme.lower() or None,
        payee_address=(params.get("pa") or [None])[0],
        payee_name=(params.get("pn") or [None])[0],
        amount=amount,
        currency=(params.get("cu") or ["INR"])[0],
        note=(params.get("tn") or [None])[0],
        reference=(params.get("tr") or params.get("tid") or [None])[0],
        raw_payload_received=True,
    )


def find_signals(text: str) -> list[SafetySignal]:
    lowered = text.lower()
    signals: list[SafetySignal] = []
    for code, phrases, weight, title, detail, severity in RULES:
        matched = next((phrase for phrase in phrases if phrase in lowered), None)
        if matched:
            # An OTP-only mention is informational; an OTP request is caught by credential_request.
            signals.append(SafetySignal(code=code, title=title, detail=detail, weight=weight, severity=severity))
    if any(marker in lowered for marker in SUSPICIOUS_URL_MARKERS):
        signals.append(SafetySignal(
            code="shortened_link", title="Shortened link", weight=25, severity="warning",
            detail="This message contains a shortened link that hides the destination. Do not open it unless you independently verify it."
        ))
    return signals


def _score_and_verdict(signals: list[SafetySignal]) -> tuple[int, str]:
    if any(s.code in {"credential_request", "collect_request"} for s in signals):
        return 90, "RED"
    # A combination of pressure + authority/pay-first/secrecy is more concerning than any one phrase.
    codes = {s.code for s in signals}
    if "urgency" in codes and ({"authority_impersonation", "secrecy", "pay_first_verify_later"} & codes):
        return 85, "RED"
    score = min(100, sum(s.weight for s in signals if s.code != "otp_topic"))
    if score >= 55:
        return score, "RED"
    if score >= 20:
        return score, "AMBER"
    return score, "GREEN"


def assess_pay_guard(request: PayGuardRequest) -> PayGuardResponse:
    parsed = parse_upi_qr(request.qr_payload)
    payee_name = request.payee_name or parsed.payee_name
    amount = request.amount if request.amount is not None else parsed.amount
    combined_text = " ".join([
        request.purpose_text,
        parsed.note or "",
        payee_name or "",
    ]).strip()
    signals = find_signals(combined_text)
    if request.qr_payload and parsed.scheme != "upi":
        signals.append(SafetySignal(
            code="unparsed_qr", title="QR format not recognized", weight=20, severity="warning",
            detail="This QR payload was not recognized as a standard UPI payment link. Do not enter banking details on a linked website unless you verify it independently."
        ))

    if request.request_type == "collect":
        if not any(signal.code == "collect_request" for signal in signals):
            signals.append(SafetySignal(
                code="collect_request", title="Collect request", weight=75, severity="high",
                detail="You selected a collect request. Review it carefully: accepting it may authorize money to leave your account."
            ))
    if request.is_new_payee:
        signals.append(SafetySignal(
            code="new_payee", title="New recipient", weight=12, severity="warning",
            detail="This recipient is new to you. Check the name and payment purpose carefully before continuing."
        ))
    if request.on_phone_call:
        signals.append(SafetySignal(
            code="active_call", title="You are on a call", weight=20, severity="warning",
            detail="A caller may be influencing your decision. End an unexpected call and contact the organization using a number you find independently."
        ))
    if amount is not None and amount >= 10000:
        signals.append(SafetySignal(
            code="large_amount", title="Large payment", weight=20 if amount < 50000 else 30, severity="warning",
            detail="This is a relatively large payment. Double-check the recipient and amount before authorizing it."
        ))
    if request.recipient_type == "person" and any(term in request.purpose_text.lower() for term in ("pension", "government", "rbi", "verification fee", "kyc fee", "police", "electricity department")):
        signals.append(SafetySignal(
            code="purpose_recipient_mismatch", title="Purpose and recipient may not match", weight=35, severity="high",
            detail="You described an official or service-related fee, but the recipient is marked as a person. Independently verify the payment before proceeding."
        ))

    score, verdict = _score_and_verdict(signals)
    # Make the 
    # A mismatch between the stated purpose and a personal recipient becomes red when other warning signs exist.
    codes = {s.code for s in signals}
    if "purpose_recipient_mismatch" in codes and ({"authority_impersonation", "pay_first_verify_later", "urgency"} & codes):
        verdict, score = "RED", max(score, 75)
    if verdict == "RED":
        label = "Stop and verify"
        explanation = "This payment situation has strong warning signs. Do not continue in this demo flow; verify through an official contact you find independently."
        steps = [
            "Do not approve the payment or share a PIN/OTP.",
            "End any unexpected call and do not use links or numbers supplied by the caller.",
            "Verify the request using an official app, website, or phone number you find yourself.",
        ]
    elif verdict == "AMBER":
        label = "Pause and check"
        explanation = "We found something that deserves a second look. This does not prove it is a scam, but you should verify before paying."
        steps = [
            "Recheck the recipient name and amount.",
            "Ask a trusted person or contact the bank/service independently if anything feels unusual.",
            "Never share your UPI PIN or OTP with anyone.",
        ]
    else:
        label = "No obvious warning pattern found"
        explanation = "No strong warning pattern was found in the details provided. This does not prove the recipient is safe; check the name, amount, and purpose yourself."
        steps = [
            "Confirm the displayed recipient and amount yourself.",
            "Continue only if you initiated the payment and understand what it is for.",
            "Never share your UPI PIN or OTP with anyone.",
        ]
    if request.language in PAY_GUARD_COPY:
        label, explanation, steps = PAY_GUARD_COPY[request.language][verdict]
    signals = localize_signals(signals, request.language)
    return PayGuardResponse(
        verdict=verdict,
        risk_score=score,
        risk_label=label,
        explanation=explanation,
        reasons=signals,
        next_steps=steps,
        parsed_payment=ParsedPayment(
            scheme=parsed.scheme,
            payee_address=request.payee_id or parsed.payee_address,
            payee_name=payee_name,
            amount=amount,
            currency=request.currency or parsed.currency or "INR",
            note=parsed.note,
            reference=parsed.reference,
            raw_payload_received=parsed.raw_payload_received,
        ),
        guided_payment_allowed=(verdict != "RED"),
        disclaimer="PaySaathi cannot verify a payee with bank data in this MVP. A GREEN result is not a safety guarantee. Payment authorization remains with the user in the payment app.",
    )


def explain_message(text: str, language: str = "en") -> MessageExplainResponse:
    lowered = text.lower()
    signals = find_signals(text)
    codes = {s.code for s in signals}
    if "credential_request" in codes or "collect_request" in codes:
        verdict, category = "RED", "suspicious"
    elif ("urgency" in codes and ({"authority_impersonation", "secrecy", "pay_first_verify_later"} & codes)) or "shortened_link" in codes:
        verdict, category = "RED", "suspicious"
    elif "otp" in lowered or "one time password" in lowered or "one-time password" in lowered:
        verdict, category = "AMBER", "otp"
    elif any(marker in lowered for marker in PROMOTION_MARKERS):
        verdict, category = ("AMBER", "suspicious") if signals else ("AMBER", "promotion")
    elif any(marker in lowered for marker in REAL_ALERT_MARKERS):
        verdict, category = ("AMBER", "suspicious") if signals else ("AMBER", "real_alert")
    elif signals:
        _, verdict = _score_and_verdict(signals)
        category = "suspicious" if verdict in {"AMBER", "RED"} else "unknown"
    else:
        verdict, category = "AMBER", "unknown"

    summaries = {
        "real_alert": "This looks like a transaction or account alert, but the sender cannot be authenticated from the message text alone.",
        "otp": "This message mentions an OTP. Never tell the code to a caller or share it in a chat; use it only in the official service you started.",
        "promotion": "This looks like a promotional message. Be careful with links, prize claims, or requests for a fee to receive a reward.",
        "suspicious": "This message contains suspicious patterns. Do not open links, share secrets, or pay until you verify it through an official channel.",
        "unknown": "I cannot confidently classify this message from its text alone. Do not share an OTP or PIN; verify important requests independently.",
    }
    actions = {
        "real_alert": "Open your bank's official app directly to confirm the transaction; do not use links in the message.",
        "otp": "Do not share the OTP. If you did not request it, do not approve anything and contact your bank through its official channel.",
        "promotion": "Ignore unexpected reward links and never pay a fee to claim a prize without independent verification.",
        "suspicious": "Pause, do not click or pay, and verify using a phone number or website you find independently.",
        "unknown": "Ask a trusted person or check the official app/website directly before acting.",
    }
    if language in MESSAGE_COPY:
        summary, recommended_action = MESSAGE_COPY[language][category]
    else:
        summary, recommended_action = summaries[category], actions[category]
    signals = localize_signals(signals, language)
    return MessageExplainResponse(
        category=category,
        verdict=verdict,
        summary=summary,
        reasons=signals,
        recommended_action=recommended_action,
        spoken_summary=summary,
    )
