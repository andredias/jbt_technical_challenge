from datetime import datetime

from httpx import AsyncClient

from jbt_drone import drone as drone_lib
from jbt_drone.authentication import create_access_token
from jbt_drone.routers import drone as drone_route
from jbt_drone.schemas import Destination


async def test_next_coordinates(client: AsyncClient) -> None:
    url = '/drone/next_destination'
    drone_lib._current_location = drone_lib._store_coords = (0.0, 0.0)

    # unauthenticated access
    resp = await client.get(url)
    assert resp.status_code == 401

    # authenticated access
    token = create_access_token({'sub': 1})
    headers = {'authorization': f'Bearer {token}'}

    # empty list of destinations
    drone_route._destinations = []
    resp = await client.get(url, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert tuple(data) == drone_lib._store_coords

    now = datetime.now()
    drone_route._destinations = [
        Destination(time=now, coords=(0.04, 0.02)),
        Destination(time=now, coords=(0.01, 0.02)),
        Destination(time=now, coords=(0.02, 0.02)),
    ]
    resp = await client.get(url, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert tuple(data) == (0.01, 0.02)
    assert len(drone_route._destinations) == 2

    resp = await client.get(url, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert tuple(data) == (0.02, 0.02)
    assert len(drone_route._destinations) == 1
