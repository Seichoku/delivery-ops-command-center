# api/main.py (only the score endpoint shown here)
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union

app = FastAPI(title="Delivery Ops API", version="0.2.1")


class Trip(BaseModel):  # Day-1 payload
    pickup_hour: int
    distance_km: float
    pickup_zone: str


class ScoreRequest(BaseModel):  # Day-3 payload
    avg_dist: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/score")
def score(payload: Union[ScoreRequest, Trip]):
    # Compute a simple risk value
    if isinstance(payload, ScoreRequest):
        risk = 0.05 + 0.02 * payload.avg_dist
    else:
        risk = 0.05 + 0.03 * payload.pickup_hour + 0.02 * payload.distance_km

    risk = max(0.0, min(0.95, float(risk)))
    # Return both keys for compatibility with your test
    return {
        "delay_risk": round(risk, 3),
        "prediction": int(risk >= 0.5),  # simple threshold; will be replaced by real model later
    }
