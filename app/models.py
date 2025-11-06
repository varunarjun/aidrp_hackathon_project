from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime

# =====================================================
# USER TABLE
# =====================================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), default="responder")  # admin, responder, analyst
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    incidents_assigned = relationship(
        "Incident", back_populates="assignee", cascade="all, delete-orphan"
    )
    enrollments = relationship(
        "Enrollment", back_populates="user", cascade="all, delete-orphan"
    )
    notifications_created = relationship(
        "Notification",
        foreign_keys="Notification.created_by",
        back_populates="creator",
        cascade="all, delete-orphan"
    )
    notifications_received = relationship(
        "Notification",
        foreign_keys="Notification.target_user_id",
        back_populates="recipient_user",
        cascade="all, delete-orphan"
    )


# =====================================================
# INCIDENT TABLE
# =====================================================
class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(50), nullable=False)
    location = Column(String(255), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    reported_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    assignee = relationship("User", back_populates="incidents_assigned")


# =====================================================
# SENSOR TABLE
# =====================================================
class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    location = Column(String(255), nullable=False)
    status = Column(String(50), default="active")
    last_reported_at = Column(DateTime(timezone=True), default=func.now(), nullable=True)


# =====================================================
# COURSE TABLE
# =====================================================
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    modules = relationship(
        "Module", back_populates="course", cascade="all, delete-orphan"
    )
    enrollments = relationship(
        "Enrollment", back_populates="course", cascade="all, delete-orphan"
    )


# =====================================================
# MODULE TABLE
# =====================================================
class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    course = relationship("Course", back_populates="modules")
    lessons = relationship(
        "Lesson", back_populates="module", cascade="all, delete-orphan"
    )


# =====================================================
# LESSON TABLE
# =====================================================
class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    video_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    module = relationship("Module", back_populates="lessons")


# =====================================================
# ENROLLMENT TABLE
# =====================================================
class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    progress = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


# =====================================================
# NOTIFICATION TABLE
# =====================================================
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=True)
    message = Column(Text, nullable=True)
    recipient = Column(String(255), nullable=True)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    target_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    recipient_user = relationship(
        "User", foreign_keys=[target_user_id], back_populates="notifications_received"
    )
    creator = relationship(
        "User", foreign_keys=[created_by], back_populates="notifications_created"
    )
