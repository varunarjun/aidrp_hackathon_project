# app/routes/incidents_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app import models, schemas
from app.database import get_db
from app.auth_utils import get_current_admin_user

# ============================================================
# ROUTER CONFIGURATION
# ============================================================
router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)

# ============================================================
# CREATE INCIDENT (Admin only)
# ============================================================
@router.post("/", response_model=schemas.IncidentOut, status_code=status.HTTP_201_CREATED)
def create_incident(
    incident: schemas.IncidentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    Create a new incident. Admin only.
    """
    # Automatically set reported_at if not provided
    db_incident = models.Incident(**incident.dict())
    if not getattr(db_incident, "reported_at", None):
        db_incident.reported_at = datetime.utcnow()
    
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

# ============================================================
# GET ALL INCIDENTS
# ============================================================
@router.get("/", response_model=List[schemas.IncidentOut])
def get_incidents(db: Session = Depends(get_db)):
    """
    Retrieve all incidents.
    """
    incidents = db.query(models.Incident).all()
    return incidents

# ============================================================
# GET INCIDENT BY ID
# ============================================================
@router.get("/{incident_id}", response_model=schemas.IncidentOut)
def get_incident_by_id(incident_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single incident by ID.
    """
    incident = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

# ============================================================
# DELETE INCIDENT BY ID (Admin only)
# ============================================================
@router.delete("/{incident_id}", status_code=status.HTTP_200_OK)
def delete_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    Delete an incident by ID. Admin only.
    """
    incident = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    db.delete(incident)
    db.commit()
    return {"message": f"✅ Incident {incident_id} deleted successfully"}