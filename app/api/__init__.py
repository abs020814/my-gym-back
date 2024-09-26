from fastapi import APIRouter

from app.api.routes import login
from .routes import  entrenadores, clientes, rutinas, usuarios, nutricion

api_router = APIRouter()
api_router.include_router(entrenadores.router, prefix="/entrenadores", tags=["entrenadores"])
api_router.include_router(clientes.router, prefix="/clientes", tags=["clientes"])
api_router.include_router(rutinas.router, prefix="/rutinas", tags=["rutinas"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
api_router.include_router(nutricion.router, prefix="/nutricion", tags=["nutricion"])

