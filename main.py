from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

#seccion mongo importar libreria
import pymongo

app = FastAPI()

class Cliente (BaseModel):
    orden: int
    nombre: str
    edad: int
    agencia: Optional[str] = None
    cuenta: int

#configuracion de mongo
cliente = pymongo.MongoClient("mongodb+srv://utplda:s4nN15Zcbf5W0D5v@cluster0.po6e08w.mongodb.net/?retryWrites=true&w=majority")
database = cliente["clientes"]
coleccion = database["datos"]
clienteList = []

class ClienteRepositorio (BaseModel):
    id: str
    nombre: str
    apellido: str
    edad: int
    oficina: Optional[str] = None

class ClienteEntrada (BaseModel):
    id: str
    nombre: str
    apellido: str
    edad: int
    oficina: Optional[str] = None


clienteList = []

@app.post("/clientes", response_model=ClienteRepositorio, tags = ["clientes"])
async def crear_cliente(clientE: ClienteEntradaEntrada):
    itemPersona = ClienteRepositorio (id= str(uuid.uuid4()), nombre = clientE.nombre, apellido = clientE.apellido, edad = clientE.edad, oficina = clientE.oficina)
    resultadoDB =  coleccion.insert_one(itemCliente.dict())
    return itemCliente

@app.get("/clientes", response_model=List[ClienteRepositorio], tags=["clientes"])
def get_clientes():
    items = list(coleccion.find())
    print (items)
    return items

@app.get("/clientes/{cliente_id}", response_model=ClienteRepositorio, tags=["clientes"])
def obtener_cliente (cliente_id: str):
    item = coleccion.find_one({"id": persona_id})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Cliente no Existe")

@app.delete("/clientes/{cliente_id}", tags=["clientes"])
def eliminar_cliente (cliente_id: str):
    result = coleccion.delete_one({"id": cliente_id})
    if result.deleted_count == 1:
        return {"mensaje": "Eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Cliente no Existe")

@app.get("/pista/{pista_id}", tags = ["artistas"])
async def obtener_pista(pista_id: str):
    track = sp.track(pista_id)
    return track
    
@app.get("/artistas/{artista_id}", tags = ["artistas"])
async def get_artista(artista_id: str):
    artista = sp.artist(artista_id)
    return artista


@app.get("/")
def read_root():
    return {"Hello": "Tarea Concluida"}