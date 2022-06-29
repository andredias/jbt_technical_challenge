import csv
from io import StringIO

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import ValidationError

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


@router.post('/upload_destinations')
async def load_destinations(csvfile: UploadFile = File(...)) -> None:
    global _destinations
    buffer = StringIO((await csvfile.read()).decode())
    try:
        _destinations = [Destination(**d) for d in csv.DictReader(buffer)]
    except ValidationError:
        raise HTTPException(
            422,
            detail='csv file must contain a timestamp, float, float records '
            'correponding to the order time, latitute and longitute',
        )
    return


@router.get('/get_destinations', response_model=list[Destination])
async def get_destinations() -> list[Destination]:
    return _destinations
