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
from retico_vision.vision import ExtractedObjectsIU, ObjectFeaturesIU

import random
import string
import retico_core
from retico_core import abstract
# from retico_core.abstract import AbstractModule
from retico_core.text import SpeechRecognitionIU, TextIU
from retico_rasanlu.rasanlu import RasaNLUModule
from retico_core.audio import MicrophoneModule
from retico_core.dialogue import DialogueActIU

class ArithmeticModule(abstract.AbstractModule):
    @staticmethod
    def name():
        return "Number Check Module"

    @staticmethod
    def description():
        return "A module teaching arithmetic."

    @staticmethod
    def input_ius():
        return DialogueActIU, ExtractedObjectsIU

    @staticmethod
    def output_iu():
        return DialogueActIU
    
    def __init__(self, ip, mic, **kwargs):
        super().__init__(**kwargs)

        self.misty = Robot(ip)
        self.questions = Queue()  
        self.current_question = None
        self.expected_answer = None
        self.explanation = None
        self.awaiting_response = False
        self.speaking = False
        self.mic = mic
        self.current_state = {"grounded_frame": None, "dialogue_act": None}

        file_path = "questions.json"
        with open(file_path, 'r') as file:
            self.data = json.load(file)

        self.populate_queue()

    def word_to_num(self, num_letter):
        word_to_num = {
            'one': '1',
            'two': '2',
            'free': '3',
            'three': '3',
            'four': '4',
            'five': '5',
            'six': '6',
            'seven': '7',
            'eight': '8',
            'nine': '9',
            'ten': '10'
        }

        converted = [word_to_num[word] for word in num_letter if word in word_to_num]
        return converted
    
    def misty_speak(self, message):
        self.mic.stop_stream()

        print("Misty starts speaking...")
        self.misty.speak(message) 
        time.sleep(10) 
        self.misty_speaking = False
        print("Misty finished speaking...")

        self.mic.start_stream()

    # def process_update(self, update_message):
    #     for iu,um in update_message:
    #         if um == abstract.UpdateType.ADD:
    #             self.process_iu(iu)
    #         elif um == abstract.UpdateType.REVOKE:
    #             self.process_revoke(iu)

    def process_update(self, update_message):
        for iu, um in update_message:
            print(f"iu: {iu}")
            if um == abstract.UpdateType.ADD:
                if isinstance(iu, ExtractedObjectsIU):
                    self.current_state["grounded_frame"] = iu.payload['num_objects']
                elif isinstance(iu, DialogueActIU):
                    # self.current_state["dialogue_act"] = None
                    self.current_state["dialogue_act"] = iu.payload

                if self.current_state["grounded_frame"] and self.current_state["dialogue_act"]:
                    self.check_answer(self.current_state, iu)


    def process_iu(self, input_iu):

        print("in check answer")
        print(f"current state: {self.current_state}")
        
        # nlu_iu = None
        # obj_iu = None

        # if isinstance(input_iu, ExtractedObjectsIU):
        #     obj_iu = input_iu.payload['num_objects']
        #     print(f"obj iu: {obj_iu}")

        # if isinstance(input_iu, DialogueActIU):
        #     nlu_iu = input_iu.payload
        #     print(f"nlu iu: {nlu_iu}")

        # if nlu_iu and obj_iu:
        #     print("in check answer")
        #     self.check_answer(str(obj_iu), self.explanation, nlu_iu, input_iu)

            # self.check_answer(self.expected_answer, self.explanation, nlu_iu, input_iu)

        
    def populate_queue(self):
            for task_id, task_data in self.data.items():
                question = {
                    "statement": task_data["Statement"],
                    "question": task_data["Question"],
                    "expected_answer": task_data["ExpectedAnswer"],
                    "explanation": task_data["Explanation"]
                }
                self.questions.put(question)

    def process_next_question(self):
        if self.current_question is None and not self.questions.empty():
            self.current_question = self.questions.get()

        if self.current_question:
            if "statement" in self.current_question and self.current_question["statement"]:
                self.misty_speak(self.current_question["statement"])

            self.misty_speak(self.current_question["question"])

            self.expected_answer = self.current_question["expected_answer"]
            self.explanation = self.current_question["explanation"]

            # self.awaiting_response = True
            self.current_question = None

    def process_revoke(self, input_iu):
        pass

    def check_answer(self, current_state, input_iu):
        print("check answer")

        expected_answer = current_state['grounded_frame']
        dialogue_act = current_state['dialogue_act']

        print(f"expected_answer: {expected_answer}")
        print(f"dialogue_act: {dialogue_act}")

        output = []
        input = []

        if 'arithmetic_answer' in dialogue_act:
            input = dialogue_act['arithmetic_answer']
            if any(char.isalpha() for char in input):
                input = [item.lower() for item in input]
                input = self.word_to_num(input)

            output = {'expected_answer': expected_answer, 'user_input': input[-1], 'explanation': self.explanation}
            print(f"input: {input}")

            output_iu = self.create_iu(input_iu)
            output_iu.payload = output
            output_iu = retico_core.UpdateMessage.from_iu(output_iu, retico_core.UpdateType.ADD)

            self.append(output_iu)
            self.current_state = {"grounded_frame": None, "dialogue_act": None}
            

            # dialogue_act['arithmetic_answer'] = []
            # self.process_next_question()

    def misty_response(self, message):
        pass

    def setup(self):
        self.process_next_question()

    # def shutdown(self):
    #     self.stop()





