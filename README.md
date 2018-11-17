PI Radio Player
===============

A projecct to play BCC live stations and on-demand programmes via MPC/MPD on the Raspberry PI. 

Setting up a development environment
------------------------------------

### Dependencies (ToDo: these should be put in a Requriements document) ###
- psutil
- flask
- python-mpd2

### Non-Python dependencies ###

- mpc/mpd
  - On Rapspbery PI:
    - sudo apt-get install mpd mpc
  - On Windows:
    - https://chriswarrick.com/blog/2013/09/01/mpd-on-windows/
    - Only mpd is needed, not mpc

- Debugging in PyCharm required a particular configuration. See PyCharm integration at the end of this article: http://flask.pocoo.org/docs/1.0/cli/

### Set up a python environment ###

To create the environment:

```conda create -n radio_player```

or 

```cd <proj-folder>; virtualenv radio_player```

To activate the envirionment:

```activate radio_player```

### Programming reminders ###

Running a test manually:
```python -m unittest audio_player/tests/test_audio_mpd.py```

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

Running on Raspberry PI (temporary method)
------------------------------------------

### One time setup ###

On Raspberry PI create a project folder, set up a Python virtual environment and clone the PiRadioPlayer repository:

```
cd <project-folder>
virtualenv radio_player_env psutil flask python-mpd2
source radio_player_env/bin/activate
git clone https://github.com/SimonFlower/PiRadioPlayer
```

To run the radio player:

```
cd <project-folder>
source radio_player_env/bin/activate
cd PiRadioPlayer
export FLASK_APP=main.py
flask run --host=0.0.0.0
```



