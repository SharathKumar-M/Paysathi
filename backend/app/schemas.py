from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field, field_validator

Language = Literal["en", "kn", "hi"]
Verdict = Literal["GREEN", "AMBER", "RED"]


class APIMessage(BaseModel):
    message: str


class ParsedPayment(BaseModel):
    scheme: str | None = None
    payee_address: str | None = None
    payee_name: str | None = None
    amount: float | None = None
    currency: str | None = None
    note: str | None = None
    reference: str | None = None
    raw_payload_received: bool = False


class PayGuardRequest(BaseModel):
    language: Language = "en"
    payee_name: str | None = Field(default=None, max_length=160)
    payee_id: str | None = Field(default=None, max_length=200)
    amount: float | None = Field(default=None, ge=0, le=100_000_000)
    currency: str = Field(default="INR", max_length=8)
    purpose_text: str = Field(default="", max_length=5000)
    qr_payload: str | None = Field(default=None, max_length=5000)
    request_type: Literal["pay", "collect", "unknown"] = "pay"
    is_new_payee: bool = False
    recipient_type: Literal["person", "merchant", "government", "utility", "unknown"] = "unknown"
    on_phone_call: bool = False

    @field_validator("purpose_text")
    @classmethod
    def trim_purpose(cls, value: str) -> str:
        return value.strip()


class SafetySignal(BaseModel):
    code: str
    title: str
    detail: str
    weight: int
    severity: Literal["info", "warning", "high"]


class PayGuardResponse(BaseModel):
    verdict: Verdict
    risk_score: int = Field(ge=0, le=100)
    risk_label: str
    explanation: str
    reasons: list[SafetySignal]
    next_steps: list[str]
    parsed_payment: ParsedPayment
    guided_payment_allowed: bool
    disclaimer: str


class MessageExplainRequest(BaseModel):
    language: Language = "en"
    text: str = Field(min_length=1, max_length=12000)


class MessageExplainResponse(BaseModel):
    category: Literal["real_alert", "otp", "promotion", "suspicious", "unknown"]
    verdict: Verdict
    summary: str
    reasons: list[SafetySignal]
    recommended_action: str
    spoken_summary: str
    limitation: str = "This is a warning-pattern check, not sender authentication. Verify important messages through an official channel."


class SaathiRequest(BaseModel):
    language: Language = "en"
    current_screen: str = Field(default="home", max_length=80)
    message: str = Field(default="", max_length=5000)
    simplify: bool = False
    screen_data: dict[str, Any] = Field(default_factory=dict)


class SaathiResponse(BaseModel):
    answer: str
    language: Language
    highlight_element: str | None = None
    next_action: str | None = None
    suggestions: list[str] = Field(default_factory=list)
    safety_note: str = "Saathi guides only. It never moves money or asks for your PIN or OTP."


class GymChoice(BaseModel):
    id: str
    text: str


class GymScenario(BaseModel):
    id: str
    title: str
    description: str
    choices: list[GymChoice]
    category: str
    estimated_seconds: int = 30


class GymAttemptRequest(BaseModel):
    session_id: str = Field(min_length=8, max_length=80, pattern=r"^[A-Za-z0-9_-]+$")
    scenario_id: str = Field(min_length=1, max_length=80)
    choice_id: str = Field(min_length=1, max_length=80)
    stage: Literal["before", "practice", "after"] = "practice"
    elapsed_seconds: int = Field(default=0, ge=0, le=3600)
    language: Language = "en"


class GymAttemptResponse(BaseModel):
    correct: bool
    points: int
    feedback: str
    safe_action: str
    session_summary: dict[str, Any]


class AfterKitRequest(BaseModel):
    language: Language = "en"
    incident_status: Literal["not_paid", "paid", "unsure"]
    has_screenshot: bool = False
    has_caller_number: bool = False
    has_transaction_details: bool = False
    amount: float | None = Field(default=None, ge=0, le=100_000_000)


class AfterKitResponse(BaseModel):
    urgency: Literal["urgent", "caution", "prevention"]
    headline: str
    steps: list[str]
    evidence_checklist: list[str]
    bank_call_script: str
    helpline: str = "1930"
    reporting_portal: str = "https://www.cybercrime.gov.in/"
    privacy_note: str = "Do not upload or share your UPI PIN, OTP, passwords, or full card details. Keep evidence on your device and share it only with official responders."


class GymSummaryResponse(BaseModel):
    session_id: str
    total_attempts: int
    correct_attempts: int
    accuracy_percent: int
    by_stage: dict[str, int]
