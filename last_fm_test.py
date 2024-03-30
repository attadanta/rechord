from dataclasses import asdict
from pydantic import ValidationError
from pytest import raises as pytest_raises
from datetime import datetime, timezone

from last_fm import GetRecentTracksInput, Image, Timestamp, Track


def test_recent_tracks_input_data_class_dict():
    i = GetRecentTracksInput(user="user", from_date=1, to_date=2, extended=1)
    expected = {
        "user": "user",
        "from_date": 1,
        "to_date": 2,
        "limit": 20,
        "extended": 1,
    }
    assert asdict(i) == expected


def test_timestamp_deserialization():
    data = {"uts": "1711782712", "#text": "30 Mar 2024, 07:11"}
    timestamp = Timestamp(**data)
    assert timestamp.time == datetime(2024, 3, 30, 7, 11, 52, tzinfo=timezone.utc)


def test_image_deserialization():
    data = {"size": "small", "#text": "https://last.fm/image.jpg"}
    image = Image(**data)
    assert image.size == "small"
    assert image.url == "https://last.fm/image.jpg"


def test_image_deserialization_invalidates():
    with pytest_raises(ValidationError):
        data = {"size": "smol", "#text": "https://last.fm/image.jpg"}
        Image(**data)


def test_track_deserialization():
    data = {
        "artist": {"mbid": "", "#text": "Suede"},
        "streamable": "0",
        "image": [
            {
                "size": "small",
                "#text": "https://lastfm.freetls.fastly.net/i/u/34s/bdd3d12695b4f7f67619fcc5236e5b3b.png",
            },
            {
                "size": "medium",
                "#text": "https://lastfm.freetls.fastly.net/i/u/64s/bdd3d12695b4f7f67619fcc5236e5b3b.png",
            },
            {
                "size": "large",
                "#text": "https://lastfm.freetls.fastly.net/i/u/174s/bdd3d12695b4f7f67619fcc5236e5b3b.png",
            },
            {
                "size": "extralarge",
                "#text": "https://lastfm.freetls.fastly.net/i/u/300x300/bdd3d12695b4f7f67619fcc5236e5b3b.png",
            },
        ],
        "mbid": "",
        "album": {"mbid": "04215404-8b0b-4c9f-bef9-f64203f6d15c", "#text": "Suede"},
        "name": "Animal Nitrate",
        "url": "https://www.last.fm/music/Suede/_/Animal+Nitrate",
        "date": {"uts": "1711782712", "#text": "30 Mar 2024, 07:11"},
    }

    track = Track(**data)
    assert track.artist.name == "Suede"
    assert track.artist.mbid == ""
    assert track.album.mbid == "04215404-8b0b-4c9f-bef9-f64203f6d15c"
    assert track.album.name == "Suede"
    assert track.timestamp.time == datetime(2024, 3, 30, 7, 11, 52, tzinfo=timezone.utc)
