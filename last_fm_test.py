import unittest
from dataclasses import asdict

from last_fm import GetRecentTracksInput


class LastFMTest(unittest.TestCase):
    def test_recent_tracks_input_data_class_dict(self):
        i = GetRecentTracksInput(
            user="user", api_key="api_key", from_date=1, to_date=2, extended=1
        )
        expected = {
            "user": "user",
            "api_key": "api_key",
            "session_key": None,
            "from_date": 1,
            "to_date": 2,
            "limit": 20,
            "extended": 1,
        }
        self.assertEqual(asdict(i), expected)
