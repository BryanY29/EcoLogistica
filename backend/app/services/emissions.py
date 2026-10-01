def calculate_co2(total_distance_km: float, co2_factor: float) -> float:
    """Estimación de emisiones de CO₂ en kilogramos."""
    return total_distance_km * co2_factor
