
# Sistema de Ventas

Proyecto de Seminario de Lenguajes

## Tecnologías
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pandas
- Borb

## Objetivo del trabajo
LABORATORIO 1

El objetivo de este trabajo práctico es desarrollar una API REST que permita gestionar ventas de productos. 
    * Utilizando las operaciones básicas de CRUD.
    * Utilizando la base de datos relacional SQLLite. El manejo de datos se dará a través de un ORM (SQLAlchemy).
    * Y se generaran reportes.

ABM de Producto
Se deberá implementar una API que permita gestionar productos.
Funcionalidades:

    1- Crear un nuevo producto
    2- Obtener el listado de productos registrados en la tabla de base de datos
    3- Obtener un producto en particular
    4- Actualizar los datos de un producto 
    5- eliminar un producto. 

    Para ello, los endpoints serán:
        ● POST /productos
        ● GET /productos
        ● GET /productos/{id}
        ● PUT /productos/{id}
        ● DELETE /productos/{id}

    Los productos deberán contar con los siguientes datos:
        ● id (int pk autoincrement not null)
        ● nombre (str not null)
        ● precio (float not null)



ABM de Ventas
Se deberán implementar nuevos endpoints para gestionar ventas sobre un sólo producto.

Funcionalidades:
    1- crear una nueva venta
    2- Obtener el listado de ventas registrados en la tabla de base de datos. 
    3- obtener una venta en particular
    4- Actualizar los datos de una venta
    5- Eliminar una venta.

    Para ello, los endpoints serán:
        ● POST /ventas
        ● GET /ventas
        ● GET /ventas/{id}
        ● PUT /ventas/{id}
        ● DELETE /ventas/{id}

    Las ventas deberán contar con los siguientes datos:
        ● id (int pk autoincrement not null)
        ● fecha (date not null)
        ● hora (time not null)
        ● id_producto (fk int not null)
        ● cantidad (int not null)
        ● precio_total (float not null)

    El precio total de la venta será calculado por la API tomando el precio unitario del producto y la cantidad de la venta.



LABORATORIO 2

ABM de Carrito
Se deberá implementar una nueva entidad denominada carrito de compras que permita agrupar
productos con sus respectivas cantidades.

Funcionalidades:



    Para ello, los endpoints serán:
        ● POST /carritos
        ● GET /carritos
        ● GET /carritos/{id}
        ● PUT /carritos/{id}
        ● DELETE /carritos/{id}
        ● POST /carritos/{id}/productos
        ● DELETE /carritos/{id}/productos/{id_producto}

    Los carritos deberán contar con los siguientes datos:
        ● id (int pk autoincrement not null)
        ● fecha_creacion (date not null)
        ● estado (str not null) (por ejemplo: "abierto" o "cerrado")


Ventas
Se le agregará un nuevo enpoint:
    ● POST /ventas/{id}/carrito 
    (Este deberá permitir asignar un carrito a una venta o reemplazar el ya asignado; si el carrito se encuentra asociado a otra venta, la API deberá devolver un error.)




RELACIÓN CARRITOS Y PRODUCTOS "carrito_producto"

La relación entre carritos y productos se realiza mediante la tabla carrito_producto, la cual deberá
contar con los siguientes datos:
        ● id (int pk autoincrement not null)
        ● id_carrito (fk int not null)
        ● id_producto (fk int not null)
        ● cantidad (int not null)





REVISAR
1) post("/sale/{sale_id}/cart)
2) 