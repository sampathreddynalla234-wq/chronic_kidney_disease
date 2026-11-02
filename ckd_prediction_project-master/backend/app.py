import os
from pathlib import Path
from datetime import datetime, timezone
import joblib
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
MODEL_PATH = Path(__file__).with_name("ckd_demo_model.joblib")
FEATURES = ["age","blood_pressure","specific_gravity","albumin","sugar",
            "blood_glucose","blood_urea","serum_creatinine","hemoglobin",
            "packed_cell_volume"]
bundle = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None

def save_record(record):
    uri = os.getenv("MONGO_URI")
    if not uri:
        return False
    try:
        from pymongo import MongoClient
        client = MongoClient(uri, serverSelectionTimeoutMS=1500)
        client.admin.command("ping")
        client["ckd_project"]["predictions"].insert_one(record)
        client.close()
        return True
    except Exception:
        return False

@app.get("/api/health")
def health():
    return jsonify(status="ok", model_loaded=bundle is not None,
                   notice="Synthetic classroom demo; not for medical use.")

@app.post("/api/predict")
def predict():
    if bundle is None:
        return jsonify(error="Model missing. Run python train_model.py first."),503
    data = request.get_json(silent=True) or {}
    missing = [f for f in FEATURES if f not in data]
    if missing:
        return jsonify(error="Missing fields", fields=missing),400
    try:
        row = {f:float(data[f]) for f in FEATURES}
        if not all(pd.notna(v) for v in row.values()):
            raise ValueError("Enter valid numeric values.")
        if not 0 <= row["age"] <= 120:
            raise ValueError("Age must be between 0 and 120.")
        if not 0 <= row["albumin"] <= 5 or not 0 <= row["sugar"] <= 5:
            raise ValueError("Albumin and sugar must be between 0 and 5.")
        if not 1 <= row["specific_gravity"] <= 1.1:
            raise ValueError("Specific gravity must be between 1.0 and 1.1.")
        frame = pd.DataFrame([row],columns=FEATURES)
        model = bundle["model"]
        pred = int(model.predict(frame)[0])
        probs = model.predict_proba(frame)[0]
        result = {
            "demo_prediction":"Higher demo-model flag" if pred else "Lower demo-model flag",
            "demo_score_percent":round(float(max(probs))*100,1),
            "notice":"Synthetic-data demo only. NOT a diagnosis or reliable CKD risk estimate."
        }
        record = {"inputs":row,"result":result,
                  "created_at":datetime.now(timezone.utc).isoformat()}
        result["saved_to_mongodb"] = save_record(record)
        return jsonify(result)
    except (TypeError,ValueError) as exc:
        return jsonify(error=str(exc)),400

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000,debug=True)
