# Vehicle Service Python SDK & App

A Python SDK and demo application generated from the **Vehicle Service Collection**
(Postman). The SDK uses only the Python standard library — no external
dependencies required.

## Layout

```
sdk/
  vehicle_sdk/
    __init__.py      # package exports
    client.py        # VehicleServiceClient (one method per endpoint)
    models.py        # Vehicle dataclass
    exceptions.py    # VehicleServiceError, VehicleNotFoundError
app/
  main.py            # demo CLI app that exercises every endpoint
```

## SDK usage

```python
from vehicle_sdk import VehicleServiceClient

client = VehicleServiceClient(base_url="http://localhost:4500")

# Create a vehicle (POST /vehicles)
v = client.create_vehicle(
    nickName="The Lisa Marie", vin="4M2DV11W4RDJ53329",
    make="Mercury", model="Villager", year="1994", miles=159864,
)

# List all vehicles (GET /vehicles)
all_vehicles = client.get_all_vehicles()

# Retrieve one (GET /vehicles/:id)
one = client.get_vehicle(1)

# Update (PATCH /vehicles/:id)
client.update_vehicle(1, miles=159999)

# Delete (DELETE /vehicles/:id)
client.delete_vehicle(1)
```

## Endpoint mapping

| Collection request  | SDK method                   | HTTP                  |
|---------------------|------------------------------|-----------------------|
| Create a vehicle    | `create_vehicle(...)`        | `POST /vehicles`      |
| Retrieve a vehicle  | `get_vehicle(id)`            | `GET /vehicles/:id`   |
| Get all vehicles    | `get_all_vehicles()`         | `GET /vehicles`       |
| Update a collection | `update_vehicle(id, **f)`    | `PATCH /vehicles/:id` |
| Delete a vehicle    | `delete_vehicle(id)`         | `DELETE /vehicles/:id`|

## Running the demo app

```bash
# Optional config
export BASE_URL=http://localhost:4500
export API_KEY=your-key        # sent as x-api-key, optional

python app/main.py
```

`BASE_URL` corresponds to the collection's `{{baseUrl}}` variable; `API_KEY`
corresponds to the `vault:apiKey` value.
