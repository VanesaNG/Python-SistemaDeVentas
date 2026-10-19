# ACÁ VOY A TENER LAS CLASES QUE VOY A UTILIZAR DE PRODUCT (PRODUCTO) Y SALE (VENTA)
# ES UNA MEZCLA ENTRE UNA CLASE DE PYTHON Y CÓDIGO DEL ORM PARA ADEMÁS CREAR LAS TABLAS EN LA BASE DE DATOS

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, Time
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("sqlite:///database.db")

Base = declarative_base()

class Product(Base):
    __tablename__= 'products'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    carts = relationship("Cart", secondary="cart_product")


class Sale(Base):
    __tablename__='sales'

    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    id_cart = Column(Integer, ForeignKey("carts.id"), unique=True, nullable=False)
    total_price = Column(Float, nullable=False)

    cart = relationship("Cart", back_populates="cart")


class Cart(Base):
    __tablename__='carts'

    id = Column(Integer, primary_key=True, nullable=False)
    creation_date = Column(Date, nullable=False)
    state = Column(String, nullable=False)

    sale = relationship("Sale", back_populates="cart")
    products = relationship("Product", secondary="cart_product")


class Cart_product(Base):
    __tablename__="cart_product"

    id = Column(Integer, primary_key=True, nullable=False)
    id_cart = Column(ForeignKey("carts.id") ,nullable=False)
    id_product = Column(ForeignKey("products.id") ,nullable=False)
    quantity = Column(Integer, nullable=False)





Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
db_session = SessionLocal()



    # id_product = Column(Integer, ForeignKey("products.id"), nullable=False)
    # quantity = Column(Integer, nullable=False)

    # sales = relationship("Sale", back_populates="product")
    # product = relationship("Product", back_populates="sales")