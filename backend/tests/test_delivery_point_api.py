from tests.factories import delivery_point_payload

ENDPOINT = "/api/v1/delivery-points"


def test_create_delivery_point(client):
    response = client.post(ENDPOINT, json=delivery_point_payload(distrito="el tambo"))
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Mercado El Tambo"
    assert data["distrito"] == "EL TAMBO"
    assert data["estado"] == "ACTIVO"


def test_list_returns_only_enabled_units(client):
    client.post(ENDPOINT, json=delivery_point_payload(nombre="Punto 1", distrito="HUANCAYO"))
    second = client.post(
        ENDPOINT, json=delivery_point_payload(nombre="Punto 2", distrito="CHILCA")
    ).json()
    client.delete(f"{ENDPOINT}/{second['punto_id']}")

    list_response = client.get(ENDPOINT)
    assert list_response.status_code == 200
    names = [item["nombre"] for item in list_response.json()]
    assert names == ["Punto 1"]


def test_list_filter_by_distrito(client):
    client.post(ENDPOINT, json=delivery_point_payload(nombre="Tambo", distrito="EL TAMBO"))
    client.post(ENDPOINT, json=delivery_point_payload(nombre="Chilca", distrito="CHILCA"))

    data = client.get(ENDPOINT, params={"distrito": "EL TAMBO"}).json()
    assert [item["nombre"] for item in data] == ["Tambo"]


def test_get_by_id(client):
    created = client.post(ENDPOINT, json=delivery_point_payload()).json()
    response = client.get(f"{ENDPOINT}/{created['punto_id']}")
    assert response.status_code == 200
    assert response.json()["punto_id"] == created["punto_id"]


def test_get_missing_id_returns_404(client):
    response = client.get(f"{ENDPOINT}/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_get_invalid_id_returns_400(client):
    response = client.get(f"{ENDPOINT}/no-es-un-uuid")
    assert response.status_code == 400


def test_distrito_fuera_de_ambito_returns_400(client):
    response = client.post(ENDPOINT, json=delivery_point_payload(distrito="LIMA"))
    assert response.status_code == 400
    assert "ámbito geográfico" in response.json()["detail"]


def test_ubicacion_invalida_returns_400(client):
    response = client.post(ENDPOINT, json=delivery_point_payload(latitud=0.0, longitud=0.0))
    assert response.status_code == 400


def test_latitud_fuera_de_rango_returns_400(client):
    response = client.post(ENDPOINT, json=delivery_point_payload(latitud=95.0))
    assert response.status_code == 400


def test_datos_incompletos_returns_400(client):
    response = client.post(ENDPOINT, json={"nombre": "Solo nombre"})
    assert response.status_code == 400


def test_update_delivery_point(client):
    created = client.post(ENDPOINT, json=delivery_point_payload()).json()
    response = client.put(f"{ENDPOINT}/{created['punto_id']}", json={"nombre": "Renombrado"})
    assert response.status_code == 200
    assert response.json()["nombre"] == "Renombrado"


def test_update_distrito_invalido_returns_400(client):
    created = client.post(ENDPOINT, json=delivery_point_payload()).json()
    response = client.put(f"{ENDPOINT}/{created['punto_id']}", json={"distrito": "LIMA"})
    assert response.status_code == 400


def test_delete_deactivates_logicamente(client):
    created = client.post(ENDPOINT, json=delivery_point_payload()).json()
    response = client.delete(f"{ENDPOINT}/{created['punto_id']}")
    assert response.status_code == 200
    assert response.json()["estado"] == "INACTIVO"

    assert client.get(ENDPOINT).json() == []
    assert client.get(f"{ENDPOINT}/{created['punto_id']}").status_code == 404


def test_delete_missing_id_returns_404(client):
    response = client.delete(f"{ENDPOINT}/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
