"""Data models for the Vehicle Service SDK."""

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Vehicle:
    """Represents a vehicle resource.

    Mirrors the JSON schema used by the Vehicle Service Collection requests.
    """

    nickName: str
    vin: str
    make: str
    model: str
    year: str
    miles: int
    id: Optional[int] = None

    def to_payload(self) -> dict:
        """Return a dict suitable for a create/update request body.

        The server-assigned ``id`` is omitted from the payload.
        """
        data = asdict(self)
        data.pop("id", None)
        return {k: v for k, v in data.items() if v is not None}

    @classmethod
    def from_dict(cls, data: dict) -> "Vehicle":
        """Build a Vehicle from an API response dict, ignoring unknown keys."""
        known = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in data.items() if k in known})
