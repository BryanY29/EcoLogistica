import uuid

import pytest
from app.repositories import DeliveryPointRepository
from app.schemas import DeliveryPointCreate, DeliveryPointUpdate
from app.services import DeliveryPointService
from app.services.exceptions import NotFoundError, ValidationError
from pydantic import ValidationError as PydanticValidationError

from tests.factories import delivery_point_payload


def make_service(db_session):
    return DeliveryPointService(DeliveryPointRepository(db_session))


def test_create_valid_normalizes_distrito(db_session):
    point = make_service(db_session).create(
        DeliveryPointCreate(**delivery_point_payload(distrito="el tambo"))
    )
    assert point.distrito == "EL TAMBO"


def test_create_distrito_fuera_de_ambito(db_session):
    service = make_service(db_session)
    with pytest.raises(ValidationError):
        service.create(DeliveryPointCreate(**delivery_point_payload(distrito="LIMA")))


def test_create_ubicacion_fuera_de_ambito(db_session):
    service = make_service(db_session)
    with pytest.raises(ValidationError):
        service.create(DeliveryPointCreate(**delivery_point_payload(latitud=0.0, longitud=0.0)))


def test_create_campos_obligatorios_faltantes():
    with pytest.raises(PydanticValidationError):
        DeliveryPointCreate(
            nombre="",
            direccion="",
            latitud=-120.0,
            longitud=100.0,
            distrito="EL TAMBO",
        )


def test_list_with_invalid_distrito(db_session):
    service = make_service(db_session)
    with pytest.raises(ValidationError):
        service.list("LIMA")


def test_get_missing_raises_not_found(db_session):
    with pytest.raises(NotFoundError):
        make_service(db_session).get(uuid.uuid4())


def test_update_ok(db_session):
    point = make_service(db_session).create(DeliveryPointCreate(**delivery_point_payload()))
    updated = make_service(db_session).update(
        point.punto_id, DeliveryPointUpdate(nombre="Nuevo nombre")
    )
    assert updated.nombre == "Nuevo nombre"
    assert updated.distrito == "EL TAMBO"


def test_update_missing_raises_not_found(db_session):
    with pytest.raises(NotFoundError):
        make_service(db_session).update(uuid.uuid4(), DeliveryPointUpdate(nombre="X"))


def test_update_distrito_no_permitido(db_session):
    point = make_service(db_session).create(DeliveryPointCreate(**delivery_point_payload()))
    with pytest.raises(ValidationError):
        make_service(db_session).update(point.punto_id, DeliveryPointUpdate(distrito="LIMA"))


def test_deactivate_and_get_after(db_session):
    service = make_service(db_session)
    point = service.create(DeliveryPointCreate(**delivery_point_payload()))
    service.deactivate(point.punto_id)
    with pytest.raises(NotFoundError):
        service.get(point.punto_id)


def test_deactivate_missing_raises_not_found(db_session):
    with pytest.raises(NotFoundError):
        make_service(db_session).deactivate(uuid.uuid4())
