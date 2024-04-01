from dataclasses import dataclass

from fastapi import FastAPI
from last_fm_model import (
    Track, Album
)
from stats import unique_albums, tracks_in_album

from util import load_tracks_data

tracks = load_tracks_data("data")
albums = list(album for album in unique_albums(tracks) if album.mbid != "")

@dataclass
class AlbumDetails:
    name: str
    artist: str
    tracks: list[Track]


api = FastAPI()


@api.get("/albums")
async def albums_index():
    return albums


@api.get("/albums/{album_id}")
async def album_details(album_id: int) -> Album:
    album = albums[album_id]
    album_tracks = tracks_in_album(tracks, album)
