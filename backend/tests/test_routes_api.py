import pytest
from app.services.geometry import haversine

from tests.factories import delivery_point_payload

ENDPOINT = "/api/v1/routes/optimize"
ORIGIN = {"lat": -12.0600, "lng": -75.2000}
TOLERANCE = 0.002


def _origin_payload(point_ids):
    return {"origin": ORIGIN, "delivery_point_ids": point_ids}


def _register(client, nombre, distrito="EL TAMBO", latitud=None, longitud=None):
    payload = delivery_point_payload(nombre=nombre, distrito=distrito)
    if latitud is not None:
        payload["latitud"] = latitud
    if longitud is not None:
        payload["longitud"] = longitud
    return client.post("/api/v1/delivery-points", json=payload).json()


def test_generate_route_returns_ordered_points(client):
    p1 = _register(client, "A", "EL TAMBO", -12.0667, -75.2260)
    p2 = _register(client, "B", "HUANCAYO", -12.0651, -75.2049)
    p3 = _register(client, "C", "CHILCA", -12.0714, -75.1805)

    response = client.post(
        ENDPOINT,
        json=_origin_payload([p1["punto_id"], p2["punto_id"], p3["punto_id"]]),
    )
    assert response.status_code == 200
    data = response.json()

    ids = [item["punto_id"] for item in data["order"]]
    assert len(ids) == 3
    assert len(set(ids)) == 3
    assert set(ids) == {p1["punto_id"], p2["punto_id"], p3["punto_id"]}
    assert data["total_distance_km"] > 0
    assert data["co2_emissions_kg"] > 0


def test_total_distance_consistente(client):
    p1 = _register(client, "A", "EL TAMBO", -12.0667, -75.2260)
    p2 = _register(client, "B", "HUANCAYO", -12.0651, -75.2049)

    data = client.post(ENDPOINT, json=_origin_payload([p1["punto_id"], p2["punto_id"]])).json()
    order = data["order"]

    first = order[0]
    second = order[1]
    expected = haversine(
        ORIGIN["lat"], ORIGIN["lng"], first["latitud"], first["longitud"]
    ) + haversine(
        first["latitud"],
        first["longitud"],
        second["latitud"],
        second["longitud"],
    )
    assert data["total_distance_km"] == pytest.approx(expected, abs=TOLERANCE)


def test_co2_es_distancia_por_factor(client):
    p1 = _register(client, "A", "EL TAMBO", -12.0667, -75.2260)
    p2 = _register(client, "B", "HUANCAYO", -12.0651, -75.2049)

    data = client.post(ENDPOINT, json=_origin_payload([p1["punto_id"], p2["punto_id"]])).json()
    expected_co2 = data["total_distance_km"] * 0.254
    assert data["co2_emissions_kg"] == pytest.approx(expected_co2, abs=TOLERANCE)


def test_origen_invalido_returns_400(client):
    p1 = _register(client, "A", "EL TAMBO", -12.0667, -75.2260)
    payload = {"origin": {"lat": 0.0, "lng": 0.0}, "delivery_point_ids": [p1["punto_id"]]}
    response = client.post(ENDPOINT, json=payload)
    assert response.status_code == 400
    assert "origen" in response.json()["detail"].lower()


def test_sin_destinos_disponibles_returns_400(client):
    missing = client.post(ENDPOINT, json=_origin_payload(["00000000-0000-0000-0000-000000000000"]))
    assert missing.status_code == 400
    assert "destinos" in missing.json()["detail"].lower()


def test_excluye_puntos_desactivados(client):
    active = _register(client, "A", "EL TAMBO", -12.0667, -75.2260)
    inactive = _register(client, "B", "HUANCAYO", -12.0651, -75.2049)
    client.delete(f"/api/v1/delivery-points/{inactive['punto_id']}")

    payload = _origin_payload([active["punto_id"], inactive["punto_id"]])
    data = client.post(ENDPOINT, json=payload).json()
    assert [item["punto_id"] for item in data["order"]] == [active["punto_id"]]


def test_requiere_al_menos_un_destino(client):
    response = client.post(ENDPOINT, json={"origin": ORIGIN, "delivery_point_ids": []})
    assert response.status_code == 400
