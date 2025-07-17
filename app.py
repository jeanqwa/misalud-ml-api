from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Carga del modelo
model = joblib.load("modelo_spo2_pulso.joblib")

@app.route("/", methods=["GET"])
def index():
    return "¡API funcionando correctamente desde Docker y Render!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    features = np.array(data["features"]).reshape(1, -1)
    prediction = model.predict(features)
    return jsonify({"prediction": prediction.tolist()})