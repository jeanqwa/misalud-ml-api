# MiSalud ML API

API de predicción de pulso y SpO2 utilizando un modelo entrenado en Python con Flask y desplegado con Docker en Render.

## Endpoints

- GET `/` — Verifica que el API está activo
- POST `/predict` — Envia un JSON con `"features"` para obtener predicción

Ejemplo de entrada:
```json
{
  "features": [75, 96]
}
```

Ejemplo de salida:
```json
{
  "prediction": [0]
}
```