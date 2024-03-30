from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


@dataclass
class Attributes(BaseModel):
    page: int
    perPage: int
    user: str
    total: int
    totalPages: int


@dataclass
class Timestamp(BaseModel):
    time: datetime = Field(alias="uts")


@dataclass
class Image(BaseModel):
    size: Literal["small", "medium", "large", "extralarge"]
    url: str = Field(alias="#text")


@dataclass
class Artist(BaseModel):
    name: str = Field(alias="#text")
    mbid: str


@dataclass
class Album(BaseModel):
    mbid: str
    name: str = Field(alias="#text")


@dataclass
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


@dataclass
class GetTokenOutput(BaseModel):
    """
    The output for the auth.getToken API method

    See https://www.last.fm/api/show/auth.getToken
    """

    token: str


@dataclass
class Session(BaseModel):
    """
    The session object returned by the auth.getSession API method

    See https://www.last.fm/api/show/auth.getSession
    """

    name: str
    key: str
    subscriber: Literal[0, 1]


@dataclass
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


@dataclass
class Tracklist(BaseModel):
    tracks: list[Track] = Field(alias="track")
    attributes: Attributes = Field(alias="@attr")


@dataclass
class GetRecentTracksOutput(BaseModel):
    track_list: Tracklist = Field(alias="recenttracks")
