import json

class StationListReader:
    def __init__(self, station_list_filaname: str):
        # get the station list
        with open(station_list_filaname) as data_file:
            self.stations = json.load(data_file)
        # check the station list - also add a unique ID to each station
        id = 1
        for station in self.get_national_stations():
            self.check_station(station, id)
            id += 1
        for station in self.get_regional_stations():
            self.check_station(station, id)
            id += 1
        for station in self.get_local_stations():
            self.check_station(station, id)
            id += 1
        if len(self.get_national_stations()) <= 0:
            raise RuntimeError("No National Stations found in station list file")
        if len(self.get_regional_stations()) <= 0:
            raise RuntimeError("No Regional Stations found in station list file")
        if len(self.get_local_stations()) <= 0:
            raise RuntimeError("No Local Stations found in station list file")

    def get_national_stations(self) -> dict:
        return self.stations['national_stations']

    def get_regional_stations(self) -> dict:
        return self.stations['regional_stations']

    def get_local_stations(self) -> dict:
        return self.stations['local_stations']

    # return national, regional or local stations from the stations list
    def get_station_list_from_zone(self, zone: str) -> dict:
        if zone.upper() == "NATIONAL":
            return self.get_national_stations()
        if zone.upper() == "REGIONAL":
            return self.get_regional_stations()
        if zone.upper() == "LOCAL":
            return self.get_local_stations()
        return list()

    def check_station(self, station: dict, id: int) -> None:
        # add the ID to the station details
        station['id'] = "id_" + str(id)

        # attempt to read the mandatory fields, throwing an exception if they aren't present
        dsn = station['display_name']
        url = station['streaming_url']
