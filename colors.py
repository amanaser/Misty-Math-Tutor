import os, sys
import requests
from queue import Queue
import time
from PIL import Image
import io
import requests
from io import BytesIO
import json

os.environ['RETICO'] = '/home/slimuser/Desktop/HRI/misty project/retico-core'
os.environ['RETICOV'] = '/home/slimuser/Desktop/HRI/misty project/retico-vision'
os.environ['RASA'] = '/home/slimuser/Desktop/HRI/misty project/retico-rasanlu'
os.environ['WAC'] = '/home/slimuser/Desktop/HRI/misty project/retico-wacnlu'
os.environ['MISTY'] = '/home/slimuser/Desktop/HRI/misty project/misty'

sys.path.append(os.environ['RETICO'])
sys.path.append(os.environ['RETICOV'])
sys.path.append(os.environ['RASA'])
sys.path.append(os.environ['WAC'])
sys.path.append(os.environ['MISTY'])

from misty.retico_mistyrobot.mistyPy.Robot import Robot
from retico_mistyrobot.misty_camera import MistyCameraModule
from retico_core.audio import MicrophoneModule
from retico_vision.vision import ExtractedObjectsIU, ObjectFeaturesIU
from retico_wacnlu.words_as_classifiers import WordsAsClassifiersModule
from retico_wacnlu.common import GroundedFrameIU


import random
import string
import retico_core
from retico_core import abstract
# from retico_core.abstract import AbstractModule
from retico_core.text import SpeechRecognitionIU, TextIU
from retico_rasanlu.rasanlu import RasaNLUModule
from retico_core.dialogue import DialogueActIU
from retico_core.dialogue import GenericDictIU


class ColorModule(abstract.AbstractModule):
    @staticmethod
    def name():
        return "Color Teaching Module"

    @staticmethod
    def description():
        return "A module teaching colors."

    @staticmethod
    def input_ius():
        return GroundedFrameIU

    @staticmethod
    def output_iu():
        return GenericDictIU
    
    def __init__(self, ip, **kwargs):
        super().__init__(**kwargs)

        self.misty = Robot(ip)
        self.expected_answer = None
        self.awaiting_response = False
        self.speaking = False

    def misty_speak(self, message):

        print("Misty starts speaking...")
        self.misty.speak(message) 
        time.sleep(5) 
        self.misty_speaking = False
        print("Misty finished speaking.")



    def process_update(self, update_message):
        for iu,um in update_message:
            if um == abstract.UpdateType.ADD:
                self.process_iu(iu)
            elif um == abstract.UpdateType.REVOKE:
                self.process_revoke(iu)

    def process_iu(self, input_iu):
        
        obj_iu = None

        if isinstance(input_iu, GroundedFrameIU):
            obj_iu = input_iu.payload
            print(f"obj iu: {obj_iu}")

        color = obj_iu['best_known_word']

        self.misty_speak(color)

    def process_revoke(self, input_iu):
        pass

    def setup(self):
        self.misty_speak("Now I will teach you the colors.")
        self.misty_speak("Put the objects in front of me and I will tell you what color that is.")





