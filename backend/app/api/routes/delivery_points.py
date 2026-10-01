import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories import DeliveryPointRepository
from app.schemas import DeliveryPointCreate, DeliveryPointOut, DeliveryPointUpdate
from app.services import DeliveryPointService

router = APIRouter(prefix="/delivery-points", tags=["delivery-points"])


def get_service(db: Annotated[Session, Depends(get_db)]) -> DeliveryPointService:
    repository = DeliveryPointRepository(db)
    return DeliveryPointService(repository)


@router.get("", response_model=list[DeliveryPointOut])
def list_delivery_points(
    distrito: str | None = None,
    service: Annotated[DeliveryPointService, Depends(get_service)] = None,
) -> list:
    return service.list(distrito)


@router.post("", response_model=DeliveryPointOut, status_code=201)
def create_delivery_point(
    payload: DeliveryPointCreate,
    service: Annotated[DeliveryPointService, Depends(get_service)] = None,
):
    return service.create(payload)


@router.get("/{punto_id}", response_model=DeliveryPointOut)
def get_delivery_point(
    punto_id: uuid.UUID,
    service: Annotated[DeliveryPointService, Depends(get_service)] = None,
):
    return service.get(punto_id)


@router.put("/{punto_id}", response_model=DeliveryPointOut)
def update_delivery_point(
    punto_id: uuid.UUID,
    payload: DeliveryPointUpdate,
    service: Annotated[DeliveryPointService, Depends(get_service)] = None,
):
    return service.update(punto_id, payload)


@router.delete("/{punto_id}", response_model=DeliveryPointOut)
def deactivate_delivery_point(
    punto_id: uuid.UUID,
    service: Annotated[DeliveryPointService, Depends(get_service)] = None,
):
    return service.deactivate(punto_id)
