import json

class StationListReader:

    def __init__(self):
        # get the station list
        with open('.\station_list.json') as data_file:
            self.stations = json.load(data_file)

    def getNationalStations(self):
        return self.stations['national_stations']

    def getRegionalStations(self):
        return self.stations['regional_stations']

    def getLocalStations(self):
        return self.stations['local_stations']



