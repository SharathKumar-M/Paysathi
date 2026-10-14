# PaySaathi Backend (FastAPI MVP)

This is the backend starter for the PaySaathi React PWA built for Hackurity 2026. It follows the feature-list priority: Pay Guard + Pressure Detector, Saathi, Message Explainer, Scam Gym, then After Kit.

## Safety and scope

- **Simulation only:** no real UPI payment is created, authorized, or blocked by this API.
- A `GREEN` result means no known rule matched; it is **not** proof that a recipient is safe.
- The backend does not verify a VPA against bank data in this MVP.
- Never send/store UPI PINs, OTPs, passwords, or full card details.
- After Kit evidence should remain on the user's device unless they explicitly submit it to an official authority. This backend stores only anonymous Scam Gym attempts, keyed by a client-generated random session ID.
- The rules are explainable demo rules, not a production-grade fraud model.

## 1. Run locally (Windows / VS Code)

Open a terminal in this folder, then run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

If PowerShell blocks environment activation, run this in the same terminal for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Open `http://127.0.0.1:8000/docs` for interactive API testing and `http://127.0.0.1:8000/health` for the health check.

## 2. Optional screenshot analysis

Text/paste analysis and curated Saathi guidance work without an API key. To enable screenshot extraction and optional LLM-powered rephrasing of Saathi answers, set `OPENAI_API_KEY` and optionally `OPENAI_MODEL` in `.env`, then restart the server. The verdict and rule-based safety decisions are not delegated to the LLM. If the key is absent, `/api/v1/messages/explain-image` returns HTTP 503 with a safe fallback instruction. Screenshot bytes are processed in memory and are not saved to disk by this app.

## 3. Frontend origins / PWA

Defaults allow Vite at `http://localhost:5173` and `http://127.0.0.1:5173`. If your teammate deploys the frontend, add its exact origin to `CORS_ORIGINS` in `.env` and restart the API. Do not use `*` with credentials in production.

The frontend should send voice-recognition transcripts as text in the `message` or `purpose_text` field. This keeps the MVP simple and makes voice guidance optional with a text fallback.

## 4. Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/v1/meta` | Languages and feature flags |
| POST | `/api/v1/pay-guard/parse-qr` | Parse a UPI QR payload string |
| POST | `/api/v1/pay-guard/analyze` | Pay Guard + pressure detection |
| POST | `/api/v1/messages/explain` | Explain pasted message text |
| POST | `/api/v1/messages/explain-image` | Screenshot text extraction + explanation (optional API key) |
| POST | `/api/v1/saathi` | Screen-aware guidance and highlight target |
| GET | `/api/v1/scam-gym/scenarios` | Practice scenarios (answers hidden) |
| POST | `/api/v1/scam-gym/attempt` | Score an answer and record an anonymous attempt |
| GET | `/api/v1/scam-gym/summary/{session_id}` | Get progress for one anonymous session |
| POST | `/api/v1/after-kit/guidance` | Recovery/reporting checklist and bank-call script |

## 5. Example requests

### Pay Guard

```json
{
  "language": "en",
  "payee_name": "Ravi Kumar",
  "payee_id": "ravi@upi",
  "amount": 2500,
  "purpose_text": "A caller said my pension will be stopped unless I pay a verification fee immediately. They told me not to tell my family.",
  "request_type": "pay",
  "is_new_payee": true,
  "recipient_type": "person",
  "on_phone_call": true
}
```

### Message explainer

```json
{
  "language": "kn",
  "text": "Your account will be blocked in 10 minutes. Share your OTP with our bank officer immediately."
}
```

### Saathi

```json
{
  "language": "en",
  "current_screen": "pay-guard",
  "message": "How do I check this payment?",
  "simplify": false,
  "screen_data": {}
}
```

### After Kit

```json
{
  "language": "en",
  "incident_status": "paid",
  "has_screenshot": true,
  "has_caller_number": true,
  "has_transaction_details": true,
  "amount": 2500
}
```

## 6. Contract notes for frontend

- Supported languages: `en`, `kn`, `hi`.
- Pay Guard verdict values: `GREEN`, `AMBER`, `RED`.
- Each warning reason contains a stable `code`, human-readable title/detail, weight, and severity.
- Map `highlight_element` to matching frontend IDs such as `payment-purpose`, `message-input`, `start-practice`, and `call-1930`.
- Generate a random `session_id` per Scam Gym learner on the client, e.g. `crypto.randomUUID().replaceAll('-', '')`; do not use a person's name, phone number, or account details.
- Do not build UI around a promise that a real payment is blocked. The API returns guidance for the simulated flow only.

## 7. Run tests

```powershell
pip install pytest httpx
pytest -q
```
