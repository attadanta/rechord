from io import StringIO
from hashlib import md5
import os
from datetime import date, timedelta
from typing import Generator
from httpx import Client


def days_between(from_date: date, to_date: date) -> Generator[date, None, None]:
    while from_date <= to_date:
        yield from_date
        from_date += timedelta(days=1)


def create_authorization_client(base_url: str, api_key: str) -> Client:
    return Client(
        base_url=base_url,
        params={"api_key": api_key},
    )


def create_unauthorized_client(base_url: str, api_key: str) -> Client:
    return Client(
        base_url=base_url,
        params={"api_key": api_key, "format": "json"},
    )


def create_authorized_client(
    base_url: str, api_key: str, user: str, session_key: str
) -> Client:
    return Client(
        base_url=base_url,
        params={"api_key": api_key, "user": user, "sk": session_key, "format": "json"},
    )


def get_renv(name: str) -> str:
    """Return the value of an environment variable. Throw an exception if it is not set."""
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"{name} environment variable is required")
    return value


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
