# backend/models.py
from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from .database import Base

class ProfileType(PyEnum):
    CHILD = "child"
    ADULT = "adult"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    profile_type = Column(Enum(ProfileType), nullable=False)

    vaccinations = relationship("VaccinationRecord", back_populates="user", cascade="all, delete-orphan")


class VaccinationRecord(Base):
    __tablename__ = "vaccination_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vaccine_name = Column(String, nullable=False)
    date_administered = Column(Date, nullable=False)
    next_due_date = Column(Date, nullable=True)  # nullable for single-dose or unknown schedules

    user = relationship("User", back_populates="vaccinations")
