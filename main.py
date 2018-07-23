from flask import Flask, redirect
from flask import render_template

from config import config_utils
from config import station_list_reader
from audio_player import audio_mpd

import urllib


# initialise Flask
app = Flask(__name__)

# top level application variables
err_msgs = list ()
info_msgs = list ()
program_config = None
stations = None
audio_player = None

# initialise configuration
try:
    program_config = config_utils.ConfigLocationFinder()
    info_msgs += ["Station list: " + program_config.get_station_list_path()]
except Exception as e:
    err_msgs += ["Error finding configuration: " + repr(e)]

# load list of stations
try:
    if program_config is not None:
        stations = station_list_reader.StationListReader(program_config.get_station_list_path())
except Exception as e:
    err_msgs += ["Error loading station list: " + repr(e)]

# TODO: add a config that allows specifying non-default port (and host?) - pass them to this constructor:
# initialise audio player
try:
    audio_player = audio_mpd.AudioPlayer ()
except Exception as e:
    err_msgs += ["Error initialising audio player: " + repr(e)]

#######################################################################################################################
# base page for the applications
#######################################################################################################################
# The base page - client side code loads the individual components
@app.route('/')
def base_page() -> str:
    return render_template('base.html')

#######################################################################################################################
# component parts of the base page
#######################################################################################################################
# The error messages component - only display if there are error messages
@app.route('/component/error_messages')
def show_err_msgs() -> str:
    if len(err_msgs) <= 0:
        return ""
    return render_template('error_messages.html', msgs=err_msgs)

# The info display component
@app.route('/component/info_messages/<string:visible>')
def show_info_msgs(visible: str) -> str:
    if visible.upper() == "TRUE":
        return render_template('info_messages.html', msgs=info_msgs)
    return ""

# The programme selector component - selections in this component control the station list component
@app.route('/component/radio_selector/<string:zone>')
def radio_selector(zone: str) -> str:
    if stations is None or zone.upper() == "NONE":
        sta_list = list ()
    else:
        sta_list = stations.get_station_list_from_zone(zone)
    return render_template('radio_selector.html', stations=sta_list)

# The station list component for live stations
@app.route("/component/live_station_list/<string:zone>")
def live_station_list(zone: str) -> str:
    if stations is None:
        sta_list = list ()
    else:
        sta_list = stations.get_station_list_from_zone(zone)
    return render_template('live_station_list.html', stations=sta_list)

# A blank component
@app.route("/component/blank")
def blank_component () -> str:
    return ""

# The schedule for on-demand programs
@app.route("/component/on_demand_schedule")
def on_demand_schedule() -> str:
    return render_template('schedule_viewer.html')

# The play bar component
@app.route('/component/play_bar')
def play_bar() -> str:
    return "Play bar holding page"

#######################################################################################################################
# methods in the application made available to the client
#######################################################################################################################
# a URL to power off
@app.route("/play/stop")
def play_stop() -> str:
    if audio_player is not None:
        audio_player.stop_mpd()
    return ""

# a URL to play live stations
@app.route("/play/live/<path:url>")
def play_live(url: str) -> str:
    if audio_player is not None:
        audio_player.live_stream_mpd(url)
    return ""

