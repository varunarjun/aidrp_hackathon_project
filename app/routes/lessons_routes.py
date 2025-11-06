from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/lessons", tags=["Lessons"])

# ✅ Create a new lesson under a specific module
@router.post("/modules/{module_id}", response_model=schemas.LessonResponse)
def create_lesson(
    module_id: int,
    lesson_data: schemas.LessonCreate,
    db: Session = Depends(get_db)
):
    # Check if module exists
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    # Create new lesson
    new_lesson = models.Lesson(
        module_id=module_id,
        title=lesson_data.title,
        description=lesson_data.description,
        video_url=lesson_data.video_url
    )

    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)

    return new_lesson


# ✅ Get all lessons under a specific module
@router.get("/modules/{module_id}", response_model=list[schemas.LessonResponse])
def get_lessons(module_id: int, db: Session = Depends(get_db)):
    lessons = db.query(models.Lesson).filter(models.Lesson.module_id == module_id).all()
    if not lessons:
        raise HTTPException(status_code=404, detail="No lessons found for this module")
    return lessons
