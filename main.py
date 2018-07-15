from flask import Flask, redirect
from flask import render_template

from config import config
from config import station_list_reader
from audio_player import audio_mpd


app = Flask(__name__)

config = config.ConfigLocationFinder()
level = app.logger.getEffectiveLevel()
# TODO: make an info dialog where the config file location is displayed and remove this logging code
app.logger.setLevel('INFO')
app.logger.info("PiRadioPlayer station list: " + config.get_station_list_path())
app.logger.setLevel(level)
stations = station_list_reader.StationListReader(config.get_station_list_path())

# TODO: add a config that allows specifying non-default port (and host?) - pass them to this constructor:
audio_player = audio_mpd.AudioPlayer ()


@app.route('/')
def base_page() -> str:
    return render_template('base.html', content="/live/national")


@app.route('/station_selector/<string:zone>')
def station_selector(zone: str) -> str:
    return render_template('station_selector.html', stations=get_station_list_from_zone(zone))


@app.route('/play_bar')
def play_bar() -> str:
    return "Play bar holding page"


@app.route("/live/<string:zone>")
def live_show_stations(zone: str) -> str:
    return render_template('show_stations.html', title="National Stations", stations=get_station_list_from_zone(zone))


@app.route("/live_play/<path:url>")
def live_play(url: str) -> str:
    audio_player.live_stream_mpd(url)


def get_station_list_from_zone(zone: str) -> dict:
    if zone.upper() == "NATIONAL":
        return stations.get_national_stations()
    if zone.upper() == "REGIONAL":
        return stations.get_regional_stations()
    if zone.upper() == "LOCAL":
        return stations.get_local_stations()
    return None
