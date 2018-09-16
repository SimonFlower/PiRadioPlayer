from mpd import MPDClient

class AudioPlayer:
    """
    A class that uses the python-mpd2 library to play a radio station. Documentation here:
    https://python-mpd2.readthedocs.io/en/latest/topics/commands.html
    """

    def __init__(self, hostname: str = "localhost", port: int = 6600):
        """
        :param hostname: IP name / address of mpd service
        :param port: port for mpd service
        """
        self.err = None
        self.client = MPDClient()

        try:
            # open the connnection to mpd
            self.client.timeout = 10
            self.client.idletimeout = None
            self.client.connect(hostname, port)

            # clear the current playlist
            self.client.clear()
        except Exception as e:
            self.err = "Error initialising audio player: " + str(e)

    def __del__(self):
        # close the connection to mpd
        try:
            self.client.close()
            self.client.disconnect()
        except Exception:
            pass

    def live_stream_mpd(self, url: str) -> str:
        msg = self.stop_mpd();
        if not msg is None:
            try:
                self.client.add(url)
                self.client.play(0)
            except Exception as e:
                msg = "Error communicating with audio player:" + str(e)

    def stop_mpd(self) -> str:
        try:
            self.client.clear()
            self.client.stop()
        except Exception as e:
            return "Error communicating with audio player:" + str(e)
        return None

    def set_volume(self, volume: int) -> str:
        """
        Set the volume
        :param volume: 0 to 100
        """
        try:
            self.client.setvol(volume)
        except Exception as e:
            return "Error communicating with audio player:" + str(e)
        return None

