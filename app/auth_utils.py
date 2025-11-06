from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
import os

from app import crud
from app.schemas import UserOut
from app.database import get_db

# ============================================================
# JWT CONFIGURATION
# ============================================================
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# OAuth2 scheme to extract Bearer token from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# ============================================================
# GET CURRENT USER
# ============================================================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserOut:
    """
    Decode the JWT token, validate it, and return the current logged-in user.
    Raises 401 if token is invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Fetch the user from the database
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    # Return the user as a validated Pydantic model
    return UserOut.model_validate(user, from_attributes=True)


# ============================================================
# ADMIN-ONLY DEPENDENCY
# ============================================================
def get_current_admin_user(
    current_user: UserOut = Depends(get_current_user)
) -> UserOut:
    """
    Ensures that only admin users can access certain endpoints.
    Raises 403 if the user is not an admin.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user
