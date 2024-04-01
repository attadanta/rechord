from util import date_intervals
from datetime import date, timedelta
from last_fm_model import Method
from last_fm_client import sign

secret = "secret"


def test_time_intervals():
    intervals = list(
        date_intervals(date(2024, 3, 1), date(2024, 3, 31), timedelta(days=7))
    )
    assert intervals == [
        (date(2024, 3, 1), date(2024, 3, 7)),
        (date(2024, 3, 8), date(2024, 3, 14)),
        (date(2024, 3, 15), date(2024, 3, 21)),
        (date(2024, 3, 22), date(2024, 3, 28)),
        (date(2024, 3, 29), date(2024, 3, 31)),
    ]


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
