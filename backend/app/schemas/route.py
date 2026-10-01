import uuid

from pydantic import BaseModel, Field

from app.schemas.delivery_point import DeliveryPointOut


class Coordinate(BaseModel):
    lat: float = Field(ge=-90.0, le=90.0)
    lng: float = Field(ge=-180.0, le=180.0)


class RouteOptimizeRequest(BaseModel):
    origin: Coordinate
    delivery_point_ids: list[uuid.UUID] = Field(min_length=1)


class RouteResult(BaseModel):
    order: list[DeliveryPointOut]
    total_distance_km: float
    co2_emissions_kg: float
