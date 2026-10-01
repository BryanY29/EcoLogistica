class DomainError(Exception):
    status_code = 400
    message = "Solicitud no válida"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotFoundError(DomainError):
    status_code = 404


class ValidationError(DomainError):
    status_code = 400


class NoDestinationsError(DomainError):
    status_code = 400
    message = "No es posible generar la ruta porque no existen destinos disponibles"
