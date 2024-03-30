from dataclasses import asdict
from pydantic import ValidationError
from pytest import raises as pytest_raises
from datetime import datetime, timezone

from last_fm import GetRecentTracksInput, Image, Timestamp


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
