# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session 

from backend.database import Base, engine, get_db
from backend.models import User, VaccinationRecord
from backend.schemas import (
    UserCreate, UserUpdate, UserOut, UserWithVaccinations,
    VaccinationCreate, VaccinationUpdate, VaccinationOut
)
import backend.crud

app = FastAPI(title="Vaccination Tracking API", version="1.0.0")

# Create tables
Base.metadata.create_all(bind=engine)

# Configure CORS for Flutter local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        # Add your Flutter emulator / device origin if needed
        "*",  # loosen for mobile dev; tighten in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}


# --- Users ---
@app.post("/users", response_model=UserOut, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, data)


@app.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud.list_users(db)


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return None


@app.get("/users/{user_id}/with-vaccinations", response_model=UserWithVaccinations)
def get_user_with_vaccinations(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "full_name": user.full_name,
        "profile_type": user.profile_type.value,
        "vaccinations": user.vaccinations,
    }


# --- Vaccination Records ---
@app.post("/vaccinations", response_model=VaccinationOut, status_code=201)
def create_vaccination(data: VaccinationCreate, db: Session = Depends(get_db)):
    # Ensure user exists
    user = crud.get_user(db, data.user_id)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    return crud.create_vaccination(db, data)


@app.get("/vaccinations", response_model=list[VaccinationOut])
def list_vaccinations(user_id: int | None = Query(default=None), db: Session = Depends(get_db)):
    return crud.list_vaccinations(db, user_id=user_id)


@app.get("/vaccinations/{record_id}", response_model=VaccinationOut)
def get_vaccination(record_id: int, db: Session = Depends(get_db)):
    record = crud.get_vaccination(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


@app.put("/vaccinations/{record_id}", response_model=VaccinationOut)
def update_vaccination(record_id: int, data: VaccinationUpdate, db: Session = Depends(get_db)):
    record = crud.update_vaccination(db, record_id, data)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


@app.delete("/vaccinations/{record_id}", status_code=204)
def delete_vaccination(record_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_vaccination(db, record_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Record not found")
    return None


# --- Reminders / Upcoming ---
@app.get("/vaccinations/upcoming", response_model=list[VaccinationOut])
def upcoming_vaccinations(
    within_days: int = Query(default=30, ge=1, le=365),
    user_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return crud.list_upcoming_vaccinations(db, within_days=within_days, user_id=user_id)
