from retico_mistyrobot.mistyPy import Robot
from retico_core import abstract
import requests
import time
import os

class CountingModule(abstract.AbstractProducingModule):

    @staticmethod
    def name():
        return "AbstractProducingModule"

    @staticmethod
    def description():
        return "This module makes the Misty robot count from 1 to 10 while displaying images."

    @staticmethod
    def input_ius():
        return []

    @staticmethod
    def output_iu():
        return "CountAndDisplayIU"
    

    def __init__(self, misty_ip, **kwargs):
        super().__init__(**kwargs)
        self.misty = misty_ip
        self.max_count = 10
        self.current_number = 0 

    # def _run(self):
    #     """Run the module to produce outputs (speak and display images)."""
    #     self.prepare_run()
    #     self._is_running = True
    #     try:
    #         while self._is_running:
    #             with self.mutex:
    #                 self.count_and_display()
    #                 time.sleep(1)  
    #     finally:
    #         self.shutdown()

    def process_update(self, update_message):
        return None  
    
    def number_to_word(number):
        num_map = {
            1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
            6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"
        }
        return num_map.get(number, str(number))
    
    def count_and_display(self):
        number_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

        for _ in range(1): 
            for i, word in enumerate(number_words, 1):
                self.misty.speak(f"Counting: {word}")
                self.misty.display_image(f"{word}.png")
                time.sleep(2)

            time.sleep(2)
            self.misty.speak("Great job! Let's do it one more time.")
            self.misty.display_image("e_DefaultContent.jpg")
            time.sleep(2)

        self.shutdown()
        
        

    def print_status(self, response, caller_function):
        print(f"Status from {caller_function}")


    def prepare_run(self):
        self.misty.display_image("e_DefaultContent.jpg")
        self.misty.speak("Hi! Today, we will practice counting numbers together.")
        time.sleep(1)
        self.misty.speak(f"We'll count from one to {self.max_count}.")
        time.sleep(2)

        self.current_number = 1
        self.count_and_display()
    
    def shutdown(self):
        self._is_running = False
        self.misty.speak("We're all done now. Thanks for counting with me!")
        self.misty.display_image("e_DefaultContent.jpg")
        self.misty.stop_action()


    # def start(self):
    #     self.introduction()
    #     self.count_numbers()

    # def introduction(self):
    #     introduction = self.misty.say("Hello! Today, we are going to learn to count from one to ten.")
    #     self.print_status(introduction, "introduction")
    #     time.sleep(2) 

    # def count_numbers(self):
    #     for number in range(1, 11):
    #         self.misty.say(str(number))
    #         time.sleep() 

