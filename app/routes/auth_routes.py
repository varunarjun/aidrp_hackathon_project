# app/routes/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, schemas, auth  # auth should include create_access_token
from app.deps import get_db
from app.auth_utils import get_current_user

router = APIRouter(tags=["Authentication"])

# -----------------------------
# Register a new user
# -----------------------------
@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user (Responder, Admin, Analyst, etc.)
    """
    existing = crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user = crud.create_user(
        db=db,
        email=user_in.email,
        password=user_in.password,
        full_name=user_in.full_name,
        role=user_in.role
    )
    return user

# -----------------------------
# Login user and get JWT token
# -----------------------------
@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user and return a JWT token.
    """
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}

# -----------------------------
# Get logged-in user's profile
# -----------------------------
@router.get("/profile", response_model=schemas.UserOut)
def read_profile(current_user: schemas.UserOut = Depends(get_current_user)):
    """
    Get the currently logged-in user's profile.
    """
    return current_user

# -----------------------------
# Logout user (simulated)
# -----------------------------
@router.post("/logout")
def logout_user():
    """
    Simulate logout. (JWT is stateless — just discard the token on client side)
    """
    return {"message": "Successfully logged out."}
