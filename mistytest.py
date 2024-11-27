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
os.environ['YOLO'] = '/home/slimuser/Desktop/HRI/misty project/retico-yolov8'
os.environ['CLIP'] = '/home/slimuser/Desktop/HRI/misty project/retico-clip'
os.environ['WAC'] = '/home/slimuser/Desktop/HRI/misty project/retico-wacnlu'
os.environ['WASR'] = '/home/slimuser/Desktop/HRI/misty project/retico-whisperasr'
os.environ['MISTY'] = '/home/slimuser/Desktop/HRI/misty project/misty'

sys.path.append(os.environ['RETICO'])
sys.path.append(os.environ['RETICOV'])
sys.path.append(os.environ['WASR'])
sys.path.append(os.environ['YOLO'])
sys.path.append(os.environ['CLIP'])
sys.path.append(os.environ['WAC'])
sys.path.append(os.environ['MISTY'])

from retico_core.debug import DebugModule
from retico_core.audio import MicrophoneModule
from retico_whisperasr.whisperasr import WhisperASRModule
from retico_yolov8.yolov8 import Yolov8
from retico_vision.vision import ExtractObjectsModule
from retico_clip.clip import ClipObjectFeatures
# from mistyPy.Robot import Robot as R
from counting import CountingModule
from retico_mistyrobot.mistyPy.Robot import Robot
# from mistyPy.Events import Events
from retico_mistyrobot.misty_camera import MistyCameraModule
from number_check import NumberCheckModule


class MistyLearningAssistant:
    def __init__(self, ip):

        # self.misty_api = R(ip)
        self.misty = Robot(ip)
        self.ip = ip
        self.misty.display_image("e_DefaultContent.jpg")

    def start(self):
        self.intro()

    def print_status(self, response, caller_function):
        print(f"Status from {caller_function}")
        # print(response.status_code)
        # print(response.json())
        # print(response.json()["result"])

    def intro(self):


        misty_camera = MistyCameraModule("192.168.0.101")
        self.misty.move_head(0, 0, 0, velocity = 100)
        objdet = Yolov8()
        extractor = ExtractObjectsModule(num_obj_to_display=2, save=True) 
        feats = ClipObjectFeatures()
            
        # counting = CountingModule(self.misty)
        # num_check = NumberCheckModule(self.misty)
        # mic = MicrophoneModule()
        # asr = WhisperASRModule()
        debug = DebugModule(print_payload_only=True)

        misty_camera.subscribe(objdet)
        objdet.subscribe(extractor)
        extractor.subscribe(feats)
        # feats.subscribe(debug)
        # mic.subscribe(asr)
        # asr.subscribe(num_check)
        # num_check.subscribe(debug)


        misty_camera.run()
        objdet.run()
        extractor.run()
        feats.run()
        
        # mic.run()
        # asr.run()
        # num_check.run()
        debug.run()

        input()

        misty_camera.stop()
        objdet.stop()
        extractor.stop()
        feats.stop()

        # mic.stop()
        # asr.stop()
        # num_check.stop()
        debug.stop()

        # counting.stop()

        # response = self.misty.speak("Hello!")
        # self.print_status(response, 'intro')
        # time.sleep(1) 

        # self.misty.display_image("three.png")

        # mic = MicrophoneModule()
        # asr = WhisperASRModule()
        # num_check = NumberCheckModule()
        # debug = DebugModule(print_payload_only=True)

        # mic.subscribe(asr)
        # asr.subscribe(num_check)
        # asr.subscribe(debug)
        # num_check.subscribe(debug)


        # mic.run()
        # asr.run()
        # num_check.run()
        # debug.run()

        # input()

        # mic.stop()
        # asr.stop()
        # num_check.stop()
        # debug.stop()
        # # counting = CountingModule(self.misty)
        # counting.start()

        # self.misty.populate_images()

        # self.misty_api.DisplayImage("image.png")

        # self.display_image(retico_misty.images_saved[1])
        # self.misty_api.display_image("e_JoyGoofy3.jpg")
        # self.upload_image("/home/slimuser/Desktop/HRI/misty project/image.png")

misty = MistyLearningAssistant("192.168.0.101")
misty.start()

# from mistyPy.Robot import Robot


# if __name__ == "__main__":
#     ip_address = "192.168.0.155"
#     # Create an instance of a robot
#     misty = Robot(ip_address)

#     current_response = misty.move_arms(30, 20)
#     print(current_response)
#     print(current_response.status_code)
#     print(current_response.json())