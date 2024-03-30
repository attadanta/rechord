from util import sign

secret = "secret"


def test_sign():
    params = {
        "method": "user.getRecentTracks",
        "api_key": "api_key",
        "foo": None,
        "sk": "session_key",
        "user": "user",
        "format": "json",
    }

    assert sign(params, secret) == "185a53fa45fb3bc0b13b757c231a0eac"
