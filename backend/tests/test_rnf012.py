"""
Prueba de integración RNF-012: la generación de ruta realiza como máximo
1 consulta principal (SELECT) a la base de datos. La generación obtiene los
destinos activos en una sola consulta y el cómputo del óptimo se hace en
memoria, sin más accesos a la base.
"""

from tests.factories import delivery_point_payload


def test_generacion_de_ruta_realiza_una_consulta_principal(client, query_counter):
    ids = []
    for i in range(4):
        response = client.post(
            "/api/v1/delivery-points",
            json=delivery_point_payload(
                nombre=f"Punto {i}",
                distrito="EL TAMBO",
                latitud=-12.0660 + i * 0.01,
                longitud=-75.2200 - i * 0.01,
            ),
        )
        ids.append(response.json()["punto_id"])

    query_counter.statements.clear()

    response = client.post(
        "/api/v1/routes/optimize",
        json={
            "origin": {"lat": -12.0600, "lng": -75.2000},
            "delivery_point_ids": ids,
        },
    )
    assert response.status_code == 200
    assert query_counter.select_count <= 1
