from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

class TipoUsuarioEnum(str, Enum):
    cliente = "cliente"
    profesional = "profesional"

class UsuarioBase(BaseModel):
    nombre_completo: str
    telefono: Optional[str]

class ClienteCreate(UsuarioBase):
    dni: str
    edad: int

class ProfesionalCreate(UsuarioBase):
    dni: str
    edad: int
    especialidad: str

class UsuarioOut(UsuarioBase):
    id: int
    tipo_usuario: TipoUsuarioEnum
    dni: Optional[str]
    edad: Optional[int]
    especialidad: Optional[str]

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }

class TurnoBase(BaseModel):
    titulo: str
    hora_inicio: datetime
    hora_fin: datetime
    id_profesional: int
    descripcion: Optional[str] = None
    id_cliente: int

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }

class TurnoCreate(TurnoBase):
    pass

class TurnoOut(TurnoBase):
    id: int

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }
