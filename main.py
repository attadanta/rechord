from dataclasses import dataclass
from datetime import datetime

from fastapi import FastAPI, HTTPException

from stats import first_and_last_listen, tracks_in_album, unique_albums
from util import load_tracks_data

tracks = load_tracks_data("data")
albums = list(
    album for album in unique_albums(tracks) if album.mbid != "" and album.name != ""
)


@dataclass
class AlbumDetails:
    name: str
    mbid: str
    first_listen: datetime
    last_listen: datetime
    total_playcount: int


api = FastAPI()


@api.get("/albums")
async def albums_index():
    return albums


@api.get("/albums/{album_id}")
async def album_details(album_id: int) -> AlbumDetails:
    album = albums[album_id]

    if not album:
        raise HTTPException(status_code=404, detail="Album not found")

    album_tracks = tracks_in_album(tracks, album)
    first, last = first_and_last_listen(album_tracks)

    return AlbumDetails(
        name=album.name,
        mbid=album.mbid,
        first_listen=first,
        last_listen=last,
        total_playcount=len(album_tracks),
    )
