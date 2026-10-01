import pytest
from app.services.emissions import calculate_co2


def test_co2_es_distancia_por_factor():
    assert calculate_co2(10.0, 0.254) == pytest.approx(2.54)


def test_co2_con_distancia_cero():
    assert calculate_co2(0.0, 0.254) == 0.0
