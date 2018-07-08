import unittest
import tempfile
from .. import audio_get_iplayer
import time


class TestAudioPlayer (unittest.TestCase):

    def test_live_stream_get_iplayer(self) -> None:
        with tempfile.TemporaryDirectory(suffix='test_audio_player') as tmpdirname:
            self.audio_player = audio_get_iplayer.AudioPlayer(tmpdirname)
            self.audio_player.live_stream_get_iplayer ('BBC Radio 4 (incl. FM, LW)')
            time.sleep (5)
            self.assertTrue (self.audio_player.is_get_iplayer_running())
            self.audio_player.stop_get_iplayer()
            self.assertFalse(self.audio_player.is_get_iplayer_running())

