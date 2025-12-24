# backend/seed.py
from datetime import date, timedelta
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .models import User, VaccinationRecord, ProfileType

def seed():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    # Clear tables
    db.query(VaccinationRecord).delete()
    db.query(User).delete()
    db.commit()

    child = User(full_name="Kiddo Tesfay", profile_type=ProfileType.CHILD)
    adult = User(full_name="Abeba Hailem", profile_type=ProfileType.ADULT)
    db.add_all([child, adult])
    db.commit()
    db.refresh(child)
    db.refresh(adult)

    db.add_all([
        VaccinationRecord(
            user_id=child.id,
            vaccine_name="MMR",
            date_administered=date.today() - timedelta(days=90),
            next_due_date=date.today() + timedelta(days=15),
        ),
        VaccinationRecord(
            user_id=adult.id,
            vaccine_name="Influenza",
            date_administered=date.today() - timedelta(days=300),
            next_due_date=date.today() + timedelta(days=25),
        ),
        VaccinationRecord(
            user_id=adult.id,
            vaccine_name="Tetanus",
            date_administered=date.today() - timedelta(days=365*9),
            next_due_date=date.today() + timedelta(days=365),  # next year
        ),
    ])
    db.commit()
    db.close()
    print("Seeded sample data.")

if __name__ == "__main__":
    seed()
