import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import usuarios, turnos
from database import Base, engine
import uvicorn
# Importar componentes de Starlette para el middleware de redirección
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from starlette.requests import Request

# Definición del middleware de redirección para evitar el problema de CORS en
# las redirecciones automáticas por barra diagonal.
class StrippingTrailingSlashMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # La condición verifica si el path termina en / (no es la raíz)
        if request.url.path.endswith("/") and request.url.path != "/":
            url_sin_slash = request.url.path[:-1]
            
            # Construye la URL completa para la redirección (307: Temporal Redirect)
            redirect_url = request.url.scheme + "://" + request.url.netloc + url_sin_slash
            if request.url.query:
                redirect_url += "?" + request.url.query
            
            # Retorna la redirección. Al ser un response explícito antes del router,
            # los middleware posteriores (como CORS) tienen la oportunidad de añadir 
            # sus cabeceras antes de que la respuesta sea enviada.
            return RedirectResponse(redirect_url, status_code=307)
            
        return await call_next(request)


# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 1. Añadir el middleware de eliminación de barra diagonal ANTES del middleware CORS
# Esto fuerza la redirección antes del router, lo que permite que el CORSMiddleware 
# intercepte la respuesta de redirección y añada las cabeceras.
app.add_middleware(StrippingTrailingSlashMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(usuarios.router)
app.include_router(turnos.router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Railway asigna PORT
    uvicorn.run(app, host="0.0.0.0", port=port)