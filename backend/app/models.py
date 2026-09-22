from sqlalchemy import Boolean, Column, Integer, Numeric, String

from .database import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String(80), nullable=False, index=True)
    model = Column(String(80), nullable=False)
    year = Column(Integer, nullable=False)
    color = Column(String(40), nullable=True)
    price = Column(Numeric(10, 2), nullable=False, default=0)
    mileage = Column(Integer, nullable=False, default=0)
    available = Column(Boolean, nullable=False, default=True)
