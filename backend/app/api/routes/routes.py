from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories import DeliveryPointRepository
from app.schemas import RouteOptimizeRequest, RouteResult
from app.services import RouteService

router = APIRouter(prefix="/routes", tags=["routes"])


def get_route_service(db: Annotated[Session, Depends(get_db)]) -> RouteService:
    repository = DeliveryPointRepository(db)
    return RouteService(repository)


@router.post("/optimize", response_model=RouteResult)
def optimize_route(
    payload: RouteOptimizeRequest,
    service: Annotated[RouteService, Depends(get_route_service)] = None,
):
    route = service.optimize(payload.origin, payload.delivery_point_ids)
    return service.to_schema(route)
