"""Vehicle Service SDK.

A lightweight Python client for the Vehicle Service API, generated from the
"Vehicle Service Collection" Postman collection.

Usage:
    from vehicle_sdk import VehicleServiceClient

    client = VehicleServiceClient(base_url="http://localhost:4500")
    vehicles = client.get_all_vehicles()
"""

from .client import VehicleServiceClient
from .models import Vehicle
from .exceptions import VehicleServiceError, VehicleNotFoundError

__all__ = [
    "VehicleServiceClient",
    "Vehicle",
    "VehicleServiceError",
    "VehicleNotFoundError",
]

__version__ = "1.0.0"
