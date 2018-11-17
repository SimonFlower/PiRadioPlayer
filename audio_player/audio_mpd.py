from mpd import MPDClient

class AudioPlayer:
    """
    A class that uses the python-mpd2 library to play a radio station. Documentation here:
    https://python-mpd2.readthedocs.io/en/latest/topics/commands.html.
    Note that the volume control runs from 0 to 100.
    """

    def __init__(self, hostname: str = "localhost", port: int = 6600):
        """
        :param hostname: IP name / address of mpd service
        :param port: port for mpd service
        """
        self.volume = 100
        self.is_connected = False
        self.hostname = hostname
        self.port = port
        self.client = MPDClient()
        self.client.timeout = 10
        self.client.idletimeout = None
        self.__make_connection__()

    def __del__(self):
        # close the connection to mpd
        self.is_connected = False
        try:
            self.client.close()
            self.client.disconnect()
        except Exception:
            pass

    def play(self, url: str) -> str:
        msg = ""
        if not self.is_connected:
            msg = self.__make_connection__()
        if len(msg) <= 0:
            msg = self.stop();
        if len(msg) <= 0:
            try:
                self.client.add(url)
                self.client.play(0)
            except Exception as e:
                msg = "Error communicating with audio player:" + str(e)
        return msg

    def stop(self) -> str:
        msg = ""
        if not self.is_connected:
            msg = self.__make_connection__()
        if len(msg) <= 0:
            try:
                self.client.clear()
                self.client.stop()
            except Exception as e:
                msg = "Error communicating with audio player:" + str(e)
        return msg

    def pause(self, pause : int) -> str:
        msg = ""
        if not self.is_connected:
            msg = self.__make_connection__()
        if len(msg) <= 0:
            try:
                self.client.pause(pause)
            except Exception as e:
                msg = "Error communicating with audio player:" + str(e)
        return msg

    def set_volume(self, volume: int) -> str:
        """
        Set the volume
        :param volume: 0 to 100
        """
        msg = ""
        if not self.is_connected:
            msg = self.__make_connection__()
        if len(msg) <= 0:
            try:
                self.client.setvol(volume)
                self.volume = volume
            except Exception as e:
                msg = "Error communicating with audio player:" + str(e)
        return msg

    def __make_connection__ (self) -> str:
        self.is_connected = False
        try:
            # open the connnection to mpd
            self.client.connect(self.hostname, self.port)

            # clear the current playlist
            self.client.clear()
            self.is_connected = True

            # set initial volume
            self.set_volume(self.volume)
        except Exception as e:
            return "Error initialising audio player: " + str(e)
        return ""
