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
os.environ['MISTY'] = '/home/slimuser/Desktop/HRI/misty project/misty'

sys.path.append(os.environ['RETICO'])
sys.path.append(os.environ['RETICOV'])
sys.path.append(os.environ['RASA'])
sys.path.append(os.environ['MISTY'])

from misty.retico_mistyrobot.mistyPy.Robot import Robot
from retico_mistyrobot.misty_camera import MistyCameraModule
from retico_core.audio import MicrophoneModule

import random
import string
import threading
from collections import deque
import retico_core
from retico_core import abstract
from retico_opendialdm.dm import DialogueDecisionIU
from retico_core.dialogue import GenericDictIU


# from retico_core.abstract import AbstractModule
from retico_core.text import SpeechRecognitionIU, TextIU
from retico_rasanlu.rasanlu import RasaNLUModule
from retico_core.dialogue import DialogueActIU


class MistyActionModule(abstract.AbstractModule):

    @staticmethod
    def name():
        return "Misty Action Module"

    @staticmethod
    def description():
        return "A Module that maps from DM decisions to Misty Robot actions"

    @staticmethod
    def input_ius():
        return [DialogueDecisionIU]

    @staticmethod
    def output_iu():
        return GenericDictIU # this is an output module so it doesn't produce any IUs

    def __init__(self, ip, mic, **kwargs):
        super().__init__(**kwargs)
        self.misty = Robot(ip)
        self.queue = deque()
        self.mic = mic


    def misty_speak(self, message):
            self.mic.stop_stream()

            print("Misty starts speaking...")
            self.misty.speak(message) 
            time.sleep(20)  
            self.misty_speaking = False
            print("Misty finished speaking.")

            self.mic.start_stream()

    def process_update(self, update_message):
            for iu,um in update_message:
                if um == abstract.UpdateType.ADD:
                    self.process_iu(iu)
                elif um == abstract.UpdateType.REVOKE:
                    self.process_revoke(iu)

    # def get_command(self):

    #     while True:
    #         if len(self.queue) == 0:
    #             time.sleep(0.1)
    #             continue  

    #         input_iu = self.queue.popleft()

    #         print(f"action module: {input_iu.payload}")
        
    #         decision = input_iu.payload['decision']
    #         print(f"decision: {decision}")

    def process_iu(self, input_iu):
        iu = input_iu.payload['decision']
        print(f"action iu: {iu}")
        self.misty_speak(iu)

        
        