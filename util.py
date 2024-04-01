import os
import json
from datetime import date, timedelta
from typing import Generator
from last_fm_model import Track, GetRecentTracksOutput


def date_intervals(
    start: date,
    end: date,
    interval: timedelta,
    epsilon: timedelta = timedelta(days=1),
) -> Generator[tuple[date, date], None, None]:
    """Returns a generator of equally long half-open segments between start and end."""
    current = start
    while current < end:
        next_date = min(current + interval, end)
        interval_end = next_date
        if next_date < end:
            interval_end -= epsilon
        yield current, interval_end
        current = next_date


def days_between(from_date: date, to_date: date) -> Generator[date, None, None]:
    while from_date <= to_date:
        yield from_date
        from_date += timedelta(days=1)


def get_renv(name: str) -> str:
    """Return the value of an environment variable. Throw an exception if it is not set."""
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"{name} environment variable is required")
    return value


def load_tracks_data(dir: str) -> list[Track]:
    tracks = []

    for tracks_file in [
        file
        for file in os.listdir(dir)
        if file.startswith("tracks_") and file.endswith(".json")
    ]:
        with open(tracks_file, "r") as f:
            data = json.load(f)
            recent_tracks_output = GetRecentTracksOutput(**data)
            tracks.extend(recent_tracks_output.recent_tracks.tracks)

    return tracks
