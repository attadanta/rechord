from dataclasses import dataclass
from typing import Literal, Optional

from pydantic import BaseModel


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


@dataclass
class AuthorizationInput:
    api_key: str
    token: str


@dataclass
class GetRecentTracksInput:
    user: str
    api_key: str
    from_date: int
    to_date: int
    session_key: Optional[str] = None
    limit: int = 20
    extended: Literal[0, 1] = 0
