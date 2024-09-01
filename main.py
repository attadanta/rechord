from dataclasses import dataclass
from datetime import datetime

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from last_fm_model import Album, Track
from stats import first_and_last_listen, tracks_in_album, unique_albums
from util import load_tracks_data


@dataclass
class AlbumSummary:
    mbid: str
    name: str


@dataclass
class AlbumDetails:
    name: str
    mbid: str
    first_listen: datetime
    last_listen: datetime
    total_playcount: int


class Store:
    def __init__(self, tracks: list[Track]):
        self.tracks = tracks

        self.albums = {
            album.mbid: AlbumSummary(album.mbid, album.name)
            for album in unique_albums(tracks)
            if album.mbid != "" and album.name != ""
        }


tracks = load_tracks_data("data")

albums = list(
    album for album in unique_albums(tracks) if album.mbid != "" and album.name != ""
)


def by_playcount(album: Album):
    return len(tracks_in_album(tracks, album))


albums.sort(key=by_playcount, reverse=True)


templates = Jinja2Templates(directory="templates")


api = FastAPI()


@api.get("/")
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "albums": [AlbumSummary(album.mbid, album.name) for album in albums],
        },
    )


@api.get("/albums")
async def albums_index():
    return albums


@api.get("/albums/{album_id}")
async def album_details(album_id: str) -> AlbumDetails:
    album = next((album for album in albums if album.mbid == album_id), None)

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
