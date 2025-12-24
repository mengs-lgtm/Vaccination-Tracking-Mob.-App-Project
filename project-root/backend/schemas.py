# backend/schemas.py
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum

class ProfileType(str, Enum):
    child = "child"
    adult = "adult"


# User Schemas
class UserBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    profile_type: ProfileType


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    profile_type: Optional[ProfileType] = None


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True


# Vaccination Schemas
class VaccinationBase(BaseModel):
    user_id: int
    vaccine_name: str = Field(..., min_length=2, max_length=100)
    date_administered: date
    next_due_date: Optional[date] = None


class VaccinationCreate(VaccinationBase):
    pass


class VaccinationUpdate(BaseModel):
    vaccine_name: Optional[str] = Field(None, min_length=2, max_length=100)
    date_administered: Optional[date] = None
    next_due_date: Optional[date] = None


class VaccinationOut(BaseModel):
    id: int
    user_id: int
    vaccine_name: str
    date_administered: date
    next_due_date: Optional[date] = None

    class Config:
        from_attributes = True


# Aggregated responses
class UserWithVaccinations(UserOut):
    vaccinations: List[VaccinationOut] = []
