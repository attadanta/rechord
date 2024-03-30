from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class Attributes(BaseModel):
    page: int
    perPage: int
    user: str
    total: int
    totalPages: int


class Timestamp(BaseModel):
    time: datetime = Field(alias="uts")


class Image(BaseModel):
    size: Literal["small", "medium", "large", "extralarge"]
    url: str = Field(alias="#text")


class Artist(BaseModel):
    name: str = Field(alias="#text")
    mbid: str


class Album(BaseModel):
    mbid: str
    name: str = Field(alias="#text")


class Track(BaseModel):
    artist: Artist
    images: list[Image] = Field(alias="image")
    mbid: str
    album: Album
    name: str
    url: str
    timestamp: Timestamp = Field(alias="date")


@dataclass
class GetTokenInput:
    """
    The input for the auth.getToken API method

    See https://www.last.fm/api/show/auth.getToken
    """

    api_key: str


class GetTokenOutput(BaseModel):
    """
    The output for the auth.getToken API method

    See https://www.last.fm/api/show/auth.getToken
    """

    token: str


class Session(BaseModel):
    """
    The session object returned by the auth.getSession API method

    See https://www.last.fm/api/show/auth.getSession
    """

    name: str
    key: str
    subscriber: Literal[0, 1]


class GetSessionOutput(BaseModel):
    """
    The session object returned by the auth.getSession API method

    See https://www.last.fm/api/show/auth.getSession
    """

    session: Session


@dataclass
class GetRecentTracksInput:
    user: str
    from_date: int
    to_date: int
    limit: int = 20
    extended: Literal[0, 1] = 0


class Tracklist(BaseModel):
    tracks: list[Track] = Field(alias="track")
    attributes: Attributes = Field(alias="@attr")


class GetRecentTracksOutput(BaseModel):
    track_list: Tracklist = Field(alias="recenttracks")
