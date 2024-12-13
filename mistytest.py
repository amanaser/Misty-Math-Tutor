import os, sys
import requests
import time
from PIL import Image
import io
import requests
from io import BytesIO
import json
import threading

os.environ['RETICO'] = '/home/slimuser/Desktop/HRI/misty project/retico-core'
os.environ['RETICOV'] = '/home/slimuser/Desktop/HRI/misty project/retico-vision'
os.environ['YOLO'] = '/home/slimuser/Desktop/HRI/misty project/retico-yolov8'
os.environ['CLIP'] = '/home/slimuser/Desktop/HRI/misty project/retico-clip'
os.environ['WAC'] = '/home/slimuser/Desktop/HRI/misty project/retico-wacnlu'
os.environ['WASR'] = '/home/slimuser/Desktop/HRI/misty project/retico-whisperasr'
os.environ['RASA'] = '/home/slimuser/Desktop/HRI/misty project/retico-rasanlu'
os.environ['DM'] = '/home/slimuser/Desktop/HRI/misty project/retico-opendialdm'
os.environ['MISTY'] = '/home/slimuser/Desktop/HRI/misty project/misty'

sys.path.append(os.environ['RETICO'])
sys.path.append(os.environ['RETICOV'])
sys.path.append(os.environ['WASR'])
sys.path.append(os.environ['YOLO'])
sys.path.append(os.environ['CLIP'])
sys.path.append(os.environ['WAC'])
sys.path.append(os.environ['RASA'])
sys.path.append(os.environ['DM'])
sys.path.append(os.environ['MISTY'])

from retico_core.debug import DebugModule
from retico_core.audio import MicrophoneModule
from retico_whisperasr.whisperasr import WhisperASRModule
from retico_yolov8.yolov8 import Yolov8
from retico_vision.vision import ExtractObjectsModule
from retico_clip.clip import ClipObjectFeatures
from retico_rasanlu.rasanlu import RasaNLUModule
from retico_core.dialogue import DialogueActIU
from retico_opendialdm.dm import OpenDialModule

# from mistyPy.Robot import Robot as R
from counting import CountingModule
from retico_mistyrobot.mistyPy.Robot import Robot
# from mistyPy.Events import Events
from retico_mistyrobot.misty_camera import MistyCameraModule
import number_check
from number_check import NumberCheckModule
from misty_action import MistyActionModule


class MistyLearningAssistant:
    def __init__(self, ip):

        self.misty = Robot(ip)
        self.misty.move_head(0, 0, 0, velocity = 100)
        self.ip = ip
        self.misty.display_image("e_DefaultContent.jpg")
        self.model_dir = "models/nlu-20241126-132611-rapid-mast.tar.gz"
        self.opendial_variables = ['expected_answer', 'user_input']
        self.domain_dir = 'dialogue_numbers.xml'

    def start(self):
        self.intro()

    def print_status(self, response, caller_function):
        print(f"Status from {caller_function}")
        # print(response.status_code)
        # print(response.json())
        # print(response.json()["result"])

    def intro(self):

        # misty_camera = MistyCameraModule("192.168.0.101")
        # self.misty.move_head(0, 0, 0, velocity = 100)
        # objdet = Yolov8()
        # extractor = ExtractObjectsModule(num_obj_to_display=2, save=True) 
        # feats = ClipObjectFeatures()
        
        mic = MicrophoneModule()
        asr = WhisperASRModule()
        debug = DebugModule(print_payload_only=True) 
        nlu = RasaNLUModule(model_dir=self.model_dir, incremental = False)  
        dm = OpenDialModule(domain_dir=self.domain_dir, variables=self.opendial_variables)
        misty_action = MistyActionModule("192.168.0.101", mic)
        counting = CountingModule(self.misty)
        num_check = NumberCheckModule(self.misty, mic)

        
        # misty_camera.subscribe(objdet)
        # objdet.subscribe(extractor)
        # extractor.subscribe(feats)
        # feats.subscribe(debug)
        mic.subscribe(asr)
        asr.subscribe(nlu)
        nlu.subscribe(num_check)
        num_check.subscribe(dm)
        dm.subscribe(misty_action)
        num_check.subscribe(debug)
        asr.subscribe(debug)
        misty_action.subscribe(debug)


        while True:
            num_check.run()
            mic.run()  
            asr.run()
            nlu.run()
            dm.run()
            misty_action.run()
            debug.run()

            input()
            mic.stop()
            asr.stop()
            nlu.stop()
            num_check.stop()
            dm.stop()
            misty_action.stop()
            debug.stop()

        # monitor_thread = threading.Thread(target=self.monitor_misty_speaking, args=(mic, asr, debug, num_check))
        # monitor_thread.daemon = True  
        # monitor_thread.start()
        # try:
        #     while True:
        #         if num_check.misty_speaking:  
        #             if mic.stream.is_active():
        #                 mic.stream.stop_stream()
        #                 asr.stop()
        #                 debug.stop()
        #                 print("Microphone stream stopped.")
        #         else:
        #             if not mic.stream.is_active():
        #                 mic.stream.start_stream()
        #                 asr.run()
        #                 debug.run()
        #                 # print("Microphone stream started.")
        # except KeyboardInterrupt:
        #     print("Exiting program.")
        # finally:
        #     mic.stop()
        #     print("Microphone stopped cleanly.")


misty = MistyLearningAssistant("192.168.0.101")
misty.start()

