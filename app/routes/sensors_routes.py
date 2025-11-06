from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db
from app.auth_utils import get_current_admin_user

# ============================================================
# ROUTER CONFIGURATION
# ============================================================
router = APIRouter(
    prefix="/sensors",
    tags=["Sensors"]
)

# ============================================================
# CREATE SENSOR (Admin only)
# ============================================================
@router.post("/", response_model=schemas.SensorOut, status_code=status.HTTP_201_CREATED)
def create_sensor(
    sensor: schemas.SensorCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    Create a new sensor. Admin only.
    """
    db_sensor = models.Sensor(**sensor.dict())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor

# ============================================================
# GET ALL SENSORS
# ============================================================
@router.get("/", response_model=List[schemas.SensorOut])
def get_sensors(db: Session = Depends(get_db)):
    """
    Retrieve all sensors.
    """
    return db.query(models.Sensor).all()

# ============================================================
# GET SENSOR BY ID
# ============================================================
@router.get("/{sensor_id}", response_model=schemas.SensorOut)
def get_sensor_by_id(sensor_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single sensor by ID.
    """
    sensor = db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor

# ============================================================
# DELETE SENSOR BY ID (Admin only)
# ============================================================
@router.delete("/{sensor_id}", status_code=status.HTTP_200_OK)
def delete_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user)
):
    """
    Delete a sensor by ID. Admin only.
    """
    sensor = db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    
    db.delete(sensor)
    db.commit()
    return {"message": f"✅ Sensor {sensor_id} deleted successfully"}
