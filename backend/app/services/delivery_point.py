import uuid

from app.core.config import settings
from app.core.constants import ESTADO_ACTIVO
from app.models import DeliveryPoint
from app.repositories import DeliveryPointRepository
from app.schemas import DeliveryPointCreate, DeliveryPointUpdate
from app.services.exceptions import NotFoundError, ValidationError


class DeliveryPointService:
    def __init__(self, repository: DeliveryPointRepository):
        self.repository = repository

    def _validate_scope(self, distrito: str, latitud: float, longitud: float) -> str:
        if not settings.is_district_allowed(distrito):
            raise ValidationError(
                "El distrito está fuera del ámbito geográfico permitido "
                "(El Tambo, Huancayo o Chilca)."
            )
        distrito_normalizado = settings.normalize_district(distrito)
        if not settings.is_in_scope(latitud, longitud):
            raise ValidationError(
                "La ubicación está fuera del ámbito geográfico de El Tambo, Huancayo y Chilca."
            )
        return distrito_normalizado

    def create(self, data: DeliveryPointCreate) -> DeliveryPoint:
        distrito = self._validate_scope(data.distrito, data.latitud, data.longitud)
        payload = data.model_dump()
        payload["distrito"] = distrito
        return self.repository.create(payload)

    def list(self, distrito: str | None = None) -> list[DeliveryPoint]:
        if distrito:
            if not settings.is_district_allowed(distrito):
                raise ValidationError(
                    "El distrito está fuera del ámbito geográfico permitido "
                    "(El Tambo, Huancayo o Chilca)."
                )
            return self.repository.list_active(settings.normalize_district(distrito))
        return self.repository.list_active()

    def get(self, point_id: uuid.UUID) -> DeliveryPoint:
        point = self.repository.get(point_id)
        if point is None or point.estado != ESTADO_ACTIVO:
            raise NotFoundError("El punto de entrega no está disponible.")
        return point

    def update(self, point_id: uuid.UUID, data: DeliveryPointUpdate) -> DeliveryPoint:
        point = self.repository.get(point_id)
        if point is None:
            raise NotFoundError("El punto de entrega no está disponible.")
        payload = data.model_dump(exclude_unset=True)
        if payload:
            distrito = point.distrito
            latitud = float(payload.get("latitud", point.latitud))
            longitud = float(payload.get("longitud", point.longitud))
            if "distrito" in payload:
                distrito = payload["distrito"]
            payload["distrito"] = self._validate_scope(distrito, latitud, longitud)
            return self.repository.update(point, payload)
        return point

    def deactivate(self, point_id: uuid.UUID) -> DeliveryPoint:
        point = self.repository.get(point_id)
        if point is None:
            raise NotFoundError("El punto de entrega no está disponible.")
        return self.repository.deactivate(point)
