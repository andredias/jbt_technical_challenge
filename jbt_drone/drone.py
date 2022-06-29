from haversine import Unit, haversine

from .schemas import Coords, Destination

_current_location = _store_coords = (0.0, 0.0)
_remaining_range = 5.0


class Drone:
    def __init__(self, drone_id: int) -> None:
        self.id = drone_id

    def choose_next_coords(self, destinations: list[Destination]) -> Coords:
        """
        The next destination is the one that is closest to the current location.
        It might lead to undefined delays to older orders but it is good enough
        for this implementation.

        Eventually, current_location, remaining_range and stored_coords
        must be replaced by object methods and properties contacting an
        external service to get these pieces of information.
        """
        current_location = self.current_location
        round_trips = (
            (
                d.coords,
                haversine(current_location, d.coords, Unit.MILES),
                haversine(d.coords, _store_coords, Unit.MILES),
            )
            for d in destinations
        )
        # it must be possible to go there and return to change batteries
        remaining_range = self.remaining_range
        reachable_destinations = (
            r for r in round_trips if remaining_range >= r[1] + r[2]
        )
        try:
            return min(reachable_destinations, key=lambda r: r[1])[0]
        except ValueError:
            return _store_coords  # get back home to replace the battery

    @property
    def current_location(self) -> Coords:
        return _current_location

    @property
    def remaining_range(self) -> float:
        return _remaining_range
