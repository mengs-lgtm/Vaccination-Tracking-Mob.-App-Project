# backend/crud.py
from datetime import date, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from .models import User, VaccinationRecord, ProfileType
from .schemas import UserCreate, UserUpdate, VaccinationCreate, VaccinationUpdate


# Users
def create_user(db: Session, data: UserCreate) -> User:
    user = User(full_name=data.full_name, profile_type=ProfileType(data.profile_type.value))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.get(User, user_id)


def list_users(db: Session) -> List[User]:
    return db.execute(select(User)).scalars().all()


def update_user(db: Session, user_id: int, data: UserUpdate) -> Optional[User]:
    user = db.get(User, user_id)
    if not user:
        return None
    if data.full_name is not None:
        user.full_name = data.full_name
    if data.profile_type is not None:
        user.profile_type = ProfileType(data.profile_type.value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = db.get(User, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True


# Vaccinations
def create_vaccination(db: Session, data: VaccinationCreate) -> VaccinationRecord:
    record = VaccinationRecord(
        user_id=data.user_id,
        vaccine_name=data.vaccine_name,
        date_administered=data.date_administered,
        next_due_date=data.next_due_date,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_vaccination(db: Session, record_id: int) -> Optional[VaccinationRecord]:
    return db.get(VaccinationRecord, record_id)


def list_vaccinations(db: Session, user_id: Optional[int] = None) -> List[VaccinationRecord]:
    stmt = select(VaccinationRecord)
    if user_id is not None:
        stmt = stmt.where(VaccinationRecord.user_id == user_id)
    return db.execute(stmt).scalars().all()


def update_vaccination(db: Session, record_id: int, data: VaccinationUpdate) -> Optional[VaccinationRecord]:
    record = db.get(VaccinationRecord, record_id)
    if not record:
        return None
    if data.vaccine_name is not None:
        record.vaccine_name = data.vaccine_name
    if data.date_administered is not None:
        record.date_administered = data.date_administered
    if data.next_due_date is not None:
        record.next_due_date = data.next_due_date
    db.commit()
    db.refresh(record)
    return record


def delete_vaccination(db: Session, record_id: int) -> bool:
    record = db.get(VaccinationRecord, record_id)
    if not record:
        return False
    db.delete(record)
    db.commit()
    return True


# Reminder logic: upcoming vaccinations within N days
def list_upcoming_vaccinations(db: Session, within_days: int = 30, user_id: Optional[int] = None) -> List[VaccinationRecord]:
    today = date.today()
    threshold = today + timedelta(days=within_days)
    stmt = select(VaccinationRecord).where(
        VaccinationRecord.next_due_date.isnot(None),
        VaccinationRecord.next_due_date >= today,
        VaccinationRecord.next_due_date <= threshold,
    )
    if user_id is not None:
        stmt = stmt.where(VaccinationRecord.user_id == user_id)
    return db.execute(stmt).scalars().all()
