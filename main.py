import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import usuarios, turnos
from database import Base, engine
import uvicorn

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