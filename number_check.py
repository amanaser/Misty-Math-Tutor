import os, sys
import time

os.environ['RETICO'] = '/home/slimuser/Desktop/HRI/misty project/retico-core'
os.environ['RASA'] = '/home/slimuser/Desktop/HRI/misty project/retico-rasanlu'
os.environ['MISTY'] = '/home/slimuser/Desktop/HRI/misty project/misty'

sys.path.append(os.environ['RETICO'])
sys.path.append(os.environ['RASA'])
sys.path.append(os.environ['MISTY'])

import random
import string
import threading
import retico_core
import retico_core.audio
from retico_mistyrobot.mistyPy.Robot import Robot
from retico_core import abstract
from retico_core.text import SpeechRecognitionIU, TextIU
from retico_core.audio import MicrophoneModule
from retico_rasanlu.rasanlu import RasaNLUModule
from retico_core.dialogue import DialogueActIU

class NumberCheckModule(abstract.AbstractModule):
    def __init__(self, misty_ip, mic):
        super().__init__()
        self.misty = misty_ip
        self.misty.display_image("e_DefaultContent.jpg")
        self.expected_number = None
        self.number_words = self.load_number_words()
        self.correct_count = 0
        self.correct_threshold = 5
        self.start_mic = False
        self.mic = None
        self.mic_running = True
        self.misty_speaking = False
        self.mic = mic


    @staticmethod
    def name():
        return "Number Check Module"

    @staticmethod
    def description():
        return "A module checking if the user correctly identifies numbers."

    @staticmethod
    def input_ius():
        return DialogueActIU

    @staticmethod
    def output_iu():
        return DialogueActIU

    # def set_mic(self, mic):
    #     self.mic = mic
    #     print(type(self.mic))

    def misty_speak(self, message):
        self.mic.stop_stream()

        print("Misty starts speaking...")
        self.misty.speak(message) 
        time.sleep(5) 
        self.misty_speaking = False
        print("Misty finished speaking.")

        self.mic.start_stream()

    def load_number_words(self):
        return ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

    def generate_random_number(self):
        self.expected_number = random.randint(1, len(self.number_words))

    def num_to_word(self, number):
        num_to_word_map = {
            "1": "one", "2": "two", "3": "three", "4": "four", "5": "five",
            "6": "six", "7": "seven", "8": "eight", "9": "nine", "10" : "ten"
        }

        if num_to_word_map.get(number, "") is not None:
            return num_to_word_map.get(number, "")
        else:
            return number
        
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

    def process_update(self, update_message):
            for iu, um in update_message:
                print(f"iu: {iu}")
                print(f"um: {um}")
                if um == abstract.UpdateType.ADD:
                    self.process_iu(iu)
                    # self.send_update(iu)
                elif um == abstract.UpdateType.REVOKE:
                    self.process_revoke(iu)

    # def send_update(self, iu):
    #     output_iu = self.create_iu(iu)
    #     output_iu.payload = iu.get_text()
    #     print(f"output: {output_iu}")
    #     um = retico_core.UpdateMessage.from_iu(output_iu, retico_core.UpdateType.ADD)
    #     self.append(um)

    def process_iu(self, iu):

        input_iu = iu
        iu = iu.payload
        print(f"iu: {iu}")

        output = []
        input = []

        if 'arithmetic_answer' in iu:
            input = iu['arithmetic_answer']
            if any(char.isalpha() for char in input):
                input = [item.lower() for item in input]
                input = self.word_to_num(input)
                asr = input[-1]

                print(f"asr: {asr}")
                print(f"expected number: {self.expected_number}")

                output = {'expected_answer':self.expected_number, 'user_input': asr}

                output_iu = self.create_iu(input_iu)
                output_iu.payload = output
                output_iu = retico_core.UpdateMessage.from_iu(output_iu, retico_core.UpdateType.ADD)

                self.append(output_iu)
            else:
                asr = input[-1]

                output = {'expected_answer':self.expected_number, 'user_input': asr}

                output_iu = self.create_iu(input_iu)
                output_iu.payload = output
                output_iu = retico_core.UpdateMessage.from_iu(output_iu, retico_core.UpdateType.ADD)

                self.append(output_iu)
        

                if self.correct_count < self.correct_threshold:
                    self.generate_random_number()

    def process_revoke(self, iu):
        pass

    def start_round(self):
        self.generate_random_number()
        expected_word = self.num_to_word(str(self.expected_number))
        self.misty.display_image(f"{expected_word}.png")
        self.misty_speak(f"What number is this?")
        # self.start_mic = True

    def setup(self):
        # self.start_mic = False
        # self.misty.speak("Now let's check how well you learned the numbers.")
        # self.mic.stop()
        self.start_round()





 # def misty_speak(self, message):
    #     def speak_thread():
    #         self.misty_speaking = True

    #         if self.mic.stream:
    #             self.mic.stream.stop_stream()
    #             print("stream")
    #         else:
    #             print("no stream")

    #         print("Misty starts speaking...")
    #         self.misty.speak(message)  # Misty speaks here
    #         time.sleep(5)  # Simulate the duration of Misty's speech
    #         self.misty_speaking = False
    #         print("Misty finished speaking.")

    #         if not self.mic.stream:
    #             self.mic.stream.start_stream()
    #             print("stream")
    #         else:
    #             print("no stream")

    #     threading.Thread(target=speak_thread, daemon=True).start()
    