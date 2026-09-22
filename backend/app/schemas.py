from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CarBase(BaseModel):
    make: str = Field(..., min_length=1, max_length=80)
    model: str = Field(..., min_length=1, max_length=80)
    year: int = Field(..., ge=1900, le=2100)
    color: Optional[str] = Field(None, max_length=40)
    price: Decimal = Field(..., ge=0)
    mileage: int = Field(0, ge=0)
    available: bool = True


class CarCreate(CarBase):
    pass


class CarUpdate(BaseModel):
    make: Optional[str] = Field(None, min_length=1, max_length=80)
    model: Optional[str] = Field(None, min_length=1, max_length=80)
    year: Optional[int] = Field(None, ge=1900, le=2100)
    color: Optional[str] = Field(None, max_length=40)
    price: Optional[Decimal] = Field(None, ge=0)
    mileage: Optional[int] = Field(None, ge=0)
    available: Optional[bool] = None


class Car(CarBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
