from io import StringIO
from hashlib import md5
import os
import json
from datetime import date, timedelta
from typing import Generator, Any, Mapping, Optional
from httpx import Client, Request
from .last_fm_model import Method, Track, GetRecentTracksOutput


def date_intervals(
    start: date,
    end: date,
    interval: timedelta,
    epsilon: timedelta = timedelta(days=1),
) -> Generator[tuple[date, date], None, None]:
    current = start
    while current < end:
        next_date = min(current + interval, end)
        interval_end = next_date
        if next_date < end:
            interval_end -= epsilon
        yield current, interval_end
        current = next_date


def days_between(from_date: date, to_date: date) -> Generator[date, None, None]:
    while from_date <= to_date:
        yield from_date
        from_date += timedelta(days=1)


def create_unauthorized_client(base_url: str, api_key: str) -> Client:
    return Client(
        base_url=base_url,
        params={"api_key": api_key, "format": "json"},
    )


def create_authorized_client(base_url: str, api_key: str, session_key: str) -> Client:
    return Client(
        base_url=base_url,
        params={"api_key": api_key, "sk": session_key, "format": "json"},
    )


def get_renv(name: str) -> str:
    """Return the value of an environment variable. Throw an exception if it is not set."""
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"{name} environment variable is required")
    return value


def load_tracks_data(dir: str) -> list[Track]:
    tracks = []

    for file in os.listdir(dir):
        with open(file, "r") as f:
            data = json.load(f)
            recent_tracks_output = GetRecentTracksOutput(**data)
            tracks.extend(recent_tracks_output.recent_tracks.tracks)

    return tracks


def create_signed_get_request(
    client: Client,
    method: Method,
    secret: str,
    params: Optional[Mapping[str, Any]] = None,
) -> Request:
    """
    Create a signed GET request for the given method and parameters.
    """
    if params is None:
        params = {}

    request_params = {}
    request_params.update(client.params)
    request_params.update(params)
    request_params["method"] = method
    request_params["api_sig"] = sign(request_params, secret)

    return client.build_request("GET", "/2.0", params=request_params)


def sign(params: dict[str, str], secret: str) -> str:
    """
    Compute the request signature (32-character hexadecimal md5 hash) for the given parameters and secret.

    See https://www.last.fm/api/webauth#_6-sign-your-calls
    """
    sorted_keys = sorted(
        [key for key in params.keys() if params[key] is not None and key != "format"]
    )

    message = StringIO()
    message.write("".join(f"{key}{params[key]}" for key in sorted_keys))
    message.write(secret)

    message_string = message.getvalue()
    message_bytes = message_string.encode("utf-8")

    hasher = md5()
    hasher.update(message_bytes)
    return hasher.hexdigest()
