
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def inicio():
    return {"mensaje": "Hola mundo"}

# ACA VOY A TENER LOS ENDPOINTS CON LOS VERBOS Y CODIGOS DE ESTADO