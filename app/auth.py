# app/auth.py
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.config import settings
from typing import Optional

# -----------------------------
# Password hashing context
# -----------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -----------------------------
# JWT configuration
# -----------------------------
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# -----------------------------
# Password utilities
# -----------------------------
def get_password_hash(password: str) -> str:
    """
    Hash a plain password using bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that a plain password matches the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

# -----------------------------
# JWT token utilities
# -----------------------------
def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with an optional expiration.
    `subject` is usually the user's email or ID.
    """
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[str]:
    """
    Decode a JWT token and return the `sub` (user identifier) if valid.
    Returns None if token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
