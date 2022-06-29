from fastapi import APIRouter, Depends

from ..authentication import authenticate_token
from ..drone import Drone
from ..schemas import Coords, Destination

router = APIRouter(prefix='/drone', tags=['drone'])

_destinations: list[Destination] = []


@router.get('/next_destination')
def get_next_destination(drone_id: int = Depends(authenticate_token)) -> Coords:
    drone = Drone(drone_id)
    return drone.choose_next_coords(_destinations)
