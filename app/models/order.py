from pydantic import BaseModel


class OrderCreate(BaseModel):

    harvest_id: str

    quantity_kg: int

    payment_method: str = "efectivo"


class OrderStatusUpdate(BaseModel):

    status: str