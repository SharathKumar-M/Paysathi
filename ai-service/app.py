
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "scam_detection_model.joblib"
)

model = joblib.load(MODEL_PATH)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "success",
        "message": "PaySaathi AI Scam Detection API is running"
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({
            "error": "Please provide a valid message"
        }), 400

    if len(message) > 10000:
        return jsonify({
            "error": "Message is too long"
        }), 400

    prediction = model.predict([message])[0]
    probabilities = model.predict_proba([message])[0]
    classes = model.classes_

    scores = dict(zip(classes, probabilities))

    return jsonify({
        "prediction": str(prediction),
        "scam_score": round(float(scores.get("scam", 0)) * 100, 2),
        "genuine_score": round(float(scores.get("genuine", 0)) * 100, 2),
        "warning": "Experimental prediction. Verify suspicious messages independently."
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
