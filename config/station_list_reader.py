import json

class StationListReader:
    def __init__(self, station_list_filename: str):
        """
        Read the station list from a file
        :param station_list_filename: the file to read from

        If self.err list is greater than zero, there were errors
        """
        self.err = list ()

        # catch exceptions so that the station list can still be used (though empty) even if there is an error
        try:
            # get the station list
            with open(station_list_filename) as data_file:
                self.stations = json.load(data_file)
        except Exception as e:
            self.err += [str(e)]
            self.stations = dict ()

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
        for station in self.get_station_list("national"):
            self.__check_station__(station, id)
            id += 1
        for station in self.get_station_list("regional"):
            self.__check_station__(station, id)
            id += 1
        for station in self.get_station_list("local"):
            self.__check_station__(station, id)
            id += 1

    # return national, regional or local stations from the stations list
    def get_station_list(self, zone: str) -> dict:
        if zone.upper() == "NATIONAL":
            return self.stations['national_stations']
        if zone.upper() == "REGIONAL":
            return self.stations['regional_stations']
        if zone.upper() == "LOCAL":
            return self.stations['local_stations']
        return list()

    def __check_station__(self, station: dict, id: int) -> None:
        station['id'] = "id_" + str(id)

        # attempt to read the mandatory fields, returing an error if they aren't present
        if not 'display_name' in station:
            self.err += ['Station missing display name: ' + id]
        if not 'streaming_url' in station:
            self.err += ['Station missing streaming URL: ' + id]
