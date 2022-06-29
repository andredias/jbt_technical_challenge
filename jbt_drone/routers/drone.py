from fastapi import APIRouter, Depends

from .. import drone as drone_lib
from ..authentication import authenticate_token
from ..schemas import Coords, Destination

router = APIRouter(prefix='/drone', tags=['drone'])

_destinations: list[Destination] = []


@router.get('/next_destination')
def get_next_destination(drone_id: int = Depends(authenticate_token)) -> Coords:
    global _destinations

    drone = drone_lib.Drone(drone_id)
    coords = drone.choose_next_coords(_destinations)

    # this point forward: simulation
    # simulate drone relocation so next call use new coordinates
    if coords != drone_lib._store_coords:
        drone_lib._current_location = coords
        # remove destination from list
        _destinations = [d for d in _destinations if d.coords != coords]
    # end of simulation

    return coords
