from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"))
    title = Column(String(255), nullable=False)
    description = Column(String(500))
    video_url = Column(String(255))

    # Relationship (a Lesson belongs to a Module)
    module = relationship("Module", back_populates="lessons")
