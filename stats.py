from collections.abc import Sequence
from datetime import datetime
from last_fm_model import Album, Track


def tracks_between(
    tracks: Sequence[Track], date_from: datetime, date_to: datetime
) -> list[Track]:
    """
    Given a list of tracks and two dates, return a list of tracks that were played between those dates.

    Args:
    tracks: A list of Track objects.
    date_from: The start date.
    date_to: The end date.

    Returns:
    A list of Track objects that were played between the given dates.
    """
    return [track for track in tracks if date_from <= track.timestamp.time <= date_to]


def unique_albums(tracks: Sequence[Track]) -> set[Album]:
    """
    Given a list of tracks, return a list of albums.

    Args:
    tracks: A list of Track objects.

    Returns:
    A list of unique album names.
    """
    return set(track.album for track in tracks)
