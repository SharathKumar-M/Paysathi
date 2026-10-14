# Paysathi

PaySaathi (local build)
1. Database (once)
createdb -U postgres paysaathi

psql -U postgres -d paysaathi -f db/schema.sql

psql -U postgres -d paysaathi -f db/seed.sql
2. Backend
cd backend

python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env      # set DATABASE_URL (and ANTHROPIC_API_KEY for AI chat)

uvicorn main:app --reload

Open http://localhost:8000/docs to test every endpoint.
Endpoints
POST /check-message  {"text": "...", "lang": "en|hi|kn"}
POST /check-payment  {"intent": "send|recv|urgent", "amount": 5000, "pressure": [false,false,false,false]}
POST /chat           {"message": "...", "lang": "en|hi|kn"}

Add a new scam rule with one INSERT into scam_patterns. No code change needed.
