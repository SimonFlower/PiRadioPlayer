import json

class StationListReader:
    def __init__(self, station_list_filaname: str):
        self.errmsg = ""
        try:
            # get the station list
            with open(station_list_filaname) as data_file:
                self.stations = json.load(data_file)
            # check the station list
            for station in self.get_national_stations():
                self.check_station(station)
            for station in self.get_regional_stations():
                self.check_station(station)
            for station in self.get_local_stations():
                self.check_station(station)
            n_stations = len(self.get_national_stations()) + \
                         len(self.get_regional_stations()) + \
                         len(self.get_local_stations())
            if n_stations < 0:
                self.errmsg = "No stations found in station list file"
        except Exception as e:
            self.errmsg = repr(e)

    def get_national_stations(self) -> dict:
        if self.errmsg == None:
            return None
        return self.stations['national_stations']

    def get_regional_stations(self) -> dict:
        if self.errmsg == None:
            return None
        return self.stations['regional_stations']

    def get_local_stations(self) -> dict:
        if self.errmsg == None:
            return None
        return self.stations['local_stations']

    def get_errmsg(self) -> str:
        if len (self.errmsg) == 0:
            return None
        return self.errmsg

    def check_station(self, station: dict) -> None:
        # attempt to read the mandatory fields, throwing an exception if they aren't present
        ipn = station['iplayer_name']
        dsn = station['display_name']
