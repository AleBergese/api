from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import SessionLocal

router = APIRouter(prefix="/turnos", tags=["Turnos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.get("/", response_model=list[schemas.TurnoOut])
def listar_turnos(id_profesional: int | None = None, id_cliente: int | None = None, db: Session = Depends(get_db)):
    if id_profesional:
        return db.query(models.Turno).filter(models.Turno.id_profesional == id_profesional).all()
    if id_cliente:
        return db.query(models.Turno).filter(models.Turno.id_cliente == id_cliente).all()
    return db.query(models.Turno).all()  # opcional: devolver todos si no se pasa ningún filtro

@router.post("/", response_model=schemas.TurnoOut)
def crear_turno(turno: schemas.TurnoCreate, db: Session = Depends(get_db)):
    # Validar que el cliente y el profesional existan
    cliente = db.query(models.Usuario).filter(models.Usuario.id == turno.id_cliente, models.Usuario.tipo_usuario == models.TipoUsuarioEnum.cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    profesional = db.query(models.Usuario).filter(models.Usuario.id == turno.id_profesional, models.Usuario.tipo_usuario == models.TipoUsuarioEnum.profesional).first()
    if not profesional:
        raise HTTPException(status_code=404, detail="Profesional no encontrado")

    nuevo_turno = models.Turno(**turno.dict())
    db.add(nuevo_turno)
    db.commit()
    db.refresh(nuevo_turno)
    return nuevo_turno