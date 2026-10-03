
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
