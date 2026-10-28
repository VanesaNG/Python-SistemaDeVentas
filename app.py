
from fastapi import FastAPI, status, HTTPException
from database import db_session, Product, Sale, Cart, Cart_product
from schema import ProductCreate, SaleCreate, SaleResponse, ProductResponse, CartAssign, CartResponse, CartCreate, addProduct
from sqlalchemy import Time, Date

app = FastAPI()



### ENDPOINTS PRODUCTOS ------------------------------------------------------------------

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


# ENDPOINT QUE OBTIENE EL LISTADO DE PRODUCTOS
@app.get("/products", status_code=status.HTTP_200_OK, response_model=list[ProductResponse])
def get_products():

    products = db_session.query(Product).all()

    return products


# ENDPOINT QUE OBTIENE UN PRODUCTO EN PARTICULAR
@app.get("/product/{product_id}", status_code=status.HTTP_200_OK)
def get_product(product_id: int):

    product = db_session.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="El producto no fue encontrado")
    
    return product


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

        productInCart = db_session.query(Cart_product).filter(Cart_product.id_product == product_id).first()

        if productInCart is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar un producto que esté registrado en un carrito")

        db_session.delete(product)
        db_session.commit()

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=f"Error al eliminar el producto: {e}")



### ENDPOINTS VENTAS ---------------------------------------------------------------------------------

# ENDPOINT QUE CREA UNA NUEVA VENTA
@app.post("/sale",status_code= status.HTTP_201_CREATED, response_model=SaleResponse)
def createSale(sale_details: SaleCreate):
    try:

        cart = db_session.query(Cart).filter(Cart.id == sale_details.id_cart).first()

        if cart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="El carrito no existe")

        if cart.state != "cerrado":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="El carrito debe estar cerrado para crear la venta")

        if cart.sale is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="El carrito se encuentra asociado a otra venta")

        items = db_session.query(Cart_product).filter(Cart_product.id_cart == sale_details.id_cart).all()

        total = 0
        for item in items:
            total += item.product.price * item.quantity


        sale = Sale(
            time = sale_details.time,
            date = sale_details.date,
            id_cart = sale_details.id_cart,
            total_price = total
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


# ENDPOINT QUE LE ASIGNA O REEMPLAZA UN CARRITO DE UNA VENTA
@app.post("/sale/{sale_id}/cart", status_code=status.HTTP_200_OK, response_model=SaleResponse)
def assignCart(sale_id:int, cart_details:CartAssign):
    try:

        sale = db_session.query(Sale).filter( Sale.id == sale_id ).first()

        if sale is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="La venta no existe")

        cart = db_session.query(Cart).filter( Cart.id == cart_details.id_cart).first()

        if cart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="El carrito no existe")

        if cart.sale is not None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="El carrito ya está asociado a una venta")

        if cart.state != "cerrado":
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="El carrito debe encontrarse cerrado para asociarlo a la venta")

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



### ENDPOINTS CARRITOS ------------------------------------------------------------------------------

# ENDPOINT QUE CREA UN CARRITO
@app.post("/cart", status_code=status.HTTP_200_OK, response_model=CartResponse)
def createCart(cart_details:CartCreate):

    try:
        cart = Cart (
            creation_date = cart_details.creation_date,
            state = cart_details.state
        )

        db_session.add(cart)
        db_session.commit()

    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error al crear carrito: {e}")

    return cart


# ENDPOINT QUE DEVUELVE UNA LISTA DE CARRITOS
@app.get("/carts", status_code=status.HTTP_200_OK, response_model=list[CartResponse])
def getCarts():

    carts = db_session.query(Cart).all()

    return carts

    
# ENDPOINT QUE DEVUELVE UN CARRITO EN PARTICULAR
@app.get("/cart/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartResponse)
def getCart(cart_id:int):

    cart = db_session.query(Cart).filter(Cart.id == cart_id).first()

    if cart is None:
        raise HTTPException(status_code=404, detail="El carrito no fue encontrado")
    
    return cart


# ENDPOINT QUE MODIFICA UN CARRITO
@app.put("/cart/{cart_id}", status_code=status.HTTP_200_OK, response_model=CartResponse)
def updateCart(cart_id: int, cart_details: CartCreate):

    try:
        cart = db_session.query(Cart).filter(Cart.id == cart_id).first()

        if cart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrito no encontrado")

        if cart.sale is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="El carrito no puede ser modificado porque está asociado a una venta")

        if cart.state == "cerrado" and cart_details.state == "abierto":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="No se puede volver a abrir un carrito ya cerrado")


        cart.creation_date = cart_details.creation_date
        cart.state = cart_details.state

        db_session.commit()
        db_session.refresh(cart)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"No se pudo modificar el carrito. Error: {e}")

    return cart


# ENDPOINT QUE ELIMINA UN CARRITO
@app.delete("/cart/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteCart(cart_id:int):
    try:
        cart = db_session.query(Cart).filter(Cart.id == cart_id).first()

        if cart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrito no encontrado")

        print("ID del carrito:", cart.id)
        print("Venta asociada:", cart.sale)
        if cart.sale is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar un carrito asociado a una venta")

        db_session.delete(cart)
        db_session.commit()

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"No se pudo eliminar el carrito, error: {e}")


# ENDPOINT QUE AGREGA UN PRODUCTO AL CARRITO
@app.post("/cart/{cart_id}/product", status_code=status.HTTP_200_OK, response_model=CartResponse)
def addProductToCart(cart_id: int, product_details:addProduct):
    try:

        cart = db_session.query(Cart).filter(Cart.id == cart_id).first()

        if cart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="El carrito no existe")

        if cart.state != "abierto":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pueden agregar productos a un carrito cerrado")

        product = db_session.query(Product).filter(Product.id == product_details.id_product).first()

        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="El producto no existe")

        product_cart = db_session.query(Cart_product).filter(
            Cart_product.id_cart == cart_id,
            Cart_product.id_product == product_details.id_product
        ).first()

        if product_cart is None:

            product_cart = Cart_product(
                id_cart = cart_id,
                id_product = product_details.id_product,
                quantity = product_details.quantity
            )

            db_session.add(product_cart)
        else:

            product_cart.quantity = product_cart.quantity + product_details.quantity

        db_session.commit()
        db_session.refresh(cart)

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"No se ha podido cargar el producto al carrito. Error: {e}")

    return cart
    
    
# ENDPOINT QUE ELIMINA UN PRODUCTO DEL CARRITO
@app.delete("/cart/{cart_id}/product/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def deteleProducCart(cart_id:int, product_id:int):
     
    try:   
        cart = db_session.query(Cart).filter(Cart.id == cart_id).first()

        if cart is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró el carrito")

        if cart.state != "abierto":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar un producto de un carrito cerrado")

        product = db_session.query(Cart_product).filter(
            Cart_product.id_cart == cart_id, Cart_product.id_product == product_id
        ).first()

        if product is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="El producto no se encontró en el carrito")

        db_session.delete(product)
        db_session.commit()


    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"No se pudo eliminar el producto del carrito. Error: {e}")