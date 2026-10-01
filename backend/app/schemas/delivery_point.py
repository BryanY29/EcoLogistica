import uuid

from pydantic import BaseModel, ConfigDict, Field


class DeliveryPointBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    direccion: str = Field(min_length=1)
    latitud: float = Field(ge=-90.0, le=90.0)
    longitud: float = Field(ge=-180.0, le=180.0)
    distrito: str = Field(min_length=1, max_length=100)


class DeliveryPointCreate(DeliveryPointBase):
    pass


class DeliveryPointUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=150)
    direccion: str | None = Field(default=None, min_length=1)
    latitud: float | None = Field(default=None, ge=-90.0, le=90.0)
    longitud: float | None = Field(default=None, ge=-180.0, le=180.0)
    distrito: str | None = Field(default=None, min_length=1, max_length=100)


class DeliveryPointOut(DeliveryPointBase):
    model_config = ConfigDict(from_attributes=True)

    punto_id: uuid.UUID
    estado: str = "ACTIVO"
    latitud: float
    longitud: float
