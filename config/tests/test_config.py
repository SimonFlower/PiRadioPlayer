import unittest
import platform
from .. import config
import os


class TestConfig (unittest.TestCase):

    def setUp(self):
        if platform.system() == 'Windows':
            self.is_windows = True
        else:
            self.is_windows = False
        self.clf = config.ConfigLocationFinder()
        self.home = os.path.expanduser("~")

    def test_get_station_list_path(self):
        local_path = os.path.join(self.home, config.RADIO_PLAYER_LOCAL_FOLDER, config.STATION_LIST_FILENAME)
        if self.is_windows:
            global_path = None
        else:
            global_path = os.path.join("etc", "radio_player", config.STATION_LIST_FILENAME)
        file_path = self.clf.get_station_list_path()
        self.assertTrue(file_path == local_path or file_path == global_path)

    def test_get_pid_folder(self):
        local_path = os.path.join(self.home, config.RADIO_PLAYER_LOCAL_FOLDER)
        if self.is_windows:
            global_path = None
        else:
            global_path = os.path.join("var", "run")
        file_path = self.clf.get_pid_folder()
        self.assertTrue(file_path == local_path or file_path == global_path)

    def test_get_log_folder(self):
        local_path = os.path.join(self.home, config.RADIO_PLAYER_LOCAL_FOLDER)
        if self.is_windows:
            global_path = None
        else:
            global_path = os.path.join("var", "log")
        file_path = self.clf.get_log_folder()
        self.assertTrue(file_path == local_path or file_path == global_path)
