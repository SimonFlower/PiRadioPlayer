from mpd import MPDClient

class AudioPlayer:
    """
    A class that uses the python-mpd2 library to play a radio station. Documentation here:
    https://python-mpd2.readthedocs.io/en/latest/topics/commands.html
    """

    def __init__(self, hostname: str = "localhost", port: int = 6600):
        """
        Raises an mpd.base.ConnecctionError if mpd can't be found
        :param hostname: IP name / address of mpd service
        :param port: port for mpd service
        """
        # open the connnection to mpd
        self.client = MPDClient()
        self.client.timeout = 10
        self.client.idletimeout = None
        self.client.connect(hostname, port)

        # clear the current playlist
        self.client.clear()

    def __del__(self):
        # close the connection to mpd
        self.client.close()
        self.client.disconnect()

    def live_stream_mpd(self, url: str) -> None:
        self.stop_mpd()
        self.client.add(url)
        self.client.play(0)

    def stop_mpd(self) -> None:
        self.client.clear()
        self.client.stop()

    def set_volume(self, volume: int) -> None:
        """
        Set the volume
        :param volume: 0 to 100
        """
        self.client.setvol(volume)

