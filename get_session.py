import sys
import os
from httpx import Client
from last_fm_client import create_signed_get_request, create_unauthorized_client
from last_fm_model import Method, GetTokenOutput, GetSessionOutput
import argparse


def get_token(client: Client, secret: str) -> str:
    request = create_signed_get_request(
        client=client, method=Method.auth_get_token, secret=secret
    )

    token_res = client.send(request)
    get_token_output = GetTokenOutput(**token_res.json())

    return get_token_output.token


def get_session_key(client: Client, token: str, secret: str) -> str:
    request = create_signed_get_request(
        client=client,
        method=Method.auth_get_session,
        secret=secret,
        params={"token": token},
    )

    response_body = client.send(request).json()
    get_session_output = GetSessionOutput(**response_body)
    return get_session_output.session.key


def main():
    """
    Get a session key from Last.fm.

    The session key is required to make authenticated requests to the Last.fm API.

    See https://www.last.fm/api/desktopauth
    """
    parser = argparse.ArgumentParser(description="Get a session key from Last.fm.")
    parser.add_argument(
        "--api-key",
        help="Your API key",
        required=True,
        dest="api_key",
    )
    parser.add_argument(
        "--secret", help="Your API secret", required=True, dest="secret"
    )

    args = parser.parse_args()

    api_key = args.api_key
    secret = args.secret

    base_url = os.getenv("BASE_URL", "https://ws.audioscrobbler.com/")
    unauthorized_client = create_unauthorized_client(base_url=base_url, api_key=api_key)

    token = get_token(unauthorized_client, secret)

    print(
        f"Go to https://www.last.fm/api/auth/?api_key={api_key}&token={token} and press return after you log in.",
        file=sys.stderr,
    )
    input()

    session_key = get_session_key(unauthorized_client, token, secret)
    print(session_key)


if __name__ == "__main__":
    main()
