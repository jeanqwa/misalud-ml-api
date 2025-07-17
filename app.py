from flask import Flask, request, jsonify
import joblib
import numpy as np
import os
import json
import tempfile

# 🔥 Firebase Admin SDK
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__)

# ✅ Cargar el modelo
model = joblib.load("modelo_spo2_pulso.joblib")

# ✅ Inicializar Firebase desde variable de entorno
if not firebase_admin._apps:
    cred_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")
    if cred_json:
        try:
            # Escribir el contenido JSON en un archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json") as tmp:
                tmp.write(cred_json)
                tmp_path = tmp.name

            cred = credentials.Certificate(tmp_path)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase inicializado correctamente")
        except Exception as e:
            print("❌ Error al inicializar Firebase:", e)
    else:
        print("⚠️ Variable de entorno FIREBASE_CREDENTIALS_JSON no definida.")

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

    # ✅ Enviar notificación si hay anomalía
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
            print("✅ Notificación enviada:", response)
        except Exception as e:
            print("❌ Error al enviar notificación:", e)

    return jsonify({"prediction": prediction})
