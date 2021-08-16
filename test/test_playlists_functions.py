import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

import config
from playlists_functions import parse_playlists_dates,\
    parse_string_to_date,\
    get_latest_date_string,\
    get_daily_playlist,\
    shuffle


class TestPlaylistsFunctions(unittest.TestCase):

    def test_parse_date_valid_date(self):
        EXPECTED = datetime(2021, 4, 12)
        date_for_test = '20210412'
        result = parse_string_to_date(date_for_test)
        self.assertEqual(EXPECTED, result)

    def test_parse_date_unexisting_date(self):
        date_for_test = '20210431'
        self.assertRaises(ValueError, parse_string_to_date, date_for_test)

    def test_get_latest_date_string(self):
        EXPECTED = '20210702'
        playlists_data = {"20210701": ["aa", "bb", "cc"], "20210702": ["dd", "ff", "cc"]}
        actual = get_latest_date_string(playlists_data)
        self.assertEqual(EXPECTED, actual)

    def test_get_latest_date_string_empty_dict(self):
        self.assertRaises(Exception, get_latest_date_string, {})

    def test_get_latest_data_string_future_dates(self):
        EXPECTED = '20210710'
        future_date = (datetime.today() + timedelta(days=1)).strftime(config.DATE_FORMAT)
        playlist_data = {"20210710": ["aa", "bb", "cc"], future_date: ["dd", "ff", "cc"]}
        actual = get_latest_date_string(playlist_data)
        self.assertEqual(EXPECTED, actual)

    def test_parse_playlists_dates(self):
        EXPECTED = [datetime(2021, 2, 15), datetime(2021, 2, 19), datetime(2021, 2, 25)]
        playlist_data_json = {"20210215": ["aa", "bb", "cc", "dd"],
                              "20210219": ["dd", "ee", "cc", "aa"],
                              "20210225": ["vv", "gg", "xx", "zz"]}
        actual = parse_playlists_dates(playlist_data_json)
        self.assertEqual(EXPECTED, actual)

    def test_parse_playlists_dates_invalid_date_format(self):
        EXPECTED = [datetime(2021, 2, 2), datetime(2021, 2, 3)]
        playlist_data_json = {"202102010": ["aa", "bb", "cc", "dd"],
                              "20210202": ["dd", "ee", "cc", "aa"],
                              "2021020": ["dd", "ee", "cc", "aa"],
                              "20210203": ["vv", "gg", "xx", "zz"]}
        actual = parse_playlists_dates(playlist_data_json)
        self.assertEqual(EXPECTED, actual)

    def test_parse_playlists_dates_unexisting_date(self):
        EXPECTED = [datetime(2021, 2, 1), datetime(2021, 2, 3)]
        playlist_data_json = {"20210201": ["aa", "bb", "cc", "dd"],
                              "20210230": ["dd", "ee", "cc", "aa"],
                              "20210203": ["vv", "gg", "xx", "zz"]}
        actual = parse_playlists_dates(playlist_data_json)
        self.assertEqual(EXPECTED, actual)

    def test_parse_playlists_dates_empty_dict(self):
        EXPECTED = []
        actual = parse_playlists_dates({})
        self.assertEqual(EXPECTED, actual)

    def test_parse_date_invalid_date(self):
        date_for_test = '202104301'
        self.assertRaises(ValueError, parse_string_to_date, date_for_test)

    @patch("playlists_functions.fetch_playlists_data")
    def test_get_daily_playlist(self, mock_fetch_playlists_data):
        EXPECTED = ["vv", "gg", "xx", "zz"]
        today_date = datetime.today().strftime(config.DATE_FORMAT)
        playlists_data = {"20210215": ["aa", "bb", "cc", "dd"],
                          "20210219": ["dd", "ee", "cc", "aa"],
                          today_date: ["vv", "gg", "xx", "zz"]}
        mock_fetch_playlists_data.return_value = playlists_data
        actual = get_daily_playlist()
        self.assertEqual(EXPECTED, actual)

    @patch("playlists_functions.fetch_playlists_data")
    def test_get_daily_playlist_empty_json(self, mock_fetch_playlists_data):
        playlists_data = {}
        mock_fetch_playlists_data.return_value = playlists_data
        self.assertRaises(Exception, get_latest_date_string)

    def test_shuffle(self):
        playlist = ["vv", "gg", "xx", "zz"]
        actual = shuffle(playlist)
        self.assertCountEqual(playlist, actual)

    def test_shuffle_empty_playlist(self):
        EXPECTED = []
        actual = shuffle([])
        self.assertEqual(EXPECTED, [])









