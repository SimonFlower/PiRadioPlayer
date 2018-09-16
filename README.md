Reminders
---------

Running on Raspberry PI (temporary method):
- cd <top-level-project-folder>
- flask run --host=0.0.0.0

Using virtualenv
- c:
- cd \users\smf\radio_player
- virtualenv radio_player

Running a test manually
- python -m unittest audio_player/tests/test_audio_mpd.py

Google Python Style Guide has the following convention for case of elements:
- module_name
- package_name
- ClassName
- method_name
- ExceptionName
- function_name
- GLOBAL_CONSTANT_NAME
- global_var_name
- instance_var_name
- function_parameter_name
- local_var_name

Dependencies
------------

Dependencies (not added the Requriements document):
- psutil
- flask
- python-mpd2

Non-Python dependencies:

- mpc/mpd
  - On Rapspbery PI:
    - sudo apt-get install mpd mpc
  - On Windows:
    - https://chriswarrick.com/blog/2013/09/01/mpd-on-windows/
    - Only mpd is needed, not mpc

- Debugging in PyCharm required a particular configuration. See PyCharm integration at the end of this article: http://flask.pocoo.org/docs/1.0/cli/
