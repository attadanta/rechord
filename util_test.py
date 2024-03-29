from util import sign
from unittest import TestCase

secret = "secret"


class TestSign(TestCase):
    def test_sign(self):
        params = {
            "method": "user.getRecentTracks",
            "api_key": "api_key",
            "foo": None,
            "sk": "session_key",
            "user": "user",
        }

        self.assertEqual(sign(params, secret), "185a53fa45fb3bc0b13b757c231a0eac")
