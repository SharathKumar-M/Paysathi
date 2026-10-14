import os
from fastapi.testclient import TestClient

# The test DB is isolated from the normal local dev database.
os.environ["PAYSAATHI_DB_PATH"] = "./data/test-paysaathi.db"
from app.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_pay_guard_flags_pressure_and_authority():
    with TestClient(app) as client:
        response = client.post("/api/v1/pay-guard/analyze", json={
            "purpose_text": "A bank officer says my pension will be stopped in 10 minutes unless I pay a verification fee. Keep it secret.",
            "recipient_type": "person",
            "on_phone_call": True,
            "is_new_payee": True,
        })
        assert response.status_code == 200
        body = response.json()
        assert body["verdict"] == "RED"
        assert body["guided_payment_allowed"] is False
        assert body["risk_score"] >= 55


def test_qr_parser():
    with TestClient(app) as client:
        response = client.post("/api/v1/pay-guard/parse-qr", json={
            "qr_payload": "upi://pay?pa=shop%40upi&pn=Corner%20Shop&am=125.50&cu=INR&tn=Groceries"
        })
        assert response.status_code == 200
        body = response.json()
        assert body["payee_address"] == "shop@upi"
        assert body["payee_name"] == "Corner Shop"
        assert body["amount"] == 125.5


def test_message_explainer_flags_otp_request():
    with TestClient(app) as client:
        response = client.post("/api/v1/messages/explain", json={
            "language": "en",
            "text": "Bank officer: share your OTP immediately or your account will be blocked."
        })
        assert response.status_code == 200
        body = response.json()
        assert body["category"] == "suspicious"
        assert body["verdict"] == "RED"


def test_after_kit_paid_has_1930_guidance():
    with TestClient(app) as client:
        response = client.post("/api/v1/after-kit/guidance", json={"language": "en", "incident_status": "paid", "amount": 500})
        assert response.status_code == 200
        body = response.json()
        assert body["helpline"] == "1930"
        assert body["urgency"] == "urgent"


def test_gym_attempt_records_progress():
    with TestClient(app) as client:
        client.get("/api/v1/scam-gym/scenarios")
        attempt = client.post("/api/v1/scam-gym/attempt", json={
            "session_id": "testsession123",
            "scenario_id": "collect-request",
            "choice_id": "decline",
            "stage": "before",
            "elapsed_seconds": 15,
        })
        assert attempt.status_code == 200
        assert attempt.json()["correct"] is True
        summary = client.get("/api/v1/scam-gym/summary/testsession123")
        assert summary.status_code == 200
        assert summary.json()["total_attempts"] >= 1


def test_hindi_pressure_phrases_are_flagged_and_localized():
    with TestClient(app) as client:
        response = client.post("/api/v1/pay-guard/analyze", json={
            "language": "hi",
            "purpose_text": "बैंक अधिकारी कहता है कि पेंशन बंद हो जाएगी। तुरंत सत्यापन शुल्क भरें और परिवार को मत बताना।",
            "recipient_type": "person",
            "on_phone_call": True,
        })
        assert response.status_code == 200
        body = response.json()
        assert body["verdict"] == "RED"
        assert "रुकें" in body["risk_label"]


def test_unknown_qr_payload_gets_warning():
    with TestClient(app) as client:
        response = client.post("/api/v1/pay-guard/analyze", json={
            "qr_payload": "https://example.invalid/collect?token=123",
            "purpose_text": "I want to pay a bill"
        })
        assert response.status_code == 200
        body = response.json()
        assert body["verdict"] == "AMBER"
        assert any(reason["code"] == "unparsed_qr" for reason in body["reasons"])


def test_saathi_fallback_is_available_without_api_key():
    with TestClient(app) as client:
        response = client.post("/api/v1/saathi", json={
            "language": "en",
            "current_screen": "after-kit",
            "message": "I already paid and money was deducted",
            "simplify": False,
            "screen_data": {},
        })
        assert response.status_code == 200
        body = response.json()
        assert "1930" in body["answer"]
        assert body["next_action"] == "open_after_kit"
