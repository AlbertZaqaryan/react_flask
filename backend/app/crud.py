from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas


def get_cars(db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[models.Car]:
    query = db.query(models.Car)
    if search:
        like = f"%{search}%"
        query = query.filter(
            (models.Car.make.ilike(like)) | (models.Car.model.ilike(like))
        )
    return query.order_by(models.Car.id.desc()).offset(skip).limit(limit).all()


def get_car(db: Session, car_id: int) -> Optional[models.Car]:
    return db.query(models.Car).filter(models.Car.id == car_id).first()


def create_car(db: Session, car: schemas.CarCreate) -> models.Car:
    db_car = models.Car(**car.model_dump())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def update_car(db: Session, car_id: int, car: schemas.CarUpdate) -> Optional[models.Car]:
    db_car = get_car(db, car_id)
    if not db_car:
        return None
    for field, value in car.model_dump(exclude_unset=True).items():
        setattr(db_car, field, value)
    db.commit()
    db.refresh(db_car)
    return db_car


def delete_car(db: Session, car_id: int) -> bool:
    db_car = get_car(db, car_id)
    if not db_car:
        return False
    db.delete(db_car)
    db.commit()
    return True
