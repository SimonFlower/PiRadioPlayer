Reminders
---------

Using virtualenv
- c:
- cd \users\smf\radio_player
- virtualenv radio_player

Running a test manually
- python -m unittest audio_player/tests/test_audio_mpd.py

Dependencies
------------

Dependencies (not added the Requriements document):
- psutil
- flask
- python-mpd2

Non-Python dependencies:

- get_iplayer
  get_iplayer players (not sure which are used)
- mpc/mpd
  On Rapspbery PI:
    sudo apt-get install mpd mpc
  On Windows:
    https://chriswarrick.com/blog/2013/09/01/mpd-on-windows/
    Only mpd is needed, not mpc
