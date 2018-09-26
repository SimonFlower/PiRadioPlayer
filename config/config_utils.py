import os
import errno
import shutil
import pathlib
import json
import tempfile

# constant names of things we need to access
GENERAL_CONFIG_FILENAME = "radio_player_config.json"
STATION_LIST_FILENAME = "station_list.json"
RADIO_PLAYER_LOCAL_FOLDER = ".radio_player"


class ConfigLocationFinder:
    """
    Find where the configuration for the program is/can be stored.
    There are two modes in which the program configuration can work:
    - Global mode - config in system default places
    - Local mode - all config stored under users home folder
    This module uses global mode if it's accessible, local mode otherwise.
    Global mode is never available on Windows.

    If self.err is set there was an initialisation error
    """

    def __init__(self, force_fail:bool = False):
        """
        Initialise the class
        :param force_fail: a testing parameter - set true to force a failure
        """
        # try to use the global locations for configuration files
        self.err = None
        try:
            if force_fail:
                raise RuntimeError ("Forcing failure")
            # config comes from /etc/radio_player
            self.__init2__("/etc/radio_player", "/var/run", "/var/log")
        except Exception:
            try:
                if force_fail:
                    raise RuntimeError("Forcing failure")
                # use local locations for configuration files
                home = pathlib.Path.home()
                folder = os.path.join(str(home), RADIO_PLAYER_LOCAL_FOLDER)
                if not os.access(folder, os.R_OK):
                    os.mkdir(folder, 0o755)
                self.__init2__(folder)
            except Exception as e:
                # record the error
                self.err = str(e)

                # set defaults so that this class will still return a value even if there is an error
                self.general_config_path = tempfile.gettempdir()
                self.station_list_path = tempfile.gettempdir()
                self.pid_folder = tempfile.gettempdir()
                self.log_folder = tempfile.gettempdir()
                self.config = dict ()

        # check mpd connecctions details
        if not 'mpd_host' in self.config:
            self.config['mpd_host'] = "localhost"
        if not 'mpd_host' in self.config:
            self.config['mpd_port'] = 6600

    def __init2__(self, config_folder: str, pid_folder: str = None, log_folder: str = None) -> None:
        if not os.access(config_folder, os.R_OK):
            os.mkdir(config_folder, 0o755)

        # copy default general and station list configuration
        self.general_config_path = os.path.join(config_folder, GENERAL_CONFIG_FILENAME)
        self.station_list_path = os.path.join(config_folder, STATION_LIST_FILENAME)
        if not os.access(self.general_config_path, os.R_OK):
            src_filename = os.path.join(os.path.dirname(__file__), "..", "initial_data", "radio_player_config.json")
            shutil.copy2(src_filename, self.general_config_path)
        if not os.access(self.station_list_path, os.R_OK):
            src_filename = os.path.join(os.path.dirname(__file__), "..", "initial_data", "station_list.json")
            shutil.copy2(src_filename, self.station_list_path)

        # check pid files storage
        if pid_folder is None:
            pid_folder = config_folder
        elif not os.access(pid_folder, os.W_OK):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), pid_folder)

        # check log files storage
        if log_folder is None:
            log_folder = config_folder
        elif not os.access(log_folder, os.W_OK):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), log_folder)

        # record where things are kept
        self.pid_folder = pid_folder
        self.log_folder = log_folder

        # load general config
        with open(self.general_config_path) as data_file:
            config = json.load(data_file)
        self.config = config['config']

        # check for required values
        if not self.config['mpd_host']:
            self.config['mpd_host'] = 'localhost'
        if not self.config['mpd_port']:
            self.config['mpd_port'] = 6600
