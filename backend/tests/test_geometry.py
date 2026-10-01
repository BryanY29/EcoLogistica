import pytest
from app.services.geometry import haversine


def test_ecuador_un_grado_de_longitud():
    distance = haversine(0.0, 0.0, 0.0, 1.0)
    assert distance == pytest.approx(111.19, abs=0.5)


def test_distancia_entre_dos_puntos_de_huancayo():
    distance = haversine(-12.0651, -75.2049, -12.0714, -75.1805)
    assert 0.5 < distance < 10.0


def test_distancia_cero_para_el_mismo_punto():
    assert haversine(-12.06, -75.20, -12.06, -75.20) == 0.0
