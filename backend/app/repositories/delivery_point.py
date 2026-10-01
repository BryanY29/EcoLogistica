import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.constants import ESTADO_ACTIVO, ESTADO_INACTIVO
from app.models import DeliveryPoint


class DeliveryPointRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_active(self, distrito: str | None = None) -> list[DeliveryPoint]:
        stmt = (
            select(DeliveryPoint)
            .where(DeliveryPoint.estado == ESTADO_ACTIVO)
            .order_by(DeliveryPoint.nombre)
        )
        if distrito:
            stmt = stmt.where(DeliveryPoint.distrito == distrito)
        return list(self.session.scalars(stmt))

    def list_by_ids_active(self, point_ids: list[uuid.UUID]) -> list[DeliveryPoint]:
        stmt = (
            select(DeliveryPoint)
            .where(
                DeliveryPoint.punto_id.in_(point_ids),
                DeliveryPoint.estado == ESTADO_ACTIVO,
            )
            .order_by(DeliveryPoint.nombre)
        )
        return list(self.session.scalars(stmt))

    def get(self, point_id: uuid.UUID) -> DeliveryPoint | None:
        return self.session.get(DeliveryPoint, point_id)

    def create(self, payload: dict) -> DeliveryPoint:
        point = DeliveryPoint(**payload)
        self.session.add(point)
        self.session.flush()
        return point

    def update(self, point: DeliveryPoint, payload: dict) -> DeliveryPoint:
        for key, value in payload.items():
            setattr(point, key, value)
        self.session.flush()
        return point

    def deactivate(self, point: DeliveryPoint) -> DeliveryPoint:
        point.estado = ESTADO_INACTIVO
        self.session.flush()
        return point
