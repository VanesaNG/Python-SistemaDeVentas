# FastAPI usa tipado en lo que es la respuesta y los modelos de datos 
# Yo le tengo que decir a cada endpoint que es lo que va a estar recibiendo y que es lo que va a estar devolviendo

from pydantic import BaseModel, Field
from datetime import date, time

class ProductCreate(BaseModel):
    name: str
    price: float

    class Config:
        from_attributes = True

# Pydantic espera normalmente recibir un diccionario
# CLASS CONFIG le dice a pydantic
# Podés crear este esquema a partir de los atributos de un objeto Python/SQLAlchemy.
# Porque SQLAlchemy te responde con un objeto


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True

class SaleCreate(BaseModel):
    date: date
    time: time
    id_cart: int

    class Config:
        from_attributes = True

class CartProductResponse(BaseModel):
    id: int
    product: ProductResponse
    quantity: int


class CartCreate(BaseModel):
    creation_date: date
    state: str


class CartResponse(BaseModel):
    id: int
    creation_date: date
    state: str
    products: list[CartProductResponse]

    class Config:
        from_attributes = True


class SaleResponse(BaseModel):
    id: int
    date: date
    time: time
    total_price: float
    cart: CartResponse

    class Config:
        from_attributes = True


class CartAssign(BaseModel):
    id_cart: int


class addProduct(BaseModel):
    id_product: int
    quantity: int = Field(gt=0)