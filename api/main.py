from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Delivery Ops API", version="0.1.0")

class Trip(BaseModel):
    pickup_hour: int
    distance_km: float
    pickup_zone: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/score")
def score(trip: Trip):
    risk = min(0.95, 0.05 + 0.03 * trip.pickup_hour + 0.02 * trip.distance_km)
    return {"delay_risk": round(float(risk), 3)}
