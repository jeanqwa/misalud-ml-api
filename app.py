from flask import Flask, request, jsonify
import joblib
import numpy as np
import os
import json
import base64

# 🔥 Firebase Admin SDK
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)

# ✅ Cargar modelo
model = joblib.load("modelo_spo2_pulso.joblib")

# ✅ Inicializar Firebase Admin usando variable de entorno codificada en base64
if not firebase_admin._apps:
    b64_json = os.environ.get("FIREBASE_CREDENTIALS_JSON_B64")
    if b64_json:
        try:
            decoded = base64.b64decode(b64_json).decode("utf-8")
            cred_dict = json.loads(decoded)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase inicializado correctamente.")
        except Exception as e:
            print(f"❌ Error al inicializar Firebase: {e}")
    else:
        print("⚠️ Variable de entorno FIREBASE_CREDENTIALS_JSON_B64 no definida.")

@app.route("/", methods=["GET"])
def index():
    return "¡API funcionando correctamente desde Docker y Render!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    features = data.get("features")
    token = data.get("fcm_token")

    if not features:
        return jsonify({"error": "Faltan características 'features'"}), 400

    features_np = np.array(features).reshape(1, -1)
    prediction = model.predict(features_np).tolist()

    # ✅ Enviar notificación si hay anomalía y token está presente
    if prediction[0] == 0 and token:
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title="⚠️ Anomalía detectada",
                    body=f"Pulso: {features[0]}, SpO₂: {features[1]}%"
                ),
                token=token
            )
            response = messaging.send(message)
            print("✅ Notificación FCM enviada:", response)
        except Exception as e:
            print("❌ Error al enviar la notificación FCM:", e)

    return jsonify({"prediction": prediction})
