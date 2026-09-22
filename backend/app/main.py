from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, SessionLocal, engine, get_db, wait_for_db
from .seed import seed

app = FastAPI(title="Cars API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    wait_for_db()
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/cars", response_model=List[schemas.Car])
def list_cars(
    skip: int = 0,
    limit: int = Query(100, le=500),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_cars(db, skip=skip, limit=limit, search=search)


@app.get("/api/cars/{car_id}", response_model=schemas.Car)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = crud.get_car(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@app.post("/api/cars", response_model=schemas.Car, status_code=201)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    return crud.create_car(db, car)


@app.put("/api/cars/{car_id}", response_model=schemas.Car)
def update_car(car_id: int, car: schemas.CarUpdate, db: Session = Depends(get_db)):
    updated = crud.update_car(db, car_id, car)
    if not updated:
        raise HTTPException(status_code=404, detail="Car not found")
    return updated


@app.delete("/api/cars/{car_id}", status_code=204)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    if not crud.delete_car(db, car_id):
        raise HTTPException(status_code=404, detail="Car not found")
    return None
