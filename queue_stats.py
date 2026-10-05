from dataclasses import dataclass


@dataclass(slots=True)
class Visit:
    """
    A case's stay at one station.

    Attributes:
        case_id: Identifier of the case.
        station: Name of the station.
        arrival_minute: Minute the case arrived at the station.
        service_start_minute: Minute the station started serving the case.
    """
    case_id: str
    station: str
    arrival_minute: int
    service_start_minute: int


def wait_minutes(visit: Visit) -> int:
    """
    Compute how long a case waited in the queue.

    Args:
        visit: The visit to measure.

    Returns:
        Minutes between arrival and service start.
    """
    if visit.service_start_minute < visit.arrival_minute:
        raise ValueError(f"Service starts before arrival for case {visit.case_id}.")
    return visit.service_start_minute - visit.arrival_minute


def average_wait_by_station(visits: list[Visit]) -> dict[str, float]:
    """
    Compute the average wait per station.

    Args:
        visits: Visits to aggregate.

    Returns:
        Average wait in minutes, keyed by station name, sorted by station name.
    """
    waits_by_station: dict[str, list[int]] = {}
    for visit in visits:
        waits_by_station.setdefault(visit.station, []).append(wait_minutes(visit))
    return {
        station: sum(waits) / len(waits)
        for station, waits in sorted(waits_by_station.items())
    }
