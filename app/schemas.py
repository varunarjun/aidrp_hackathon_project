# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# =========================================================
# ====================== USERS ===========================
# =========================================================
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: Optional[str] = "responder"  # default role

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    role: str
    is_active: bool

    class Config:
        from_attributes = True  # Pydantic v2 compatible

# =========================================================
# ====================== AUTH TOKENS =====================
# =========================================================
class Token(BaseModel):
    access_token: str
    token_type: str

# =========================================================
# ====================== INCIDENTS =======================
# =========================================================
class IncidentBase(BaseModel):
    title: str
    description: Optional[str] = None
    severity: str
    location: str
    assigned_to: Optional[int] = None

class IncidentCreate(IncidentBase):
    pass

class IncidentOut(IncidentBase):
    id: int
    reported_at: Optional[datetime] = None  # allow None if not yet populated

    class Config:
        from_attributes = True

# =========================================================
# ====================== SENSORS =========================
# =========================================================
class SensorBase(BaseModel):
    type: str
    location: str

class SensorCreate(SensorBase):
    name: str

class SensorOut(SensorCreate):
    id: int
    status: Optional[str] = "inactive"
    last_reported_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# =========================================================
# ====================== COURSES =========================
# =========================================================
class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None

class CourseOut(BaseModel):
    id: int
    title: str
    description: Optional[str]

    class Config:
        from_attributes = True

# =========================================================
# ====================== MODULES =========================
# =========================================================
class ModuleCreate(BaseModel):
    title: str
    content: Optional[str] = None

class ModuleOut(BaseModel):
    id: int
    course_id: int
    title: str
    content: Optional[str]

    class Config:
        from_attributes = True

# =========================================================
# ====================== ENROLLMENTS =====================
# =========================================================
class EnrollmentOut(BaseModel):
    id: int
    user_id: int
    course_id: int
    progress: int

    class Config:
        from_attributes = True

class EnrolledCourse(BaseModel):
    course_id: int
    title: str
    description: Optional[str]

class EnrolledCoursesResponse(BaseModel):
    user_id: int
    enrolled_courses: List[EnrolledCourse]

# =========================================================
# ====================== NOTIFICATIONS ==================
# =========================================================
class NotificationBase(BaseModel):
    title: str
    message: str
    recipient: EmailStr

class NotificationCreate(NotificationBase):
    pass

class NotificationOut(BaseModel):
    id: int
    title: str
    message: str
    sent: bool
    target_user_id: Optional[int] = None
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
