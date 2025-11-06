from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas, models
from app.database import get_db
from app.auth_utils import get_current_admin_user
from app.utils.security import hash_password  # ✅ Fixed import

# ============================================================
# ADMIN ROUTER CONFIGURATION
# ============================================================
router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

# ============================================================
# 1️⃣ LIST ALL USERS (ADMIN ONLY)
# ============================================================
@router.get("/users", response_model=List[schemas.UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    users = db.query(models.User).all()
    return [schemas.UserOut.model_validate(user, from_attributes=True) for user in users]

# ============================================================
# 2️⃣ UPDATE A USER (ADMIN ONLY)
# ============================================================
@router.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    db_user = crud.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user_in.email is not None:
        db_user.email = user_in.email
    if user_in.full_name is not None:
        db_user.full_name = user_in.full_name
    if user_in.role is not None:
        db_user.role = user_in.role
    if user_in.password is not None:
        db_user.hashed_password = hash_password(user_in.password)
    if user_in.is_active is not None:
        db_user.is_active = user_in.is_active

    db.commit()
    db.refresh(db_user)
    return schemas.UserOut.model_validate(db_user, from_attributes=True)

# ============================================================
# 3️⃣ DELETE A USER (ADMIN ONLY)
# ============================================================
@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    db_user = crud.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": f"✅ User {user_id} deleted successfully"}
