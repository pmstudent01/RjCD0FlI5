"""HTTP client for the Vehicle Service API.

Each method maps 1:1 to a request in the "Vehicle Service Collection":

    Collection request      -> SDK method
    --------------------------------------------------
    Create a vehicle        -> create_vehicle()
    Retrieve a vehicle      -> get_vehicle(vehicle_id)
    Get all vehicles        -> get_all_vehicles()
    Update a collection     -> update_vehicle(vehicle_id, ...)
    Delete a vehicle        -> delete_vehicle(vehicle_id)
"""

import json
from typing import List, Optional, Union
from urllib import request as _request
from urllib.error import HTTPError, URLError

from .models import Vehicle
from .exceptions import VehicleServiceError, VehicleNotFoundError


class VehicleServiceClient:
    """Client for the Vehicle Service API.

    Args:
        base_url: Base URL of the API, e.g. ``http://localhost:4500``.
            Maps to the ``{{baseUrl}}`` collection/environment variable.
        api_key: Optional API key. When provided it is sent as the
            ``x-api-key`` header (maps to the collection's ``vault:apiKey``).
        timeout: Per-request timeout in seconds.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:4500",
        api_key: Optional[str] = None,
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    # ------------------------------------------------------------------ #
    # Internal request helper
    # ------------------------------------------------------------------ #
    def _request(self, method: str, path: str, body: Optional[dict] = None):
        url = f"{self.base_url}{path}"
        data = None
        headers = {"Accept": "application/json"}

        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if self.api_key:
            headers["x-api-key"] = self.api_key

        req = _request.Request(url, data=data, headers=headers, method=method)

        try:
            with _request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
                if not raw:
                    return None
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    return raw
        except HTTPError as e:
            raw = e.read().decode("utf-8") if e.fp else ""
            payload = None
            if raw:
                try:
                    payload = json.loads(raw)
                except json.JSONDecodeError:
                    payload = raw
            if e.code == 404:
                raise VehicleNotFoundError(
                    f"Resource not found: {method} {path}",
                    status_code=404,
                    payload=payload,
                ) from e
            raise VehicleServiceError(
                f"Request failed ({e.code}): {method} {path}",
                status_code=e.code,
                payload=payload,
            ) from e
        except URLError as e:
            raise VehicleServiceError(
                f"Could not reach {url}: {e.reason}"
            ) from e

    # ------------------------------------------------------------------ #
    # Endpoint methods
    # ------------------------------------------------------------------ #
    def get_all_vehicles(self) -> List[Vehicle]:
        """GET /vehicles — list all vehicles."""
        data = self._request("GET", "/vehicles")
        items = data if isinstance(data, list) else data.get("vehicles", []) if isinstance(data, dict) else []
        return [Vehicle.from_dict(v) for v in items]

    def get_vehicle(self, vehicle_id: Union[int, str]) -> Vehicle:
        """GET /vehicles/:id — retrieve a single vehicle by id."""
        data = self._request("GET", f"/vehicles/{vehicle_id}")
        return Vehicle.from_dict(data)

    def create_vehicle(
        self,
        nickName: str,
        vin: str,
        make: str,
        model: str,
        year: str,
        miles: int,
    ) -> Vehicle:
        """POST /vehicles — create a new vehicle. Expects HTTP 201."""
        payload = {
            "nickName": nickName,
            "vin": vin,
            "make": make,
            "model": model,
            "year": year,
            "miles": miles,
        }
        data = self._request("POST", "/vehicles", body=payload)
        return Vehicle.from_dict(data) if isinstance(data, dict) else data

    def update_vehicle(self, vehicle_id: Union[int, str], **fields) -> Vehicle:
        """PATCH /vehicles/:id — partially update a vehicle.

        Pass any of: nickName, vin, make, model, year, miles.
        """
        data = self._request("PATCH", f"/vehicles/{vehicle_id}", body=fields)
        return Vehicle.from_dict(data) if isinstance(data, dict) else data

    def delete_vehicle(self, vehicle_id: Union[int, str]) -> None:
        """DELETE /vehicles/:id — delete a vehicle by id."""
        self._request("DELETE", f"/vehicles/{vehicle_id}")
