import firebase_admin
from firebase_admin import credentials, messaging
import os
import json
import tempfile

# Inicializa Firebase solo si la variable está definida
firebase_json_str = os.getenv("FIREBASE_CREDENTIALS_JSON")
if firebase_json_str:
    try:
        firebase_dict = json.loads(firebase_json_str)
        # Corrige el error del private_key con saltos de línea
        if "private_key" in firebase_dict:
            firebase_dict["private_key"] = firebase_dict["private_key"].replace("\\n", "\n")
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json') as tmp:
            json.dump(firebase_dict, tmp)
            tmp.flush()
            cred = credentials.Certificate(tmp.name)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase inicializado correctamente.")
    except Exception as e:
        print(f"❌ Error al inicializar Firebase: {e}")
else:
    print("⚠️ Variable de entorno FIREBASE_CREDENTIALS_JSON no definida.")
