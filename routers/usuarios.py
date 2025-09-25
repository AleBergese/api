from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List # Importa List para los tipos de respuesta
import models
import schemas
from database import SessionLocal

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/clientes", response_model=schemas.UsuarioOut)
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    nuevo = models.Usuario(
        nombre_completo=cliente.nombre_completo,
        dni=cliente.dni,
        edad=cliente.edad,
        telefono=cliente.telefono,
        tipo_usuario=models.TipoUsuarioEnum.cliente
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.post("/profesionales", response_model=schemas.UsuarioOut)
def crear_profesional(pro: schemas.ProfesionalCreate, db: Session = Depends(get_db)):
    nuevo = models.Usuario(
        nombre_completo=pro.nombre_completo,
        dni=pro.dni,
        edad=pro.edad,
        telefono=pro.telefono,
        tipo_usuario=models.TipoUsuarioEnum.profesional,
        especialidad=pro.especialidad
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# --- Nuevos métodos GET ---

@router.get("/clientes", response_model=List[schemas.UsuarioOut])
def obtener_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene una lista de todos los usuarios que son clientes.
    """
    clientes = db.query(models.Usuario).filter(models.Usuario.tipo_usuario == models.TipoUsuarioEnum.cliente).offset(skip).limit(limit).all()
    return clientes

@router.get("/profesionales", response_model=List[schemas.UsuarioOut])
def obtener_profesionales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene una lista de todos los usuarios que son profesionales.
    """
    profesionales = db.query(models.Usuario).filter(models.Usuario.tipo_usuario == models.TipoUsuarioEnum.profesional).offset(skip).limit(limit).all()
    return profesionales

@router.get("/clientes/{cliente_id}", response_model=schemas.UsuarioOut)
def obtener_cliente_por_id(cliente_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un cliente específico por su ID.
    """
    cliente = db.query(models.Usuario).filter(models.Usuario.id == cliente_id, models.Usuario.tipo_usuario == models.TipoUsuarioEnum.cliente).first()
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.get("/profesionales/{profesional_id}", response_model=schemas.UsuarioOut)
def obtener_profesional_por_id(profesional_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un profesional específico por su ID.
    """
    profesional = db.query(models.Usuario).filter(models.Usuario.id == profesional_id, models.Usuario.tipo_usuario == models.TipoUsuarioEnum.profesional).first()
    if profesional is None:
        raise HTTPException(status_code=404, detail="Profesional no encontrado")
    return profesional