# app/routes/admin_notifications_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import FileResponse
import pandas as pd
import os
import logging

from app import models, schemas
from app.database import get_db
from app.auth_utils import get_current_admin_user
from app.utils.email_utils import send_email

router = APIRouter(
    prefix="/admin/notifications",
    tags=["Admin Notifications"]
)

# CREATE NOTIFICATION
@router.post("/", response_model=schemas.NotificationOut, status_code=status.HTTP_201_CREATED)
def create_notification(
    notification: schemas.NotificationCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    recipient = db.query(models.User).filter(models.User.email == notification.recipient).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient user not found")

    db_notification = models.Notification(
        title=notification.title,
        message=notification.message,
        target_user_id=recipient.id,
        created_by=current_admin.id,
        sent=False
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    # Send email
    try:
        if send_email(recipient.email, db_notification.title, db_notification.message):
            db_notification.sent = True
            db.commit()
    except Exception as e:
        logging.error(f"❌ Email sending failed: {e}")

    return db_notification

# GET ALL NOTIFICATIONS
@router.get("/", response_model=List[schemas.NotificationOut])
def get_all_notifications(
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    return db.query(models.Notification).all()

# DELETE NOTIFICATION
@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    db.delete(notification)
    db.commit()
    return None

# DAILY REPORT CSV
@router.get("/report/daily", response_class=FileResponse)
def daily_report(
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    notifications = db.query(models.Notification).all()
    if not notifications:
        raise HTTPException(status_code=404, detail="No notifications found")

    df = pd.DataFrame([{
        "title": n.title,
        "recipient_id": n.target_user_id,
        "created_by": n.created_by,
        "sent": n.sent,
        "created_at": n.created_at
    } for n in notifications])

    file_path = os.path.join(os.getcwd(), "notification_report.csv")
    df.to_csv(file_path, index=False)

    return FileResponse(file_path, media_type="text/csv", filename="daily_notification_report.csv")
