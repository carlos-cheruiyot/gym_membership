from sqlalchemy import column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base

import re

Base = declarative_base()

class member(Base):
    __tablename__ = 'members'

    member_id = column(Integer, primary_key=True, autoincrement=True)
    first_name= column(String(50), nullable=False)
    last_name= column(String(50), nullable=False)
    email= column(String(100), unique=True, nullable=False)

    workout_sessions = relationship("workout_session", back_populates="member", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<member(id={self.member_id}, name='{self.first_name} {self.last_name}', email='{self.email}')>"
    



    @validates('email')

    def validate_email (self, key, address):
        if not address:
            raise ValueError("email is required.")
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", address):
            raise ValueError("invalid email address.")
        return address
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    

class workout_session(Base):
    __table__ = 'workout_sessions'

    session_id = column(Integer, primary_key=True, autoincrement=True)
    member_id = column(Integer, ForeignKey('member.member_id'), nullable=False)
    Date = column(Date, nullable=False)
    workout_type = column(String(50), nullable=False)
    duration_minutes = column(Integer, nullable=False)


    member = relationship("member", back_populates="workout_sessions")

    def __repr__(self):
        return f"<workoutsessions(id={self.session_id}, member_id={self.member_id}, date={self.Date}, type='{self.workout_type}', duration={self.duration_minutes}min)>"
    

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration <= 0:
            raise ValueError("duration must be positive.")
        return duration
    

    @validates('workout_type')
    def validate_workout_type(self, key, workout_type):
        if not workout_type or not workout_type.strip():
            raise ValueError("workout type cannot be empty.")
        return workout_type.strip() 


