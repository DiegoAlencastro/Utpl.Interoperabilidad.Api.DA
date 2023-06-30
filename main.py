from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid

from fastapi_versioning import VersionedFastAPI, version

from fastapi.security import HTTPBasic, HTTPBasicCredentials

from auth import authenticate

#seccion mongo_importar libreria
import pymongo


description = """
Interoperabilidad Actualizacion Datos Cliente. 🚀

## Cliente

Se actuliza datos cliente.
Detalle de clientes.

"""
tags_metadata = [
    {
        "name":"clientes",
        "description":"Actualizacion Datos Cliente"
    }
]
app = FastAPI(
    title="Interoperabilidad Actualizacion Datos Cliente",
    description= description,
    version="tarea4",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Diego Alencastro",
        "url": "https://github.com/DiegoAlencastro/Utpl.Interoperabilidad.Api.DA.git",
        "email": "dialencastro@utpl.edu.ec",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags = tags_metadata  
)

#para agregar seguridad a nuestro api
security = HTTPBasic()


#configuracion de mongo
cliente = pymongo.MongoClient("mongodb+srv://utplda:s4nN15Zcbf5W0D5v@cluster0.po6e08w.mongodb.net/?retryWrites=true&w=majority")
database = cliente["clientes"]
coleccion = database["datos"]

class Cliente (BaseModel):
    orden: int
    nombre: str
    edad: int
    agencia: Optional[str] = None
    cuenta: int


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

personasList = []

@app.post("/clientes", response_model=ClienteRepositorio, tags = ["clientes"])
@version(1,0)
async def crear_cliente(clientE: ClienteEntradaEntrada):
    print ('llego')
    clientE.apellido, edad = clientE.edad, oficina = clientE.oficina)
    resultadoDB =  coleccion.insert_one(itemCliente.dict())
    return itemCliente

@app.get("/clientes", response_model=List[ClienteRepositorio], tags=["clientes"])
@version(1,0)
def get_clientes():
    itemsCliente = list(coleccion.find())
    print (items)
    return itemsCliente

## Buscar Cliente
@app.get("/clientes/{cliente_id}", response_model=ClienteRepositorio, tags=["clientes"])
@version(1,0)
def obtener_cliente (cliente_id: str):
    item = coleccion.find_one({"id": persona_id})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Cliente no Existe")

## Identificar Cliente por codigo.    
@app.get("/Cliente/codigo/{cod_num}", response_model=Huesped, tags = ["clientes"])
@version(2,0)
def obtener_cod(cod_num: int):
    item = coleccion.find_one({"cod": cod_num})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Cliente no Existe")

    ##codigo Sin Existencia
    
@app.delete("/clientes/{cliente_id}", tags=["clientes"])
@version(1,0)
def eliminar_cliente (cliente_id: str):
    result = coleccion.delete_one({"id": cliente_id})
    if result.deleted_count == 1:
        return {"mensaje": "Eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Cliente no Existe")

@app.get("/")
@version(1,0)
def read_root():
    return {"Hello": "Tarea Concluida APP Cliente DA"}


app = VersionedFastAPI(app)