from io import StringIO
from hashlib import md5
from httpx import Client, Request
from typing import Any, Mapping, Optional
from last_fm_model import Method


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
