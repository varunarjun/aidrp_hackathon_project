# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import datetime
from typing import Optional, List

from app import models, schemas, auth  # auth.py handles password hashing/verification


# =========================================================
# USER OPERATIONS
# =========================================================
def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Fetch user by email"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    """Fetch user by ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(
    db: Session,
    email: str,
    password: str,
    full_name: Optional[str] = None,
    role: str = "student"
) -> models.User:
    """Create a new user with hashed password"""
    try:
        hashed_password = auth.get_password_hash(password)
        user = models.User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
            created_at=datetime.utcnow()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )


def update_user(db: Session, db_user: models.User, user_in: schemas.UserCreate) -> models.User:
    """Update user details"""
    db_user.email = user_in.email
    db_user.full_name = user_in.full_name
    db_user.role = user_in.role
    if user_in.password:
        db_user.hashed_password = auth.get_password_hash(user_in.password)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: models.User):
    """Delete a user"""
    db.delete(db_user)
    db.commit()


def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    """Authenticate user with email and password"""
    user = get_user_by_email(db, email)
    if not user or not auth.verify_password(password, user.hashed_password):
        return None
    return user


# =========================================================
# COURSE OPERATIONS
# =========================================================
def create_course(db: Session, course_in: schemas.CourseCreate) -> models.Course:
    """Create a new course"""
    try:
        course = models.Course(
            title=course_in.title,
            description=course_in.description,
            created_at=datetime.utcnow()
        )
        db.add(course)
        db.commit()
        db.refresh(course)
        return course
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course creation failed"
        )


def get_course(db: Session, course_id: int) -> Optional[models.Course]:
    """Get a single course by ID"""
    return db.query(models.Course).filter(models.Course.id == course_id).first()


def get_courses(db: Session, skip: int = 0, limit: int = 100) -> List[models.Course]:
    """Get all courses with pagination"""
    return db.query(models.Course).offset(skip).limit(limit).all()


def update_course(db: Session, course_id: int, title: str, description: Optional[str]) -> models.Course:
    """Update an existing course"""
    course = get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    course.title = title
    course.description = description
    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, course_id: int) -> None:
    """Delete a course"""
    course = get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    db.delete(course)
    db.commit()


# =========================================================
# MODULE OPERATIONS
# =========================================================
def create_module(db: Session, course_id: int, module_in: schemas.ModuleCreate) -> models.Module:
    """Add a module to an existing course"""
    course = get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    try:
        module = models.Module(
            course_id=course_id,
            title=module_in.title,
            content=module_in.content,
            created_at=datetime.utcnow()
        )
        db.add(module)
        db.commit()
        db.refresh(module)
        return module
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create module for course {course_id}"
        )


def get_module(db: Session, module_id: int) -> Optional[models.Module]:
    """Get a single module by ID"""
    return db.query(models.Module).filter(models.Module.id == module_id).first()


def update_module(db: Session, module_id: int, title: str, content: str) -> models.Module:
    """Update a module"""
    module = get_module(db, module_id)
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    module.title = title
    module.content = content
    db.commit()
    db.refresh(module)
    return module


def delete_module(db: Session, module_id: int):
    """Delete a module"""
    module = get_module(db, module_id)
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    db.delete(module)
    db.commit()


# =========================================================
# ENROLLMENT OPERATIONS
# =========================================================
def enroll_user(db: Session, user_id: int, course_id: int) -> models.Enrollment:
    """Enroll a user into a course"""
    existing = get_enrollment(db, user_id, course_id)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already enrolled")
    try:
        enrollment = models.Enrollment(
            user_id=user_id,
            course_id=course_id,
            progress=0,
            created_at=datetime.utcnow()
        )
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        return enrollment
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Enrollment failed"
        )


def get_enrollment(db: Session, user_id: int, course_id: int) -> Optional[models.Enrollment]:
    """Check if user is already enrolled"""
    return (
        db.query(models.Enrollment)
        .filter(models.Enrollment.user_id == user_id, models.Enrollment.course_id == course_id)
        .first()
    )


def get_user_enrollments(db: Session, user_id: int) -> List[models.Enrollment]:
    """Fetch all enrollments for a user"""
    return db.query(models.Enrollment).filter(models.Enrollment.user_id == user_id).all()


# =========================================================
# NOTIFICATION OPERATIONS
# =========================================================
def create_notification(
    db: Session, title: str, message: str, recipient: Optional[str] = None
) -> models.Notification:
    """Create a new notification"""
    try:
        notification = models.Notification(
            title=title,
            message=message,
            recipient=recipient,
            sent=False,
            created_at=datetime.utcnow()
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Notification creation failed"
        )


def mark_notification_sent(db: Session, notification_id: int) -> models.Notification:
    """Mark a notification as sent"""
    notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification {notification_id} not found"
        )
    notification.sent = True
    db.commit()
    db.refresh(notification)
    return notification


def get_all_notifications(db: Session) -> List[models.Notification]:
    """Fetch all notifications"""
    return db.query(models.Notification).all()


def get_notification(db: Session, notification_id: int) -> Optional[models.Notification]:
    """Fetch a single notification"""
    return db.query(models.Notification).filter(models.Notification.id == notification_id).first()


def delete_notification(db: Session, notification_id: int):
    """Delete a notification"""
    notification = get_notification(db, notification_id)
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    db.delete(notification)
    db.commit()
