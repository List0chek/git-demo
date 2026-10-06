from report import format_report


class TestFormatReport:
    def test_starts_with_header(self) -> None:
        report = format_report({"Triage": 7.5})
        assert report.splitlines()[0] == "Average wait per station"

    def test_has_one_line_per_station(self) -> None:
        report = format_report({"Doctor": 32.5, "Triage": 7.5})
        station_lines = report.splitlines()[1:]
        assert len(station_lines) == 2
        assert station_lines[0].startswith("Doctor")
