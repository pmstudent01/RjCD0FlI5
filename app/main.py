"""Vehicle Service demo app.

A small CLI application that exercises the full Vehicle Service API using the
generated vehicle_sdk. It runs through every endpoint from the
"Vehicle Service Collection":

    1. Create a vehicle      (POST   /vehicles)
    2. Get all vehicles      (GET    /vehicles)
    3. Retrieve a vehicle    (GET    /vehicles/:id)
    4. Update a vehicle      (PATCH  /vehicles/:id)
    5. Delete a vehicle      (DELETE /vehicles/:id)

Configuration via environment variables:
    BASE_URL   base URL of the API (default: http://localhost:4500)
    API_KEY    optional API key sent as x-api-key
"""

import os
import sys

# Make the sibling sdk/ package importable when run directly.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sdk"))

from vehicle_sdk import VehicleServiceClient, VehicleServiceError  # noqa: E402


def main() -> int:
    base_url = os.environ.get("BASE_URL", "http://localhost:4500")
    api_key = os.environ.get("API_KEY")

    client = VehicleServiceClient(base_url=base_url, api_key=api_key)
    print(f"Connecting to Vehicle Service at {base_url}\n")

    try:
        # 1. Create
        print("Creating a vehicle...")
        created = client.create_vehicle(
            nickName="The Lisa Marie",
            vin="4M2DV11W4RDJ53329",
            make="Mercury",
            model="Villager",
            year="1994",
            miles=159864,
        )
        print(f"  Created: {created}\n")

        vehicle_id = getattr(created, "id", None) or 1

        # 2. List all
        print("Fetching all vehicles...")
        vehicles = client.get_all_vehicles()
        print(f"  Found {len(vehicles)} vehicle(s).\n")

        # 3. Retrieve one
        print(f"Retrieving vehicle {vehicle_id}...")
        vehicle = client.get_vehicle(vehicle_id)
        print(f"  Retrieved: {vehicle}\n")

        # 4. Update
        print(f"Updating vehicle {vehicle_id} mileage...")
        updated = client.update_vehicle(vehicle_id, miles=159999)
        print(f"  Updated: {updated}\n")

        # 5. Delete
        print(f"Deleting vehicle {vehicle_id}...")
        client.delete_vehicle(vehicle_id)
        print("  Deleted.\n")

        print("All operations completed successfully.")
        return 0

    except VehicleServiceError as exc:
        print(f"\nAPI error: {exc}")
        if exc.status_code:
            print(f"  status_code={exc.status_code}")
        if exc.payload:
            print(f"  payload={exc.payload}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
