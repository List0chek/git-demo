from queue_stats import Visit, average_wait_by_station
from report import format_report

SAMPLE_VISITS = [
    Visit(case_id="c1", station="Triage", arrival_minute=0, service_start_minute=5),
    Visit(case_id="c2", station="Triage", arrival_minute=3, service_start_minute=13),
    Visit(case_id="c1", station="Doctor", arrival_minute=15, service_start_minute=40),
    Visit(case_id="c2", station="Doctor", arrival_minute=25, service_start_minute=65),
    Visit(case_id="c1", station="Lab", arrival_minute=50, service_start_minute=68)
]


def main() -> None:
    """
    Print the wait report for the sample visits.
    """
    print(format_report(average_wait_by_station(SAMPLE_VISITS)))


if __name__ == "__main__":
    main()
