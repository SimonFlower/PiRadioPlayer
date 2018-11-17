import json
import re

ZONE_NATIONAL = "NATIONAL"
ZONE_REGIONAL = "REGIONAL"
ZONE_LOCAL = "LOCAL"

class StationListReader:
    def __init__(self, station_list_filename: str, force_fail: bool = False):
        """
        Read the station list from a file
        :param station_list_filename: the file to read from
        :param force_fail a testing parameter - set true to force a failure

        If len(self.err) list is greater than zero, there were errors
        """
        self.err = list ()

        # compile a pattern to match colour constants in CSS (e.g "#FF0000")
        self.colour_pattern = re.compile("^#([A-F,a-f,0-9]){6}$")

        # catch exceptions so that the station list can still be used (though empty) even if there is an error
        try:
            if force_fail:
                raise RuntimeError ("Forcing failure")
            # get the station list
            with open(station_list_filename) as data_file:
                self.stations = json.load(data_file)
        except Exception as e:
            self.err += [str(e)]
            self.stations = dict ()
            self.stations['national_stations'] = list()
            self.stations['regional_stations'] = list()
            self.stations['local_stations'] = list()

        # check stations lists exist
        if not 'national_stations' in self.stations:
            self.err += ["National stations list missing from station list file"]
            self.stations ['national_stations'] = list ()
        if not 'regional_stations' in self.stations:
            self.err += ["Regional stations list missing from station list file"]
            self.stations['regional_stations'] = list()
        if not 'local_stations' in self.stations:
            self.err += ["Local stations list missing from station list file"]
            self.stations['local_stations'] = list()

        # check the station list - also add a unique ID to each station
        id = 1
        for station in self.get_station_list(ZONE_NATIONAL):
            self.__check_station__(station, id)
            id += 1
        for station in self.get_station_list(ZONE_REGIONAL):
            self.__check_station__(station, id)
            id += 1
        for station in self.get_station_list(ZONE_LOCAL):
            self.__check_station__(station, id)
            id += 1

    def get_station_list(self, zone: str) -> dict:
        """
        return national, regional or local stations from the stations list
        :param zone: one of the ZONE_ constants
        :return: the station details or None
        """
        if zone.upper() == ZONE_NATIONAL:
            return self.stations['national_stations']
        if zone.upper() == ZONE_REGIONAL:
            return self.stations['regional_stations']
        if zone.upper() == ZONE_LOCAL:
            return self.stations['local_stations']
        return list()

    def find_station (self, station_id: str) -> dict:
        """
        Given a station ID, find the station details
        :param station_id: the id of the station to find, in the form id_<int>
        :return: the station details or None
        """
        # search the station lists
        for station in self:
            if station['id'] == station_id:
                return station
        return None

    def __getitem__(self, item_index) -> dict:
        """
        Because sequences are iterable in Python, implemeting __getitem__ and __len__
        allows an object to be iterated
        :param item_index: the index of the item to return
        :return: the item
        """
        if item_index < 0:
            raise IndexError ("item_index out of range")
        if item_index < len (self.get_station_list(ZONE_NATIONAL)):
            return self.get_station_list(ZONE_NATIONAL)[item_index]
        item_index -= len (self.get_station_list(ZONE_NATIONAL))
        if item_index < len (self.get_station_list(ZONE_REGIONAL)):
            return self.get_station_list(ZONE_REGIONAL)[item_index]
        item_index -= len (self.get_station_list(ZONE_REGIONAL))
        if item_index < len (self.get_station_list(ZONE_LOCAL)):
            return self.get_station_list(ZONE_LOCAL)[item_index]
        raise IndexError ("item_index out of range")

    def __len__(self) -> int:
        """
        Because sequences are iterable in Python, implemeting __getitem__ and __len__
        allows an object to be iterated
        :return: the number of stations
        """
        return len(self.get_station_list(ZONE_NATIONAL)) + \
               len(self.get_station_list(ZONE_REGIONAL)) + \
               len(self.get_station_list(ZONE_LOCAL))

    def __check_station__(self, station: dict, id: int) -> None:
        station['id'] = "id_" + str(id)

        # attempt to read the mandatory fields, returing an error if they aren't present
        if not 'display_name' in station:
            self.err += ['Station missing display name: ' + id]
        if not 'streaming_url' in station:
            self.err += ['Station missing streaming URL: ' + id]

        # check for display colour and insert if not present (or malformed)
        if not 'display_colour' in station:
            station['display_colour'] = '#FF0000'
        elif not self.colour_pattern.match (station['display_colour']):
            station['display_colour'] = '#FF0000'

