def delivery_point_payload(
    nombre: str = "Mercado El Tambo",
    direccion: str = "Av. Los Andes 300",
    latitud: float = -12.0667,
    longitud: float = -75.2260,
    distrito: str = "EL TAMBO",
) -> dict:
    return {
        "nombre": nombre,
        "direccion": direccion,
        "latitud": latitud,
        "longitud": longitud,
        "distrito": distrito,
    }
