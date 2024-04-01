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


def sort_by_time_played(track: Track) -> datetime:
    """
    Given a track, return the time it was played.
    """
    return track.timestamp.time


def tracks_in_album(tracks: Sequence[Track], album: Album) -> list[Track]:
    """
    Given a list of tracks and an album, return a list of tracks that belong to that album.

    Args:
    tracks: A list of Track objects.
    album: An Album object.

    Returns:
    A list of Track objects that belong to the given album.
    """
    return [track for track in tracks if track.album == album]


def first_and_last_listen(tracks: Sequence[Track]) -> tuple[datetime, datetime]:
    """
    Given a sequence of tracks, return the first and last time played.
    """
    if not tracks:
        return (None, None)

    if len(tracks) == 1:
        return tracks[0].timestamp.time, tracks[0].timestamp.time

    sorted_tracks = sorted(tracks, key=sort_by_time_played)
    first, last = sorted_tracks[0], sorted_tracks[-1]

    return (first.timestamp.time, last.timestamp.time)
