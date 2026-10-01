import uuid

from app.core.constants import ESTADO_ACTIVO, ESTADO_INACTIVO
from app.repositories import DeliveryPointRepository

from tests.factories import delivery_point_payload

POINT_A = {
    "nombre": "Mercado El Tambo",
    "direccion": "Av. Los Andes 300",
    "latitud": -12.0667,
    "longitud": -75.2260,
    "distrito": "EL TAMBO",
}


def test_create_and_get(db_session):
    repo = DeliveryPointRepository(db_session)
    point = repo.create(delivery_point_payload())
    db_session.commit()

    fetched = repo.get(point.punto_id)
    assert fetched is not None
    assert fetched.nombre == "Mercado El Tambo"
    assert fetched.estado == ESTADO_ACTIVO


def test_get_missing_returns_none(db_session):
    repo = DeliveryPointRepository(db_session)
    assert repo.get(uuid.uuid4()) is None


def test_update_points(db_session):
    repo = DeliveryPointRepository(db_session)
    point = repo.create(delivery_point_payload())
    updated = repo.update(point, {"nombre": "Plaza Huancayo"})
    db_session.commit()

    assert updated.nombre == "Plaza Huancayo"
    assert repo.get(point.punto_id).nombre == "Plaza Huancayo"


def test_deactivate(db_session):
    repo = DeliveryPointRepository(db_session)
    point = repo.create(delivery_point_payload())
    repo.deactivate(point)
    db_session.commit()

    assert repo.get(point.punto_id).estado == ESTADO_INACTIVO
    assert repo.list_active() == []


def test_list_active_filters_inactive_and_distrito(db_session):
    repo = DeliveryPointRepository(db_session)
    repo.create(POINT_A)
    point_b = repo.create(
        {
            "nombre": "Municipalidad Chilca",
            "direccion": "Jr. Independencia 120",
            "latitud": -12.0714,
            "longitud": -75.1805,
            "distrito": "CHILCA",
        }
    )
    repo.deactivate(point_b)
    db_session.commit()

    assert len(repo.list_active()) == 1
    assert len(repo.list_active("EL TAMBO")) == 1
    assert repo.list_active("CHILCA") == []


def test_list_by_ids_active_excludes_inactive(db_session):
    repo = DeliveryPointRepository(db_session)
    active = repo.create(POINT_A)
    inactive = repo.create(
        {
            "nombre": "Chilca",
            "direccion": "Jr. 1",
            "latitud": -12.0714,
            "longitud": -75.1805,
            "distrito": "CHILCA",
        }
    )
    repo.deactivate(inactive)
    db_session.commit()

    result = repo.list_by_ids_active([active.punto_id, inactive.punto_id])
    assert [p.punto_id for p in result] == [active.punto_id]
