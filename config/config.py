import os
import errno
import shutil
import pathlib

# constant names of things we need to access
STATION_LIST_FILENAME = "station_list.json"
RADIO_PLAYER_LOCAL_FOLDER = ".radio_player"


class ConfigLocationFinder:
    """
    Find where the configuration for the program is/can be stored.
    There are two modes in which the program configuration can work:
    - Global mode - config in system default places
    - Local mode - all config stored under users home folder
    This module uses global mode if it's accessible, local mode otherwise.
    Global mode is never available on Windows
    """
    def __init__(self):
        # try to use the global locations
        try:
            self.init_global()
        except Exception:
            # use local locations
            self.init_local()

    def init_global(self) -> None:
        # config comes from /etc/radio_player
        config_folder = "/etc/radio_player"
        if not os.access(config_folder, os.R_OK):
            os.mkdir(config_folder, 755)

        # copy default station list configuration
        station_list_path = os.path.join(config_folder, STATION_LIST_FILENAME)
        if not os.access(station_list_path, os.R_OK):
            src_filename = os.path.join(os.path.dirname(__file__), "..", "initial_data", "station_list.json")
            shutil.copy2(src_filename, station_list_path)

        # pid files are stored in /var/run
        pid_folder = "/var/run"
        if not os.access(pid_folder, os.W_OK):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), pid_folder)

        # log files go to /var/log
        log_folder = "/var/log"
        if not os.access(log_folder, os.W_OK):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), log_folder)

        # record where things are kept
        self.station_list_path = station_list_path
        self.pid_folder = pid_folder
        self.log_folder = log_folder

    def init_local(self) -> None:
        # everything is stored at ~/.radio_player
        home = pathlib.Path.home()
        folder = os.path.join(home, RADIO_PLAYER_LOCAL_FOLDER)
        if not os.access(folder, os.R_OK):
            os.mkdir(folder, 755)

        # copy default station list configuration
        station_list_path = os.path.join(folder, STATION_LIST_FILENAME)
        if not os.access(station_list_path, os.R_OK):
            src_filename = os.path.join(os.path.dirname(__file__), "..", "initial_data", "station_list.json")
            shutil.copy2(src_filename, station_list_path)

        # record where things are kept
        self.station_list_path = station_list_path
        self.pid_folder = folder
        self.log_folder = folder

    def get_station_list_path(self) -> str:
        return self.station_list_path

    def get_pid_folder(self) -> str:
        return self.pid_folder

    def get_log_folder(self) -> str:
        return self.log_folder
