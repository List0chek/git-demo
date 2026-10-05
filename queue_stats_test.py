import pytest

from queue_stats import Visit, average_wait_by_station, wait_minutes


class TestWaitMinutes:
    def test_wait_is_time_from_arrival_to_service(self) -> None:
        visit = Visit(case_id="c1", station="Triage", arrival_minute=10, service_start_minute=25)
        assert wait_minutes(visit) == 15

    def test_service_before_arrival_raises(self) -> None:
        visit = Visit(case_id="c1", station="Triage", arrival_minute=30, service_start_minute=20)
        with pytest.raises(ValueError):
            wait_minutes(visit)


class TestAverageWaitByStation:
    def test_averages_each_station_separately(self) -> None:
        visits = [
            Visit(case_id="c1", station="Triage", arrival_minute=0, service_start_minute=5),
            Visit(case_id="c2", station="Triage", arrival_minute=0, service_start_minute=15),
            Visit(case_id="c1", station="Doctor", arrival_minute=10, service_start_minute=40)
        ]
        assert average_wait_by_station(visits) == {"Doctor": 30.0, "Triage": 10.0}
