# mycroft-clementine-player-plasma-skill

This skill integrates [Clementine Music Player](https://www.clementine-player.org/) with [Mycroft](https://mycroft.ai/) which enables users to Play Local Music.

#### Installation of skill:

* Download or Clone Git
* Rename the folder to "mycroft-clementine-player-plasma-skill"
* Move it to /opt/mycroft/skills folder

#### Installation of requirements:
##### Linux: 
* inside the mycroft-core directory find .venv folder
* enable venv (source .venv/bin/activate)
* install Dbus: `pip install dbus-python`
* install Psutil: `pip install psutil`

##### How To Use: 
###### Play Music/Song
- "Hey Mycroft, play music"
- "Hey Mycroft, play song"

###### Pause Music/Song
- "Hey Mycroft, pause music"
- "Hey Mycroft, pause song"

###### Stop Music/Song
- "Hey Mycroft, stop music"
- "Hey Mycroft, stop song"

###### Next Song
- "Hey Mycroft, next song"

###### Previous Song
- "Hey Mycroft, previous song"

###### Jump forward
- "Hey Mycroft, jump 3 songs forward"
- "Hey Mycroft, go 8 forward"

###### Jump backward
- "Hey Mycroft, jump 10 songs back"
- "Hey Mycroft, go 4 backward"
- "Hey Mycroft, go 22 back"

## Current state

Working features:
* Play Music
* Pause Music
* Stop Music
* Next Song
* Previous Song
