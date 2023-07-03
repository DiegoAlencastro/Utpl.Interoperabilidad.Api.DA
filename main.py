from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid
import pymongo

from fastapi_versioning import VersionedFastAPI, version
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from auth import authenticate

#seccion mongo_importar libreria
cliente = pymongo.MongoClient("mongodb+srv://utplda:s4nN15Zcbf5W0D5v@cluster0.po6e08w.mongodb.net/?retryWrites=true&w=majority")
database = cliente["clientes"]
coleccion = database["datos"]


description = """
Interoperabilidad Actualizacion Datos Cliente. 🚀

## Cliente

Se actuliza datos cliente.
Detalle de clientes.

"""
tags_metadata = [
    {
        "name":"cliente",
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
        "url": "https://github.com/familiaerba/Utpl.Interoperabilidad.Api.git",
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

class ClienteRepositorio (BaseModel):
    id: str
    nombre: str
    cantPro: int
    cedula: Optional[str] = None
    ciudad: Optional[str] = None

class ClienteEntrada (BaseModel):
    nombre:str
    cantPro:int
    ciudad: Optional[str] = None

class ClienteEntradaV2 (BaseModel):
    nombre:str
    cantPro:int
    cedula:str
    ciudad: Optional[str] = None




clienteList = []

@app.post("/cliente", response_model=ClienteRepositorio, tags = ["cliente"])
@version(1, 0)
async def crear_cliente(clienteE: ClienteEntrada):
    itemcliente = ClienteRepositorio (id= str(uuid.uuid4()), nombre = clienteE.nombre, cantPro = clienteE.cantPro, ciudad = clienteE.ciudad)
    resultadoDB =  coleccion.insert_one(itemcliente.dict())
    return itemcliente

@app.post("/cliente", response_model=ClienteRepositorio, tags = ["cliente"])
@version(2, 0)
async def crear_Clientev2(clienteE: ClienteEntradaV2):
    itemcliente = ClienteRepositorio (id= str(uuid.uuid4()), nombre = personE.nombre, cantPro = personE.cantPro, ciudad = personE.ciudad, cedula = personE.cedula)
    resultadoDB =  coleccion.insert_one(itemcliente.dict())
    return itemcliente

## Buscar Cliente
@app.get("/client", response_model=List[ClienteRepositorio], tags = ["clientes"])
@version(1,0)
def get_cliente():
    return clienteList

## Identificar Cliente por codigo.
@app.get("/client/{cedula_id}", response_model=ClienteRepositorio, tags = ["clientes"])
@version(1,0)
def obtener_Cliente (cedula_id: int):
    for comprador in clienteList:
        if cedula == cedula:
            return comprador
    raise HTTPException(status_code=404, detail="Cliente no encontrado")
@app.get("/Cliente", response_model=List[ClienteRepositorio], tags=["Cliente"])
@version(1, 0)
def get_Cliente(credentials: HTTPBasicCredentials = Depends(security)):
    authenticate(credentials)
    items = list(coleccion.find())
    print (items)
    return items

@app.get("/Cliente/{Cliente_id}", response_model=ClienteRepositorio , tags=["Ciente"])
@version(1, 0)
def obtener_Cliente (Cliente_id: str):
    item = coleccion.find_one({"id": Cliente_id})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrada")

  ##codigo Sin Existencia
@app.delete("/Cliente/{Cliente_id}", tags=["Cliente"])
@version(1, 0)
def eliminar_Cliente (Cliente_id: str):
    result = coleccion.delete_one({"id": Cliente_id})
    if result.deleted_count == 1:
        return {"mensaje": "Cliente eliminada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrada")

@app.get("/Cliente/{Cliente_id}", tags = ["Cliente"])
@version(1, 0)
async def obtener_pista(Cliente_id: str):
    track = sp.track(Cliente_id)
    return track
    
@app.get("/Cliente/{Cliente_id}", tags = ["Cliente"])
@version(1, 0)
async def get_Cliente(Cliente_id: str):
    Cliente = sp.Client(Cliente_id)
    return Cliente

   

@app.get("/")
def read_root():
    return {"Hello": "Tarea Concluida APP Cliente DA"}

app = VersionedFastAPI(app)
