from pprint import pprint

from config.station_list_reader import StationListReader

stations = StationListReader ()

if (stations.get_errmsg() != None):
    print (stations.get_errmsg())
else:
    pprint (stations.get_national_stations ())
