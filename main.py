from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Cliente (BaseModel):
    orden: int
    nombre: str
    edad: int
    agencia: Optional[str] = None
    cuenta: int

clienteList = []

@app.post("/clientes", response_model=Cliente)
def crear_cliente(client: Cliente):
    clienteList.append(client)
    return client

@app.get("/clientes", response_model=List[Cliente])
def get_clientes():
    return clienteList

@app.get("/clientespersonas/{cliente_orden}", response_model=Cliente)
def obtener_cliente (cliente_orden: int):
    for cliente in clienteList:
        if cliente.orden == cliente_orden:
            return cliente
    raise HTTPException(status_code=404, detail="Cliente no registrado")

@app.get("/")
def read_root():
    return {"Hello": "Interoperabilidad 2"}
