# import os,sys
# import random
# import string

# # retico
# from retico_core import abstract
# from retico_core.text import SpeechRecognitionIU, TextIU
# from retico_core.dialogue import DialogueActIU


# class NumberCheckModule(abstract.AbstractModule):
#     def __init__(self):
#             super().__init__()
#             self.expected_number = None
#             self.number_words = self.load_number_words()

#     @staticmethod
#     def name():
#         return "Number Check Module"

#     @staticmethod
#     def description():
#         return "A module checking if the user correctlt identifies the numbers"

#     @staticmethod
#     def input_ius():
#         return [SpeechRecognitionIU]

#     @staticmethod
#     def output_iu():
#         return [TextIU]
    
#     def load_number_words(self):
#         with open('answers.txt', 'r') as f:
#             return [line.strip() for line in f.readlines()]
        
#     def generate_random_number(self):
#         self.expected_number = random.randint(1, len(self.number_words))  
#         return str(self.expected_number)
    
#     def number_to_word(self, number):
#         num_to_word_map = {
#             "1": "one", "2": "two", "3": "three", "4": "four", "5": "five",
#             "6": "six", "7": "seven", "8": "eight", "9": "nine", "10" : "ten"
#         }

#         if num_to_word_map.get(number, "") is not None:
#             return num_to_word_map.get(number, "")
#         else:
#             return number
    
#     def process_update(self, update_message):
#         for iu, um in update_message:
#             if um == abstract.UpdateType.COMMIT:
#                 self.process_iu(iu)
#             elif um == abstract.UpdateType.REVOKE:
#                 self.process_revoke(iu)
    
#     def process_iu(self, iu):
#         translator = str.maketrans('', '', string.punctuation)
#         input = iu.get_text()

#         asr = str(input).lower().translate(translator)

#         if asr.isdigit():
#             asr = self.number_to_word(asr)

#         print(f"asr: {asr}")

#         if str(self.expected_number).isdigit():
#             self.expected_number = self.number_to_word(str(self.expected_number))

#         c_expected_number = str(self.expected_number).lower().translate(translator)
#         print(f"c_expected_number: {c_expected_number}")

#         while True:
#             if asr == c_expected_number:
#                 print (f"Great job! The number was {c_expected_number}.")
#             else:
#                 return f"That's not correct. Let's try again! What number is this? {self.number_words[self.expected_number - 1]}."

#     def process_revoke(self, iu):
#         print("Input revoked:", iu.get_text())

#     def setup(self):
#         self.generate_random_number()
#         print(f"self.expected_number: {self.expected_number}")




import os, sys

os.environ['RETICO'] = '/home/slimuser/Desktop/HRI/misty project/retico-core'
sys.path.append(os.environ['RETICO'])

import random
import string
import retico_core
from retico_mistyrobot.mistyPy import Robot
from retico_core import abstract
# from retico_core.abstract import AbstractModule
from retico_core.text import SpeechRecognitionIU, TextIU


class NumberCheckModule(abstract.AbstractModule):
    def __init__(self, misty_ip):
        super().__init__()
        self.misty = misty_ip
        self.misty.display_image("e_DefaultContent.jpg")
        self.expected_number = None
        self.number_words = self.load_number_words()
        self.correct_count = 0
        self.correct_threshold = 5

    @staticmethod
    def name():
        return "Number Check Module"

    @staticmethod
    def description():
        return "A module checking if the user correctly identifies numbers."

    @staticmethod
    def input_ius():
        return SpeechRecognitionIU

    @staticmethod
    def output_iu():
        return TextIU

    def load_number_words(self):
        return ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

    def generate_random_number(self):
        self.expected_number = random.randint(1, len(self.number_words))

    def number_to_word(self, number):
        num_to_word_map = {
            "1": "one", "2": "two", "3": "three", "4": "four", "5": "five",
            "6": "six", "7": "seven", "8": "eight", "9": "nine", "10" : "ten"
        }

        if num_to_word_map.get(number, "") is not None:
            return num_to_word_map.get(number, "")
        else:
            return number

    def process_update(self, update_message):
        for iu, um in update_message:
            if um == abstract.UpdateType.COMMIT:
                self.process_iu(iu)
                self.send_update(iu)
            elif um == abstract.UpdateType.REVOKE:
                self.process_revoke(iu)

    def send_update(self, iu):
        output_iu = self.create_iu(iu)
        output_iu.payload = iu.get_text()
        print(f"output: {output_iu}")
        um = retico_core.UpdateMessage.from_iu(output_iu, retico_core.UpdateType.ADD)
        self.append(um)

    def process_iu(self, iu):
        translator = str.maketrans('', '', string.punctuation)
        input = iu.get_text()
        asr = str(input).lower().translate(translator)
        if asr.isdigit():
            asr = self.number_to_word(asr)
        print(f"asr: {asr}")

        if str(self.expected_number).isdigit():
            self.expected_number = self.number_to_word(str(self.expected_number))

        c_expected_number = str(self.expected_number).lower().translate(translator)
        print(f"c_expected_number: {c_expected_number}")

        if asr == c_expected_number:
            self.correct_count += 1
            self.misty.speak(random.choice([
                "Great job!",
                "Well done!",
                "You're amazing!",
                "Keep it up!"
            ]))

            if self.correct_count < self.correct_threshold:
                self.generate_random_number()
                self.start_round()
            else:
                self.misty.display_image("e_DefaultContent.jpg")
                self.misty.speak("Congratulations! You've mastered the numbers!")
                self.correct_count = 0  
        else:
            self.misty.speak(f"Not quite. The correct answer was {c_expected_number}.")
            self.correct_count = max(0, self.correct_count - 1)  # Optional: penalize incorrect answers
            self.start_round()



        # self.append(update_message)

    def process_revoke(self, iu):
        pass

    def start_round(self):
        self.generate_random_number()
        expected_word = self.number_to_word(str(self.expected_number))
        self.misty.display_image(f"{expected_word}.png")
        self.misty.speak(f"What number is this?")

    def setup(self):
        self.misty.speak("Now let's check how well you learn.")
        self.start_round()






    