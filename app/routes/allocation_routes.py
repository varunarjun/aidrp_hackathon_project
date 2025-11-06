# app/routes/allocation_routes.py
from fastapi import APIRouter

router = APIRouter(prefix="/allocation", tags=["Resource Allocation"])

@router.get("/predict")
def predict_resource(incident_type: str, severity: int):
    # Minimal dummy logic
    resources = {
        "fire": ["Fire Truck", "Water Tank"],
        "flood": ["Boats", "Rescue Team"],
        "earthquake": ["Ambulance", "Rescue Team"]
    }
    needed = resources.get(incident_type.lower(), ["General Rescue Team"])
    return {
        "incident_type": incident_type,
        "severity": severity,
        "allocated_resources": needed[:severity]  # just slice for demo
    }
