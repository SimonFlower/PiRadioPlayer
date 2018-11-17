import json

from flask import Flask
from flask import render_template
from flask import request

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

#######################################################################################################################
# Base page for the applications - this is a single page application with sections:
# - An error message component - only displayed if there are errors initialising the app
# - Standby / Region / On-demand station selection pane
# - Live radio selection / On demand schedule selection
# - Play bar - with 'now playing' information
# The final two component parts of the page can be loaded separately into the base page
#######################################################################################################################
# The base page
@app.route('/')
def base_page() -> str:
    return render_template('base.html',
                           error_messages = err_msgs,
                           info_msgs = info_msgs)

#######################################################################################################################
# component parts of the base page
#######################################################################################################################
# The station/schedule component
@app.route("/component/station_schedule")
def station_schedule() -> str:
    operation = request.args.get ('operation')
    if operation is None:
        operation = ""
    if operation == 'live':
        zone = request.args.get ('zone')
        return render_template('live_station_list.html', stations=stations.get_station_list(zone))
    if operation == 'on_demand':
        return render_template('schedule_viewer.html')
    if operation == 'blank':
        return ""
    return "/component/schedule: Unrecognised operation [" + operation + "]"

# The play bar component
@app.route('/component/play_bar')
def play_bar() -> str:
    operation = request.args.get ('operation')
    if operation is None:
        operation = ""
    if operation == 'stop':
        audio_player.stop()
        return ""
    if operation == 'live_station':
        station_id = request.args.get ('station_id')
        station = stations.find_station(station_id)
        if station is None:
            return "/component/play_bar: Missing or invalid 'station_id' parameter"
        errmsg = audio_player.play(station['streaming_url'])
        if len(errmsg) > 0:
            return "Error with audio: " + errmsg
        return render_template('playbar_live.html', station=station, volume=audio_player.volume)

    return "/component/play_bar: Unrecognised operation [" + operation + "]"

#######################################################################################################################
# audio operations
#######################################################################################################################
@app.route("/audio")
def audio () -> str:
    errmsg = ""

    # process volume change request
    param = request.args.get ('volume')
    if param is not None:
        try:
            volume = int (float (param))
            if volume < 0 or volume > 100:
                raise ValueError
        except ValueError:
            return "/audio: bad volume value: [" + param + "]"
        errmsg += audio_player.set_volume(volume)

    # process pause request
    param = request.args.get ('pause')
    if param is not None:
        try:
            pause = int (float (param))
            if pause < 0 or pause > 1:
                raise ValueError
        except ValueError:
            return "/audio: bad pause value: [" + param + "]"
        errmsg += audio_player.pause(pause)

    return errmsg

#######################################################################################################################
# odds and ends
#######################################################################################################################

# we need to process the javascript for the project using a template, so that data can
# be passed from server to client
@app.route("/scripts/radio_player.js")
def process_script () -> str:
    return render_template('radio_player.js',
                           national_stations = stations.get_station_list(station_list_reader.ZONE_NATIONAL),
                           regional_stations = stations.get_station_list(station_list_reader.ZONE_REGIONAL),
                           local_stations = stations.get_station_list(station_list_reader.ZONE_LOCAL))

