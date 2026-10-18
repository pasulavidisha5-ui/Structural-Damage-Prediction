
from pathlib import Path
import json
from pathlib import Path
from fastapi import HTTPException
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "structural_damage_simple_model.pkl"
)

model = joblib.load(MODEL_PATH)

app = FastAPI(title="StructuralGuard AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BuildingInput(BaseModel):
    age: int = Field(ge=0, le=200)
    floors: int = Field(ge=1, le=20)
    families: int = Field(ge=1, le=50)
    building_size: str
    building_height: str
    construction_material: str
    building_usage: str


@app.get("/api/health")
def health():
    return {"status": "ok"}

# Model accuracy and confusion matrix endpoint
BASE_DIR = Path(__file__).resolve().parent.parent
METRICS_PATH = BASE_DIR / "model_metrics.json"


@app.get("/api/metrics")
def get_metrics():
    if not METRICS_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Model metrics not found. Run simple_model.py first."
        )

    try:
        with open(METRICS_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not read model metrics."
        ) from exc


@app.post("/api/predict")
def predict(data: BuildingInput):
    try:
        input_data = pd.DataFrame([{
            "age": data.age,
            "count_floors_pre_eq": data.floors,
            "count_families": data.families,
            "building_size": data.building_size,
            "building_height": data.building_height,
            "construction_material": data.construction_material,
            "building_usage": data.building_usage,
        }])

        prediction = int(model.predict(input_data)[0])
        probabilities = model.predict_proba(input_data)[0]

        probability_map = {
            int(cls): float(prob)
            for cls, prob in zip(model.classes_, probabilities)
        }

        labels = {
            1: "Low",
            2: "Medium",
            3: "High",
        }

        confidence = probability_map[prediction] * 100

        # Keep the existing risk-assessment rules.
        if prediction == 3:
            risk = (
                "High Risk"
                if confidence >= 70
                else "Medium Risk"
            )
        elif prediction == 2:
            risk = "Medium Risk"
        else:
            risk = (
                "Low Risk"
                if confidence >= 70
                else "Medium Risk"
            )

        return {
            "damage_class": prediction,
            "damage": labels[prediction],
            "risk": risk,
            "confidence": round(confidence, 2),
            "probabilities": {
                labels[k]: round(probability_map.get(k, 0) * 100, 2)
                for k in (1, 2, 3)
            },
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {exc}",
        ) from exc
