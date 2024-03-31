from util import sign
from last_fm import Method

secret = "secret"


def test_sign():
    params = {
        "method": Method.user_get_recent_tracks,
        "api_key": "api_key",
        "foo": None,
        "sk": "session_key",
        "user": "user",
        "format": "json",
    }

    assert sign(params, secret) == "185a53fa45fb3bc0b13b757c231a0eac"
