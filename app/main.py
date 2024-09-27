import logging
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables de entorno desde .env

from fastapi import FastAPI
from .api import api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(SessionMiddleware, secret_key="!secret")

# Configurar el cliente OAuth (por ejemplo, para Google)
oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.environ.get('GOOGLE_ID'),
    client_secret=os.environ.get('GOOGLE_SECRET'),
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:3000/auth',
    client_kwargs={'scope': 'openid profile email'}
)
# Ruta para iniciar la autenticación con Google
# @app.get("/login")
# async def login_via_google():
#     redirect_uri = 'http://localhost:3000/auth'
#     return await oauth.google.authorize_redirect(redirect_uri)

# Ruta de redirección/callback para Google
@app.get("/auth")
async def auth_via_google(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    # Aquí puedes crear un token JWT para tu aplicación, en este ejemplo, solo devolvemos el perfil del usuario
    return {"email": user.email, "name": user.name}

# Ruta para manejar POST en /auth (si necesitas manejar datos enviados vía POST)
class Token(BaseModel):
    token: str

@app.post("/auth")
async def auth_via_google(token: Token):
    # Verificar el token con Google
    url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token.token}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Token inválido")

    user_info = response.json()

    # Extraer información del usuario
    email = user_info.get("email")
    name = user_info.get("name")

    return {"email": email, "name": name}

# Ruta que maneja el callback después de la autenticación
@app.get("/auth/callback")
async def auth_callback(request: Request):
    # Maneja el código de autenticación que Google devuelve
    code = request.query_params.get("code")
    
    if not code:
        raise HTTPException(status_code=400, detail="No se recibió el código de autenticación")

    # Aquí procesarías el código para intercambiarlo por un token de acceso
    # y manejar la autenticación del usuario en tu aplicación.

    return {"message": "Autenticación completada", "code": code}

# Punto de entrada para ejecutar la aplicación con Uvicorn

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=3000)

    
app.include_router(api_router)