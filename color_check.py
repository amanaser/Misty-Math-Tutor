import os, sys
import requests
from queue import Queue
import time
from PIL import Image
import io
import requests
from io import BytesIO
import json
import string

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
from collections import deque
import retico_core
from retico_core import abstract
# from retico_core.abstract import AbstractModule
from retico_core.text import SpeechRecognitionIU, TextIU
from retico_rasanlu.rasanlu import RasaNLUModule
from retico_core.audio import MicrophoneModule
from retico_core.dialogue import DialogueActIU
from retico_core.dialogue import GenericDictIU


class ColorCheckModule(abstract.AbstractModule):
    @staticmethod
    def name():
        return "Color Checking Module"

    @staticmethod
    def description():
        return "A module checking if the user recognizes the colors correctly."

    @staticmethod
    def input_ius():
        return DialogueActIU, GroundedFrameIU

    @staticmethod
    def output_iu():
        return DialogueActIU
    
    def __init__(self, ip, mic, **kwargs):
        super().__init__(**kwargs)

        self.misty = Robot(ip)
        self.expected_answer = None
        self.speaking = False
        self.mic = mic
        self.queue = deque(maxlen=1)
        self.current_state = {"grounded_frame": None, "dialogue_act": None}


    def speak_and_wait(self, message, delay=3):
        self.mic.stop_stream()

        print("Misty starts speaking...")
        self.misty.speak(message) 
        time.sleep(10) 
        self.misty_speaking = False
        print("Misty finished speaking.")

        self.mic.start_stream()

    def process_update(self, update_message):
        # for iu,um in update_message:
        #     if um == abstract.UpdateType.ADD:
        #         self.process_iu(iu)
        #     elif um == abstract.UpdateType.REVOKE:
        #         self.process_revoke(iu)

        for iu, um in update_message:
            print(f"iu: {iu}")
            if um == abstract.UpdateType.ADD:
                if isinstance(iu, GroundedFrameIU):
                    self.current_state["grounded_frame"] = iu.payload['best_known_word']
                    print(f"self.current_state[grounded_frame]: {self.current_state['grounded_frame']}")
                elif isinstance(iu, DialogueActIU):
                    self.current_state["dialogue_act"] = iu.payload
                    print(f"self.current_state[dialogue_act]: {self.current_state['dialogue_act']}")

                if self.current_state["grounded_frame"] and self.current_state["dialogue_act"]:
                    self.check_answer(self.current_state, iu)

    # def process_iu(self, input_iu):
        
    #     obj_iu = None
    #     nlu_iu = None
    #     obj_processed = None

    #     frame = {}
    #     # print(f"input: {input_iu.payload}")

    #     if isinstance(input_iu, GroundedFrameIU):
    #         obj_iu = input_iu.payload['best_known_word']
    #         obj_processed = ''.join(char.lower() for char in obj_iu if char not in string.punctuation)
    #         frame['expected_answer'] = obj_processed
    #         print(f"obj processed: {obj_processed}")

    #     if isinstance(input_iu, DialogueActIU):
    #         nlu_iu = input_iu.payload

    #         if 'color' in nlu_iu:
    #             input = nlu_iu['color']
    #             input = [item.lower() for item in input]

    #             frame['user_input'] = input[-1]
    #             print(f"nlu: {nlu_iu}")


    #     if len(frame) == 0: return
    #     print(f"frame: {frame}")
    #     # if nlu_iu:
    #     #     print("in check answer")
    #     #     self.check_answer(obj_processed, nlu_iu, input_iu)

    #         # self.check_answer(self.expected_answer, self.explanation, nlu_iu, input_iu)


    def process_revoke(self, input_iu):
        pass

    def check_answer(self, current_state, input_iu):
        # print("check")
        # output = []
        # input = []

        # if 'color' in iu:
        #     input = iu['color']
        #     input = [item.lower() for item in input]

        #     output = {'expected_answer':answer, 'user_input': input[-1]}
        #     print(f"input: {input}")
        #     print(f"output: {output}")

        #     output_iu = self.create_iu(input_iu)
        #     output_iu.payload = output
        #     output_iu = retico_core.UpdateMessage.from_iu(output_iu, retico_core.UpdateType.ADD)

        #     self.append(output_iu)

        expected_answer = current_state['grounded_frame']
        dialogue_act = current_state['dialogue_act']

        expected_answer = expected_answer.translate(str.maketrans('', '', string.punctuation))


        print(f"expected_answer: {expected_answer}")
        print(f"dialogue_act: {dialogue_act}")


        output = []
        input = []

        if 'color' in dialogue_act:
            input = dialogue_act['color']
            input = [item.lower() for item in input]
            # input = ''.join(char.lower() for char in dialogue_act if char not in string.punctuation)

            output = {'expected_answer': expected_answer, 'user_input': input[-1]}
            print(f"output: {output}")

            output_iu = self.create_iu(input_iu)
            output_iu.payload = output
            output_iu = retico_core.UpdateMessage.from_iu(output_iu, retico_core.UpdateType.ADD)

            self.append(output_iu)
            self.current_state = {"grounded_frame": None, "dialogue_act": None}

    def misty_response(self, message):
        pass

    def setup(self):
        self.speak_and_wait("Now you tell me the colors for each object and I will tell you if you are right")





