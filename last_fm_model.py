from enum import StrEnum
from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass as pydantic_dataclass


class Method(StrEnum):
    user_get_recent_tracks = "user.getRecentTracks"
    auth_get_token = "auth.getToken"
    auth_get_session = "auth.getSession"


@pydantic_dataclass(frozen=True)
class Error:
    error: int
    message: str


@pydantic_dataclass(frozen=True)
class Attributes:
    page: int
    perPage: int
    user: str
    total: int
    totalPages: int


class Timestamp(BaseModel):
    time: datetime = Field(alias="uts")


@pydantic_dataclass(frozen=True)
class Image:
    size: Literal["small", "medium", "large", "extralarge"]
    url: str = Field(alias="#text")


@pydantic_dataclass(frozen=True)
class Artist:
    mbid: str
    name: str = Field(alias="#text")


@pydantic_dataclass(frozen=True)
class Album:
    mbid: str
    name: str = Field(alias="#text")


@pydantic_dataclass(frozen=True)
class Track:
    artist: Artist
    mbid: str
    album: Album
    name: str
    url: str
    images: list[Image] = Field(alias="image")
    timestamp: Timestamp = Field(alias="date")


@dataclass(frozen=True)
class GetTokenInput:
    """
    The input for the auth.getToken API method

    See https://www.last.fm/api/show/auth.getToken
    """

    api_key: str


@pydantic_dataclass(frozen=True)
class GetTokenOutput:
    """
    The output for the auth.getToken API method

    See https://www.last.fm/api/show/auth.getToken
    """

    token: str


@pydantic_dataclass(frozen=True)
class Session:
    """
    The session object returned by the auth.getSession API method

    See https://www.last.fm/api/show/auth.getSession
    """

    name: str
    key: str
    subscriber: Literal[0, 1]


@pydantic_dataclass(frozen=True)
class GetSessionOutput:
    """
    The session object returned by the auth.getSession API method

    See https://www.last.fm/api/show/auth.getSession
    """

    session: Session


@dataclass(frozen=True)
class GetRecentTracksInput:
    user: str
    date_from: datetime
    date_to: datetime
    page: int = 1
    limit: int = 20
    extended: Literal[0, 1] = 0

    def as_params(self) -> dict:
        return {
            "user": self.user,
            "from": int(self.date_from.timestamp()),
            "to": int(self.date_to.timestamp()),
            "page": self.page,
            "limit": self.limit,
            "extended": self.extended,
        }


@pydantic_dataclass(frozen=True)
class Tracklist:
    tracks: list[Track] = Field(alias="track")
    attributes: Attributes = Field(alias="@attr")


@pydantic_dataclass(frozen=True)
class GetRecentTracksOutput:
    recent_tracks: Tracklist = Field(alias="recenttracks")
