from dataclasses import dataclass

from app.core.config import settings
from app.models import DeliveryPoint
from app.repositories import DeliveryPointRepository
from app.schemas import Coordinate, DeliveryPointOut, RouteResult
from app.services import emissions
from app.services.exceptions import NoDestinationsError, ValidationError
from app.services.geometry import haversine
from app.services.route_optimizer import solve_tsp


@dataclass
class OptimizedRoute:
    order: list[DeliveryPoint]
    total_distance_km: float
    co2_emissions_kg: float


class RouteService:
    def __init__(self, repository: DeliveryPointRepository, co2_factor: float | None = None):
        self.repository = repository
        self.co2_factor = co2_factor if co2_factor is not None else settings.co2_factor

    def _validate_origin(self, origin: Coordinate) -> None:
        if not settings.is_in_scope(origin.lat, origin.lng):
            raise ValidationError(
                "El punto de origen está fuera del ámbito geográfico "
                "de El Tambo, Huancayo y Chilca."
            )

    def _distance_matrix(self, origin: Coordinate, points: list[DeliveryPoint]):
        coords = [(origin.lat, origin.lng)]
        coords.extend((float(p.latitud), float(p.longitud)) for p in points)
        size = len(coords)
        matrix = [[0.0] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                if i != j:
                    matrix[i][j] = haversine(coords[i][0], coords[i][1], coords[j][0], coords[j][1])
        return matrix

    def optimize(self, origin: Coordinate, delivery_point_ids: list) -> OptimizedRoute:
        self._validate_origin(origin)
        points = self.repository.list_by_ids_active(delivery_point_ids)
        if not points:
            raise NoDestinationsError(
                "No es posible generar la ruta porque no existen destinos habilitados."
            )
        dist_matrix = self._distance_matrix(origin, points)
        order_indices = solve_tsp(dist_matrix)
        ordered_points = [points[i - 1] for i in order_indices[1:]]
        total_distance = sum(
            dist_matrix[order_indices[i]][order_indices[i + 1]]
            for i in range(len(order_indices) - 1)
        )
        co2 = emissions.calculate_co2(total_distance, self.co2_factor)
        return OptimizedRoute(
            order=ordered_points,
            total_distance_km=round(total_distance, 3),
            co2_emissions_kg=round(co2, 3),
        )

    def to_schema(self, route: OptimizedRoute) -> RouteResult:
        return RouteResult(
            order=[DeliveryPointOut.model_validate(point) for point in route.order],
            total_distance_km=route.total_distance_km,
            co2_emissions_kg=route.co2_emissions_kg,
        )
