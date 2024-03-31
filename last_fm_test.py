from pydantic import ValidationError
from pytest import raises as pytest_raises
from datetime import datetime, timezone

from last_fm import (
    GetRecentTracksInput,
    Image,
    Timestamp,
    Track,
    Attributes,
    GetRecentTracksOutput,
)


def test_recent_tracks_input_data_class_dict():
    date_from = datetime(2024, 3, 30, 7, 11, 52, tzinfo=timezone.utc)
    date_to = datetime(2024, 3, 30, 7, 11, 52, tzinfo=timezone.utc)

    i = GetRecentTracksInput(
        user="user", date_from=date_from, date_to=date_to, extended=1
    )
    expected = {
        "user": "user",
        "from": int(date_from.timestamp()),
        "to": int(date_to.timestamp()),
        "page": 1,
        "limit": 20,
        "extended": 1,
    }
    assert i.model_dump(by_alias=True) == expected


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


def test_attributes_deserialization():
    data = {
        "user": "rj",
        "totalPages": "4779",
        "page": "1",
        "perPage": "50",
        "total": "238917",
    }
    attributes = Attributes(**data)

    assert attributes.user == "rj"
    assert attributes.totalPages == 4779
    assert attributes.page == 1
    assert attributes.perPage == 50
    assert attributes.total == 238917


def test_recent_tracks_output_deserialization():
    data = {
        "recenttracks": {
            "track": [
                {
                    "artist": {"mbid": "", "#text": "Suede"},
                    "streamable": "0",
                    "image": [
                        {
                            "size": "small",
                            "#text": "https://lastfm.freetls.fastly.net/i/u/34s/8c0d651a01874200ac82475b92854f20.jpg",
                        },
                        {
                            "size": "medium",
                            "#text": "https://lastfm.freetls.fastly.net/i/u/64s/8c0d651a01874200ac82475b92854f20.jpg",
                        },
                        {
                            "size": "large",
                            "#text": "https://lastfm.freetls.fastly.net/i/u/174s/8c0d651a01874200ac82475b92854f20.jpg",
                        },
                        {
                            "size": "extralarge",
                            "#text": "https://lastfm.freetls.fastly.net/i/u/300x300/8c0d651a01874200ac82475b92854f20.jpg",
                        },
                    ],
                    "mbid": "7fd9a27a-e5de-4f56-900d-a6ef66c38b62",
                    "album": {
                        "mbid": "",
                        "#text": "Dog Man Star (Remastered) [Deluxe Edition]",
                    },
                    "name": "The Asphalt World (Remastered)",
                    "url": "https://www.last.fm/music/Suede/_/The+Asphalt+World+(Remastered)",
                    "date": {"uts": "1711788633", "#text": "30 Mar 2024, 08:50"},
                },
            ],
            "@attr": {
                "user": "scrbl",
                "totalPages": "4779",
                "page": "1",
                "perPage": "50",
                "total": "238917",
            },
        }
    }

    output = GetRecentTracksOutput(**data)

    track_list = output.recent_tracks

    assert len(output.recent_tracks.tracks) == 1
    assert track_list.tracks[0].artist.name == "Suede"
    assert track_list.attributes.user == "scrbl"
