import pytest
from app.services.geometry import haversine

from tests.factories import delivery_point_payload

ORIGIN = {"lat": -12.0600, "lng": -75.2000}
TOLERANCE = 0.002


def _register(client, nombre, distrito, latitud, longitud):
    payload = delivery_point_payload(
        nombre=nombre, distrito=distrito, latitud=latitud, longitud=longitud
    )
    return client.post("/api/v1/delivery-points", json=payload).json()


def test_flujo_completo_registrar_optimizar_verificar(client):
    p1 = _register(client, "Mercado El Tambo", "EL TAMBO", -12.0667, -75.2260)
    p2 = _register(client, "Plaza Huancayo", "HUANCAYO", -12.0651, -75.2049)
    p3 = _register(client, "Chilca", "CHILCA", -12.0714, -75.1805)
    p4 = _register(client, "Sicaya", "HUANCAYO", -12.0947, -75.1773)

    listado = client.get("/api/v1/delivery-points")
    assert listado.status_code == 200
    assert len(listado.json()) == 4

    response = client.post(
        "/api/v1/routes/optimize",
        json={
            "origin": ORIGIN,
            "delivery_point_ids": [
                p1["punto_id"],
                p2["punto_id"],
                p3["punto_id"],
                p4["punto_id"],
            ],
        },
    )
    assert response.status_code == 200
    data = response.json()

    assert len(data["order"]) == 4

    coords = [(ORIGIN["lat"], ORIGIN["lng"])]
    coords.extend((item["latitud"], item["longitud"]) for item in data["order"])
    expected_total = sum(
        haversine(coords[i][0], coords[i][1], coords[i + 1][0], coords[i + 1][1])
        for i in range(len(coords) - 1)
    )
    assert data["total_distance_km"] == pytest.approx(expected_total, abs=TOLERANCE)
    assert data["co2_emissions_kg"] == pytest.approx(expected_total * 0.254, abs=TOLERANCE)

    ids = [item["punto_id"] for item in data["order"]]
    assert len(set(ids)) == 4

    deactivated = client.delete(f"/api/v1/delivery-points/{p4['punto_id']}")
    assert deactivated.status_code == 200

    listado_2 = client.get("/api/v1/delivery-points")
    assert len(listado_2.json()) == 3
