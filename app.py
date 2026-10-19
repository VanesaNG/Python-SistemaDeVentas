
from fastapi import FastAPI, status, HTTPException
from database import db_session, Product, Sale, Cart
from schema import ProductCreate, SaleCreate, SaleResponse, ProductResponse, CartAssign, CartResponse, CartCreate
from sqlalchemy import Time, Date

app = FastAPI()

@app.get("/")
def inicio():
    return {"mensaje": "Hola mundo"}

# ACA VOY A TENER LOS ENDPOINTS CON LOS VERBOS Y CODIGOS DE ESTADO

####  ENDPOINTS PRODUCTOS

# ENDPOINT QUE CREA UN NUEVO PRODUCTO
@app.post("/product", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def create_product(product_details: ProductCreate):

    try:
        product = db_session.query(Product).filter(Product.name == product_details.name).first()

        if product:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product already exists")

        product = Product(
            name= product_details.name,
            price= product_details.price
        )

        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error al crear producto: {e}")
    
    return product


# ENDPOINT QUE OBTIENE UN PRODUCTO EN PARTICULAR
@app.get("/product/{product_id}", status_code=status.HTTP_200_OK)
def get_product(product_id: int):

    product = db_session.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="El producto no fue encontrado")
    
    return product


# ENDPOINT QUE OBTIENE EL LISTADO DE PRODUCTOS
@app.get("/products", status_code=status.HTTP_200_OK, response_model=list[ProductResponse])
def get_products():

    products = db_session.query(Product).all()

    return products



# ENDPOINT QUE ACTUALIZA LOS DATOS DE UN PRODUCTO
@app.put("/product/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
def update_product(product_id: int, product_details: ProductCreate):


    try:
        product = db_session.query(Product).filter(Product.id == product_id).first()

        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

        product.name = product_details.name
        product.price = product_details.price

        db_session.commit()
        db_session.refresh(product)

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error al modificar el producto: {e}")

    return product



# ENDPOINT QUE ELIMINA UN PRODUCTO
@app.delete("/product/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteProduct(product_id: int):

    try:

        product = db_session.query(Product).filter(Product.id == product_id).first()

        if product is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        db_session.delete(product)
        db_session.commit()

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"Error al eliminar el producto: {e}")



####  ENDPOINTS PRODUCTOS

    # ENDPOINT QUE CREA UNA NUEVA VENTA
@app.post("/sale",status_code= status.HTTP_201_CREATED, response_model=SaleResponse)
def createSale(sale_details: SaleCreate):
    try:

        product = db_session.query(Product).filter(Product.id == sale_details.id_product).first()

        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe el producto")

        sale = Sale(
            time = sale_details.time,
            date = sale_details.date,
            id_cart = sale_details.id_cart,
            total_price = 0
        )

        db_session.add(sale)
        db_session.commit()
        db_session.refresh(sale)

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error al crear la venta: {e}")

    return sale

    # ENDPOINT QUE OBTIENE EL LISTADO DE VENTAS
@app.get("/sales", status_code=status.HTTP_200_OK, response_model=list[SaleResponse])
def getSales():

    sales = db_session.query(Sale).all()


    for sale in sales:
        print(sale.id_product, sale.product)
    return sales



    # ENDPOINT QUE OBTIENE UNA VENTA EN PARTICULAR
@app.get("/sale/{sale_id}", status_code=status.HTTP_200_OK, response_model=SaleResponse)
def getSale(sale_id:int):
    sale = db_session.query(Sale).filter(Sale.id == sale_id).first()

    if sale is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail="No se encontró la venta")

    return sale


    
    # ENDPOINT QUE ACTUALIZA LOS DATOS DE UNA VENTA
@app.put("/sale/{sale_id}", status_code=status.HTTP_200_OK, response_model=SaleResponse)
def updateSale(sale_id: int, sale_details:SaleCreate):

    try:
        sale = db_session.query(Sale).filter(Sale.id == sale_id).first()

        if sale is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail="Venta no encontrada")

        sale.date = sale_details.date
        sale.time = sale_details.time
        sale.id_product = sale_details.id_product
        sale.quantity = sale_details.quantity

        db_session.commit()
        db_session.refresh(sale)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"No se pudo modificar la venta. Error: {e}")

    return sale



    # ENDPOINT QUE ELIMINA UNA VENTA
@app.delete("/sale/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteSale(sale_id:int):
    try:
        sale = db_session.query(Sale).filter(Sale.id == sale_id).first()

        if sale is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada")

        db_session.delete(sale)
        db_session.commit()

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error al eliminar la venta {e}")




 #######REVISAAAAAAAAAAAAAAAAARR####### 1

    # ENDPOINT QUE LE ASIGNA O REEMPLAZA UN CARRITO DE UNA VENTA

@app.post("/sale/{sale_id}/cart", status_code=status.HTTP_200_OK, response_model=SaleResponse)
def assignCart(sale_id:int, cart_details:CartAssign):
    try:
        cart = db_session.query(Cart).filter( Cart.id == cart_details.id_cart).first()

        if cart.sale is not None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="El carrito ya está asociado a una venta")

        sale = db_session.query(Sale).filter( Sale.id == sale_id ).first()

        sale.id_cart = cart_details.id_cart

        db_session.commit()
        db_session.refresh(sale)

    except HTTPException:
        raise


    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"No se pudo asignar el carrito a la venta. Error: {e}")

    return sale

    # POST /carritos
    # ENDPOINT QUE CREA UN CARRITO
@app.post("/cart", status_code=status.HTTP_200_OK, response_model=CartResponse)
def createCart(cart_details:CartCreate):

    try:
        cart = Cart (
            creation_date = cart_details.creation_date,
            state = cart_details.state
        )

        db_session.add(Cart)
        db_session.commit()

    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error al crear carrito: {e}")

    return cart



    # GET /carritos
    # GET /carritos/{id}
    # PUT /carritos/{id}
    # DELETE /carritos/{id}
    # POST /carritos/{id}/productos
    # DELETE /carritos/{id}/productos/{id_producto}

    







# CONTROL K CONTROL C
# CONTROL K CONTROL U