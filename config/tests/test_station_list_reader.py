import unittest
import os
from .. import station_list_reader


class TestStationListReader (unittest.TestCase):

    def setUp(self):
        filename = os.path.join(os.path.dirname(__file__), "..", "..", "initial_data", "station_list.json")
        self.slr = station_list_reader.StationListReader(filename)

    def test_get_national_stations(self) -> None:
        stations = self.slr.get_national_stations()
        self.assertEqual(len(stations), 13)

    def test_get_regional_stations(self) -> None:
        stations = self.slr.get_regional_stations()
        self.assertEqual(len(stations), 6)

    def test_get_local_stations(self) -> None:
        stations = self.slr.get_local_stations()
        self.assertEqual(len(stations), 40)

    def test_get_errmsg(self) -> None:
        self.assertIsNone(self.slr.get_errmsg())

