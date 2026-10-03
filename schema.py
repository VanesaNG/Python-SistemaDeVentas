# FastAPI usa tipado en lo que es la respuesta y los modelos de datos 
# Yo le tengo que decir a cada endpoint que es lo que va a estar recibiendo y que es lo que va a estar devolviendo

from pydantic import BaseModel
from datetime import date, time

class ProductCreate(BaseModel):
    name: str
    price: float

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True

class SaleCreate(BaseModel):
    date: date
    time: time
    id_product: int
    quantity: int

    class Config:
        from_attributes = True


class SaleResponse(BaseModel):
    id: int
    date: date
    time: time
    product: ProductResponse
    quantity: int
    total_price: float

    class Config:
        from_attributes = True




