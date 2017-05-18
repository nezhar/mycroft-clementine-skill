import sys
import dbus
import glib
import os
import psutil
from traceback import print_exc
from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
import subprocess

__author__ = 'aix'

LOGGER = getLogger(__name__)

class ClementineMusicPlayerSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(ClementineMusicPlayerSkill, self).__init__(name="ClementineMusicPlayerSkill")
        
    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        self.load_data_files(dirname(__file__))

        internals_clementine_play_skill_intent = IntentBuilder("ClementinePlayKeywordIntent").\
            require("ClementinePlayKeyword").build()
        self.register_intent(internals_clementine_play_skill_intent, self.handle_internals_clementine_play_skill_intent)

        internals_clementine_jump_forward_skill_intent = IntentBuilder("ClementineJumpForwardKeywordIntent").\
            require("ClementineJumpKeyword").require("nrOfSongs").require("ClementineJumpForwardKeyword").build()
        self.register_intent(internals_clementine_jump_forward_skill_intent, self.handle_internals_clementine_jumpForward_skill_intent)

        internals_clementine_jump_backward_skill_intent = IntentBuilder("ClementineJumpBackwardKeywordIntent").\
            require("ClementineJumpKeyword").require("nrOfSongs").require("ClementineJumpBackwardKeyword").build()
        self.register_intent(internals_clementine_jump_backward_skill_intent, self.handle_internals_clementine_jumpBackward_skill_intent)
                
        internals_clementine_stop_skill_intent = IntentBuilder("ClementineStopKeywordIntent").\
            require("ClementineStopKeyword").build()
        self.register_intent(internals_clementine_stop_skill_intent, self.handle_internals_clementine_stop_skill_intent)
        
        internals_clementine_next_skill_intent = IntentBuilder("ClementineNextKeywordIntent").\
            require("ClementineNextKeyword").build()
        self.register_intent(internals_clementine_next_skill_intent, self.handle_internals_clementine_next_skill_intent)

        internals_clementine_previous_skill_intent = IntentBuilder("ClementinePreviousKeywordIntent").\
            require("ClementinePreviousKeyword").build()
        self.register_intent(internals_clementine_previous_skill_intent, self.handle_internals_clementine_previous_skill_intent)
        
        internals_clementine_pause_skill_intent = IntentBuilder("clementinePauseKeywordIntent").\
            require("clementinePauseKeyword").build()
        self.register_intent(internals_clementine_pause_skill_intent, self.handle_internals_clementine_pause_skill_intent)


    def handle_internals_clementine_play_skill_intent(self, message):    
	
        clementineRunning = False   

        for proc in psutil.process_iter():
            pinfo = proc.as_dict(attrs=['pid', 'name'])    
            if pinfo['name'] == 'clementine':
                clementineRunning = True
    
        if clementineRunning:
            self.speak_dialog("clementine.play")
            #print('yes')

	    def runplay():
       		 bus = dbus.SessionBus()
        	 remote_object = bus.get_object("org.mpris.MediaPlayer2.clementine","/org/mpris/MediaPlayer2")
        	 remote_object.Play(dbus_interface = "org.mpris.MediaPlayer2.Player")	
	    runplay()
        
	else:
       	   def runprocandplay():
           	#cmdstring = "clementine %s %s %s" % ('-p' '-k' '0')
           	#os.system(cmdstring)
           	subprocess.call(['clementine', '-p', '-k', '0'])
           	bus = dbus.SessionBus()
           	remote_object = bus.get_object("org.mpris.MediaPlayer2.clementine","/org/mpris/MediaPlayer2")
           	remote_object.Play(dbus_interface = "org.mpris.MediaPlayer2.Player")
           runprocandplay()
   
    def handle_internals_clementine_stop_skill_intent(self, message):        
        bus = dbus.SessionBus()
        remote_object = bus.get_object("org.mpris.MediaPlayer2.clementine","/org/mpris/MediaPlayer2") 
        remote_object.Stop(dbus_interface = "org.mpris.MediaPlayer2.Player")
        
        self.speak_dialog("clementine.stop")
    
    def handle_internals_clementine_next_skill_intent(self, message):
        bus = dbus.SessionBus()
        remote_object = bus.get_object("org.mpris.MediaPlayer2.clementine","/org/mpris/MediaPlayer2") 
        remote_object.Next(dbus_interface = "org.mpris.MediaPlayer2.Player")
        
        self.speak_dialog("clementine.next")
        
    def handle_internals_clementine_jumpForward_skill_intent(self, message):
        bus = dbus.SessionBus()
        remote_object = bus.get_object("org.mpris.MediaPlayer2.clementine","/org/mpris/MediaPlayer2")
        properties_manager = dbus.Interface(remote_object, 'org.freedesktop.DBus.Properties')
        nrOfSongs = message.data.get("nrOfSongs")
        try:
            parsedNrOfSongs = int(nrOfSongs)
            i = 0;
            while(parsedNrOfSongs>i):
                if(properties_manager.Get('org.mpris.MediaPlayer2.Player', 'CanGoPrevious')):
                    remote_object.Next(dbus_interface = "org.mpris.MediaPlayer2.Player")
                    i+=1
            self.speak("Jumped "+nrOfSongs+" songs forward")
        except ValueError:
            self.speak("sorry, was not able to parse the amount of songs i should go forward. Your wrong nr was: "+nrOfSongs)
    
    def handle_internals_clementine_jumpBackward_skill_intent(self, message):
        bus = dbus.SessionBus()
        remote_object = bus.get_object("org.mpris.MediaPlayer2.clementine","/org/mpris/MediaPlayer2")
        properties_manager = dbus.Interface(remote_object, 'org.freedesktop.DBus.Properties')
        nrOfSongs = message.data.get("nrOfSongs")
        try:
            parsedNrOfSongs = int(nrOfSongs)
            i = 0;
            while(parsedNrOfSongs>i):
                if(properties_manager.Get('org.mpris.MediaPlayer2.Player', 'CanGoPrevious')):
                    remote_object.Previous(dbus_interface = "org.mpris.MediaPlayer2.Player")
                    i+=1
            self.speak("Jumped "+nrOfSongs+" songs backward")
        except ValueError:
            self.speak("sorry, was not able to parse the amount of songs i should go backward. Your wrong nr was: "+nrOfSongs)

        
    def handle_internals_clementine_previous_skill_intent(self, message):
        
        bus = dbus.SessionBus()
        remote_object = bus.get_object("org.mpris.MediaPlayer2.clementine","/org/mpris/MediaPlayer2") 
        remote_object.Previous(dbus_interface = "org.mpris.MediaPlayer2.Player")
        
        self.speak_dialog("clementine.previous")     

    def handle_internals_clementine_pause_skill_intent(self, message):
        
        bus = dbus.SessionBus()
        remote_object = bus.get_object("org.mpris.MediaPlayer2.clementine","/org/mpris/MediaPlayer2") 
        remote_object.Pause(dbus_interface = "org.mpris.MediaPlayer2.Player")
        
        self.speak_dialog("clementine.pause")     
        
    def stop(self):
        pass

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return ClementineMusicPlayerSkill()
