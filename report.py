def format_report(average_waits: dict[str, float]) -> str:
    """
    Format average waits as a plain-text report.

    Args:
        average_waits: Average wait in minutes, keyed by station name.

    Returns:
        A header line followed by one line per station.
    """
    lines = ["Average wait per station"]
    for station, minutes in average_waits.items():
        lines.append(f"{station}: {minutes:.1f} min")
    return "\n".join(lines)
