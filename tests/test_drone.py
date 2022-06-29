from datetime import datetime, timedelta

from jbt_drone import drone as lib
from jbt_drone.schemas import Destination


def test_drone() -> None:
    drone = lib.Drone(1)
    lib._current_location = lib._store_coords = (-22.8209783, -47.2389362)

    # empty list of destinations. Stay at the store
    assert drone.choose_next_coords([]) == lib._store_coords

    destinations = [
        Destination(
            time=datetime.now() - timedelta(minutes=10),
            lat=-22.8144896,
            long=-47.2555224,
        ),
        Destination(time=datetime.now(), lat=-22.8186593, long=-47.2557496),
        Destination(
            time=datetime.now() - timedelta(minutes=15),
            lat=-22.8313904,
            long=-47.2718947,
        ),
        Destination(
            time=datetime.now() - timedelta(minutes=5),
            lat=-22.8013904,
            long=-47.2818947,
        ),
        Destination(
            time=datetime.now() - timedelta(minutes=1),
            lat=-22.7313904,
            long=-47.2718947,
        ),
    ]

    # choose the closest destination
    coords = drone.choose_next_coords(destinations)
    assert coords == destinations[1].coords

    # choose next closest destination
    lib._current_location = destinations.pop(1).coords
    coords = drone.choose_next_coords(destinations)
    assert coords == destinations[0].coords

    # The remaining range is not enough. The drone must return to the store
    lib._current_location = destinations.pop(0).coords
    lib._remaining_range = 3.5
    coords = drone.choose_next_coords(destinations)
    assert coords == lib._store_coords
