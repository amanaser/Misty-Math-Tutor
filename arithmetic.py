import os, sys
import requests
import time
from PIL import Image
import io
import requests
from io import BytesIO
import json

os.environ['RETICO'] = '/home/slimuser/Desktop/HRI/misty project/retico-core'
os.environ['RETICOV'] = '/home/slimuser/Desktop/HRI/misty project/retico-vision'
os.environ['RASA'] = '/home/slimuser/Desktop/HRI/misty project/retico-rasanlu'
os.environ['MISTY'] = '/home/slimuser/Desktop/HRI/misty project/misty'

sys.path.append(os.environ['RETICO'])
sys.path.append(os.environ['RETICOV'])
sys.path.append(os.environ['RASA'])
sys.path.append(os.environ['MISTY'])

from misty.retico_mistyrobot.mistyPy.Robot import Robot
from retico_mistyrobot.misty_camera import MistyCameraModule

import random
import string
import retico_core
from retico_core import abstract
# from retico_core.abstract import AbstractModule
from retico_core.text import SpeechRecognitionIU, TextIU
from retico_rasanlu.rasanlu import RasaNLUModule
from retico_core.dialogue import DialogueActIU


class ArithmeticModule(abstract.AbstractModule):
    def __init__(self, misty_ip):
        super().__init__()
        self.misty = misty_ip

    @staticmethod
    def name():
        return "Number Check Module"

    @staticmethod
    def description():
        return "A module teaching arithmetic."

    @staticmethod
    def input_ius():
        return DialogueActIU

    @staticmethod
    def output_iu():
        return TextIU
    
    def __init__(self, ip, **kwargs):
        super().__init__(**kwargs)

        self.misty = ip


    def process_update(self, update_message):
        for iu,um in update_message:
            print(f"iu: {iu.payload}")
            if um == abstract.UpdateType.ADD:
                self.process_iu(iu)
            elif um == abstract.UpdateType.REVOKE:
                self.process_revoke(iu)

    def process_iu(self, input_iu):
        pass

    def process_revoke(self, input_iu):
        pass
