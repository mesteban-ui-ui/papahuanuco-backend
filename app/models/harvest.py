from pydantic import BaseModel
from typing import Optional
from datetime import date


class HarvestCreate(BaseModel):

    variety: str
    quantity_kg: int
    price_per_kg: float

    harvest_date: Optional[date] = None
    method: Optional[str] = None
    fertilization: Optional[str] = None

    ciclo_dias: Optional[int] = None
    altitude: Optional[int] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None


class HarvestUpdate(BaseModel):

    quantity_kg: Optional[int] = None
    price_per_kg: Optional[float] = None
    available: Optional[bool] = None