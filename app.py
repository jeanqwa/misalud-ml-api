from flask import Flask, request, jsonify
import joblib
import numpy as np
import os
import json

# 🔥 Firebase Admin SDK
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)

# Cargar modelo
model = joblib.load("modelo_spo2_pulso.joblib")

# ✅ Inicializar Firebase Admin usando variable de entorno
if not firebase_admin._apps:
    cred_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")
    if cred_json:
        cred = credentials.Certificate(json.loads(cred_json))
        firebase_admin.initialize_app(cred)
    else:
        print("⚠️ Variable de entorno FIREBASE_CREDENTIALS_JSON no definida.")

@app.route("/", methods=["GET"])
def index():
    return "¡API funcionando correctamente desde Docker y Render!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    features = data.get("features")
    token = data.get("fcm_token")  # ⚠️ Esperamos también el token FCM

    if not features:
        return jsonify({"error": "Faltan características 'features'"}), 400

    features_np = np.array(features).reshape(1, -1)
    prediction = model.predict(features_np).tolist()

    # ✅ Si es una anomalía, se envía una notificación push
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
