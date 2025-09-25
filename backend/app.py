from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__, 
            static_folder="../static", 
            template_folder="../templates")

CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # this will be the 'backend' folder path

# -----------------------
# Load model + encoders
# -----------------------
model = joblib.load(os.path.join(BASE_DIR, "model.joblib"))
le_sleep_disorder = joblib.load(os.path.join(BASE_DIR, "le_sleep_disorder.joblib"))
le_gender = joblib.load(os.path.join(BASE_DIR, "le_gender.joblib"))
le_occupation = joblib.load(os.path.join(BASE_DIR, "le_occupation.joblib"))
le_bmi = joblib.load(os.path.join(BASE_DIR, "le_bmi.joblib"))

# -----------------------
# Preprocessing function
# -----------------------
def preprocess_input(data):
    # Split BP
    bp = data.get("bp", "0/0")
    try:
        systolic, diastolic = map(int, bp.split("/"))
    except:
        systolic, diastolic = 0, 0

    # Encode categorical values safely
    def safe_transform(le, value):
        try:
            return le.transform([value])[0]
        except:
            return 0  # fallback to first class if unknown

    gender_enc = safe_transform(le_gender, data.get("gender", ""))
    occupation_enc = safe_transform(le_occupation, data.get("occupation", ""))
    bmi_enc = safe_transform(le_bmi, data.get("bmi", ""))

    # Build feature array in same order as training
    features = np.array([
        float(data.get("sleep_duration", 0)),
        float(data.get("sleep_quality", 0)),
        float(data.get("stress_level", 0)),
        float(data.get("physical_activity_level", 0)),
        float(data.get("age", 0)),
        bmi_enc,
        systolic,
        diastolic,
        float(data.get("heart_rate", 0)),
        float(data.get("daily_steps", 0)),
        gender_enc,
        occupation_enc
    ]).reshape(1, -1)

    return features

# -----------------------
# Routes
# -----------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        features = preprocess_input(data)

        pred_enc = model.predict(features)[0]
        pred_label = le_sleep_disorder.inverse_transform([pred_enc])[0]

        return jsonify({"result": pred_label})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# -----------------------
# Run app
# -----------------------
if __name__ == "__main__":
    app.run(debug=False)
    port = int(os.environ.get("PORT", 5000))  # Get PORT from environment or default to 5000
    app.run(host="0.0.0.0", port=port)
