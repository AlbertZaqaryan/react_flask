from sqlalchemy.orm import Session

from . import models


SAMPLE_CARS = [
    dict(make="Toyota", model="Corolla", year=2021, color="White", price=21500, mileage=18000, available=True),
    dict(make="Tesla", model="Model 3", year=2023, color="Red", price=42990, mileage=5000, available=True),
    dict(make="BMW", model="M3", year=2020, color="Black", price=58900, mileage=27000, available=False),
    dict(make="Honda", model="Civic", year=2022, color="Blue", price=24800, mileage=12000, available=True),
    dict(make="Ford", model="Mustang", year=2019, color="Yellow", price=36500, mileage=41000, available=True),
]


def seed(db: Session) -> None:
    """Insert sample cars only if the table is empty."""
    if db.query(models.Car).count() == 0:
        db.add_all(models.Car(**data) for data in SAMPLE_CARS)
        db.commit()
        print(f"[seed] inserted {len(SAMPLE_CARS)} sample cars")
