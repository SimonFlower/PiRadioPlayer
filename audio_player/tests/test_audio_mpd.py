import unittest
from .. import audio_mpd
import time


class TestAudioPlayer (unittest.TestCase):

    def test_live_stream_mpd(self) -> None:
        self.audio_player = audio_mpd.AudioPlayer("localhost", 6600)
        self.audio_player.live_stream_mpd ('http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio3_mf_p')
        time.sleep (5)
        self.audio_player.stop_mpd()

