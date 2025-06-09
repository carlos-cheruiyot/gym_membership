from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base
import re

Base = declarative_base()

class Member(Base):
    __tablename__ = 'members'

    member_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    # One-to-many relationship: a member can have many workout sessions
    workout_sessions = relationship(
        "WorkoutSession",
        back_populates="member",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        return (
            f"<Member(id={self.member_id}, name='{self.full_name}', email='{self.email}')>"
        )

    @validates('email')
    def validate_email(self, key, address):
        if not address:
            raise ValueError("Email is required.")
        # Simple regex email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", address):
            raise ValueError("Invalid email address.")
        return address

    @property
    def full_name(self):
        return f"{self.first_name.strip().title()} {self.last_name.strip().title()}"


class WorkoutSession(Base):
    __tablename__ = 'workout_sessions'

    session_id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey('members.member_id', ondelete='CASCADE'), nullable=False)
    date = Column(Date, nullable=False)
    workout_type = Column(String(50), nullable=False)
    duration_minutes = Column(Integer, nullable=False)  # Duration in minutes

    member = relationship("Member", back_populates="workout_sessions")

    def __repr__(self):
        return (
            f"<WorkoutSession(id={self.session_id}, member_id={self.member_id}, "
            f"date={self.date}, workout_type='{self.workout_type}', "
            f"duration={self.duration_minutes} min)>"
        )

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("Duration must be a positive integer.")
        return duration

    @validates('workout_type')
    def validate_workout_type(self, key, workout_type):
        if not workout_type or not workout_type.strip():
            raise ValueError("Workout type cannot be empty.")
        return workout_type.strip().title()
