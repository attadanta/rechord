from fastapi import FastAPI
from last_fm_model import (
    Track,
)
from stats import unique_albums

from util import load_tracks_data

tracks = load_tracks_data("data")


api = FastAPI()


@api.get("/albums")
async def albums_index():
    return unique_albums(tracks)


@api.get("/albums/{album_id}")
async def album_detail(album_id: int) -> Track:
    return tracks[album_id]
