from fastapi import FastAPI
from last_fm_model import (
    Track, Album
)
from stats import unique_albums

from util import load_tracks_data

tracks = load_tracks_data("data")
albums = list(unique_albums(tracks))


api = FastAPI()


@api.get("/albums")
async def albums_index():
    return albums


@api.get("/albums/{album_id}")
async def album_detail(album_id: int) -> Album:
    return albums[album_id]
