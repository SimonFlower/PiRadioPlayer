from flask import Flask
from flask import render_template

from config import config_utils
from config import station_list_reader
from audio_player import audio_mpd

# TODO : Add logging and send stacktrace of any exceptions to the log, something like this:
#        traceback.print_exc()


# We want to keep as much state as possible on the client side, but a radio is a device that
# is either on or off and it can only play one station at a time, so some state has to live
# on the server. These variables hold the state:
#   now_playing may contain:
#     None = power off
#     An ID from the station list = the ID for the live stream that's playing
#     On-demand TBC
now_playing = None

# initialise Flask
app = Flask(__name__)

# top level application variables
err_msgs = list ()
info_msgs = dict ()
program_config = None
stations = None
audio_player = None

# initialise configuration
program_config = config_utils.ConfigLocationFinder()
info_msgs["Configuration file"] = program_config.general_config_path
info_msgs["Station list file"] =  program_config.station_list_path
info_msgs["Log folder"] =         program_config.log_folder
info_msgs["PID folder"] =         program_config.pid_folder
info_msgs["MPD player host"] =    program_config.config['mpd_host']
info_msgs["MPD player port"] =    program_config.config['mpd_port']
if program_config.err is not None:
    err_msgs += [program_config.err]

# load list of stations
stations = station_list_reader.StationListReader(program_config.station_list_path)
if len (stations.err) > 0:
    err_msgs += stations.err

# initialise audio player
audio_player = audio_mpd.AudioPlayer(program_config.config['mpd_host'],
                                     program_config.config['mpd_port'])
if audio_player.err is not None:
    err_msgs += [audio_player.err]

#######################################################################################################################
# base page for the applications - this is a single page application with compnent parts of the page that can be
# loaded separately:
# - An error message component - only displayed if there are errors initialising the app
# - Standby / Live radio / On demand selection pane
# - Live radio selection / On demand selection
# - Play bar - 'now playing' information
#######################################################################################################################
# The base page - client side code loads the individual components
@app.route('/')
def base_page() -> str:
    return render_template('base.html',
                           error_messages = err_msgs)

#######################################################################################################################
# component parts of the base page
#######################################################################################################################
# The programme selector component - selections in this component control the station list component
@app.route('/component/radio_selector')
def radio_selector() -> str:
    return render_template('radio_selector.html',
                           national_stations = stations.get_station_list("national"),
                           regional_stations = stations.get_station_list("regional"),
                           local_stations = stations.get_station_list("local"),
                           info_msgs=info_msgs)

# The station list component for live stations
@app.route("/component/live_station_list/<string:zone>")
def live_station_list(zone: str) -> str:
    if stations is None:
        sta_list = list ()
    else:
        sta_list = stations.get_station_list(zone)
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

