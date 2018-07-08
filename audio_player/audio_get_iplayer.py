import subprocess
import os
import errno
import psutil

RADIO_PLAYER_PID_FILENAME = "radio_player.pid"
GET_IPLAYER_CMD = "get_iplayer"


class AudioPlayer:
    """
    A class that calls the operating system to play a radio station. When I started this it appeared that
    get_iplayer would do a good job, but later versions of get_iplayer have removed the streaming functions.
    This class is probably redundant now.
    """

    def __init__(self, pid_folder: str):
        self.pid_folder = pid_folder
        self.pid_filename = os.path.join(self.pid_folder, RADIO_PLAYER_PID_FILENAME)

        # find path strings for find_in_path()
        env = os.environ.get('PATH')
        if env is None:
            self.path_list = ['.']
        else:
            self.path_list = env.split(os.pathsep) + ['.']
        env = os.environ.get('PATHEXT')
        if env is None:
            self.suffix_list = ['']
        else:
            self.suffix_list = env.split(os.pathsep)

        # find absolute path to get_iplayer
        self.get_iplayer_path = self.find_in_path(GET_IPLAYER_CMD)

        # find get_iplayer version
        args = [self.get_iplayer_path, '--helpbasic']
        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        for line in process.stdout:
            words = line.split()
            if len(words) >= 3:
                if words[0] == b'get_iplayer' and len(words[1]) > 1 and words[2] == b'Copyright':
                    self.get_iplayer_version = words[1][0:len(words[1])-1].decode()
        if self.get_iplayer_version is None:
            raise RuntimeError("Unable to find version of " + GET_IPLAYER_CMD)

    def live_stream_get_iplayer(self, station_name: str) -> None:
        # stop any running get_iplayer
        self.stop_get_iplayer()

        # build the command - it's different for versions 2 and 3 of get_iplayer
        # *** actually it's not possible in version 3 ***
        if self.get_iplayer_version.startswith('2'):
            args = [self.get_iplayer_path, '--stream', '--type=liveradio',
                    station_name, '--player="mplayer -cache 128 -"']
        else:
            args = [self.get_iplayer_path, '--stream', '--type=liveradio',
                    station_name, '--player="mplayer -cache 128 -"']

        # run the command
        process = subprocess.Popen(args)

        # record the pid
        pid = process.pid
        if not process.poll():
            self.record_pid(pid)

    def is_get_iplayer_running(self) -> bool:
        try:
            with open(self.pid_filename) as data_file:
                pid = int(data_file.read())
            return psutil.pid_exists(pid)
        except FileNotFoundError:
            return False

    def stop_get_iplayer(self) -> None:
        try:
            with open(self.pid_filename) as data_file:
                pid = int(data_file.read())
            process = psutil.Process(pid)
            process.kill()
        except FileNotFoundError:
            pass

    def record_pid(self, pid) -> None:
        if pid is None:
            os.remove(self.pid_filename)
        else:
            with open(self.pid_filename, mode="w") as data_file:
                data_file.write(str(pid))

    def find_in_path(self, exe: str) -> str:
        """
        Find an executable using the PATH environment variable. This is needed because:
        https://bugs.python.org/issue8557
        :param exe: the executable to search for (without any '.exe' suffix)
        :return: the absolute path to the executable or None
        """
        for path in self.path_list:
            for suffix in self.suffix_list:
                filename = os.path.join(path, exe) + suffix
                if os.access(filename, os.X_OK):
                    return filename
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), exe)
