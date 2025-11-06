from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db
from app.auth_utils import get_current_user, get_current_admin_user

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

# ================================================================
# 1️⃣ List all courses (Public)
# ================================================================
@router.get("/", response_model=List[schemas.CourseOut])
def list_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all available courses with pagination"""
    return crud.get_courses(db, skip=skip, limit=limit)


# ================================================================
# 2️⃣ Create a new course (Admin only)
# ================================================================
@router.post("/", response_model=schemas.CourseOut)
def create_course(
    course_in: schemas.CourseCreate,
    db: Session = Depends(get_db),
    admin: schemas.UserOut = Depends(get_current_admin_user)
):
    """Create a new course - Admin only"""
    return crud.create_course(db=db, course_in=course_in)


# ================================================================
# 3️⃣ Add a module to a course (Admin only)
# ================================================================
@router.post("/{course_id}/modules", response_model=schemas.ModuleOut)
def add_module(
    course_id: int,
    module_in: schemas.ModuleCreate,
    db: Session = Depends(get_db),
    admin: schemas.UserOut = Depends(get_current_admin_user)
):
    """Add a module to a specific course - Admin only"""
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    return crud.create_module(db=db, course_id=course_id, module_in=module_in)


# ================================================================
# 4️⃣ Update an existing course (Admin only)
# ================================================================
@router.put("/{course_id}", response_model=schemas.CourseOut)
def update_course(
    course_id: int,
    course_in: schemas.CourseCreate,
    db: Session = Depends(get_db),
    admin: schemas.UserOut = Depends(get_current_admin_user)
):
    """Update course details - Admin only"""
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    updated_course = crud.update_course(db, course_id, course_in.title, course_in.description)
    return updated_course


# ================================================================
# 5️⃣ Delete a course (Admin only)
# ================================================================
@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    admin: schemas.UserOut = Depends(get_current_admin_user)
):
    """Delete a course - Admin only"""
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    crud.delete_course(db, course_id)
    return {"detail": "Course deleted successfully"}


# ================================================================
# 6️⃣ Enroll current user in a course (Authenticated user)
# ================================================================
@router.post("/{course_id}/enroll", response_model=schemas.EnrollmentOut)
def enroll_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(get_current_user)
):
    """Enroll the currently logged-in user in a specific course"""
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    existing = crud.get_enrollment(db, user_id=current_user.id, course_id=course_id)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already enrolled in this course")

    return crud.enroll_user(db=db, user_id=current_user.id, course_id=course_id)


# ================================================================
# 7️⃣ Get all courses the current user is enrolled in
# ================================================================
@router.get("/enrolled", response_model=schemas.EnrolledCoursesResponse)
def get_enrolled_courses(
    current_user: schemas.UserOut = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all courses the currently logged-in user is enrolled in"""
    enrollments = crud.get_user_enrollments(db, user_id=current_user.id)

    enrolled_courses = [
        schemas.EnrolledCourse(
            course_id=e.course.id,
            title=e.course.title,
            description=e.course.description
        )
        for e in enrollments
    ]

    return schemas.EnrolledCoursesResponse(
        user_id=current_user.id,
        enrolled_courses=enrolled_courses
    )
