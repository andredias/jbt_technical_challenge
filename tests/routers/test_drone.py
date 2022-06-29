from datetime import datetime, timedelta
from pathlib import Path

from httpx import AsyncClient

from jbt_drone import drone as drone_lib
from jbt_drone.authentication import create_access_token
from jbt_drone.routers import drone as drone_route
from jbt_drone.schemas import Destination


def new_destinations() -> list[Destination]:
    now = datetime.now()
    return [
        Destination(time=now - timedelta(minutes=2), lat=0.04, long=0.02),
        Destination(time=now - timedelta(minutes=1), lat=0.01, long=0.02),
        Destination(time=now - timedelta(minutes=0), lat=0.02, long=0.02),
    ]


async def test_next_destination(client: AsyncClient) -> None:
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

    drone_route._destinations = new_destinations()
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


async def test_upload_destinations(client: AsyncClient) -> None:
    drone_route._destinations = []
    csvfilename = Path(__file__).parent / 'destinations.csv'
    files = {
        'csvfile': ('destinations.csv', csvfilename.read_bytes(), 'text/csv')
    }
    resp = await client.post('/drone/upload_destinations', files=files)
    assert resp.status_code == 200
    assert len(drone_route._destinations) == 3


async def test_get_destinations(client: AsyncClient) -> None:
    drone_route._destinations = []

    resp = await client.get('/drone/get_destinations')
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 0

    drone_route._destinations = new_destinations()
    resp = await client.get('/drone/get_destinations')
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 3
