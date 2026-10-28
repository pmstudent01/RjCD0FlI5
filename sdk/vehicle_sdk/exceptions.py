"""Exceptions raised by the Vehicle Service SDK."""


class VehicleServiceError(Exception):
    """Base error for all Vehicle Service SDK failures.

    Attributes:
        status_code: HTTP status code returned by the API (if any).
        payload: Parsed response body (if any).
    """

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


class VehicleNotFoundError(VehicleServiceError):
    """Raised when a vehicle with the requested id does not exist (HTTP 404)."""
