import os, sys
import requests
import time
from PIL import Image
import io
import requests
from io import BytesIO
import json
import warnings
warnings.filterwarnings('ignore')

os.environ['RETICO'] = '/home/slimuser/Desktop/HRI/misty project/retico-core'
os.environ['RETICOV'] = '/home/slimuser/Desktop/HRI/misty project/retico-vision'
os.environ['YOLO'] = '/home/slimuser/Desktop/HRI/misty project/retico-yolov8'
os.environ['CLIP'] = '/home/slimuser/Desktop/HRI/misty project/retico-clip'
os.environ['WASR'] = '/home/slimuser/Desktop/HRI/misty project/retico-whisperasr'
os.environ['RASA'] = '/home/slimuser/Desktop/HRI/misty project/retico-rasanlu'
os.environ['DM'] = '/home/slimuser/Desktop/HRI/misty project/retico-opendialdm'
os.environ['MISTY'] = '/home/slimuser/Desktop/HRI/misty project/misty'

sys.path.append(os.environ['RETICO'])
sys.path.append(os.environ['RETICOV'])
sys.path.append(os.environ['RASA'])
sys.path.append(os.environ['YOLO'])
sys.path.append(os.environ['CLIP'])
sys.path.append(os.environ['DM'])
sys.path.append(os.environ['WASR'])
sys.path.append(os.environ['MISTY'])

from retico_core.debug import DebugModule
from retico_core.audio import MicrophoneModule
from retico_whisperasr.whisperasr import WhisperASRModule
from retico_rasanlu.rasanlu import RasaNLUModule
from retico_core.dialogue import DialogueActIU
from retico_mistyrobot.mistyPy.Robot import Robot
from retico_yolov8.yolov8 import Yolov8
from retico_vision.vision import ExtractObjectsModule
from retico_clip.clip import ClipObjectFeatures
from retico_mistyrobot.misty_camera import MistyCameraModule
from retico_opendialdm.dm import OpenDialModule
from misty_action import MistyActionModule
from arithmetic import ArithmeticModule

model_dir = "models/nlu-20241126-132611-rapid-mast.tar.gz"

opendial_variables = ['expected_answer',
                          'user_input',
                          'explanation'
                          ]

domain_dir = 'dialogue.xml'

misty = Robot("192.168.0.101")

misty_camera = MistyCameraModule("192.168.0.101")
misty.move_head(20, 0, 0, velocity = 100)
objdet = Yolov8()
extractor = ExtractObjectsModule(num_obj_to_display=2, save=True) 
# feats = ClipObjectFeatures()

mic = MicrophoneModule()
asr = WhisperASRModule()
nlu = RasaNLUModule(model_dir=model_dir, incremental = False)
arithmetic = ArithmeticModule("192.168.0.101", mic)
dm = OpenDialModule(domain_dir=domain_dir, variables=opendial_variables)
misty_action = MistyActionModule("192.168.0.101", mic)
debug = DebugModule(print_payload_only=True)


misty_camera.subscribe(objdet)
objdet.subscribe(extractor)

mic.subscribe(asr)
asr.subscribe(nlu)
nlu.subscribe(arithmetic)
extractor.subscribe(arithmetic)
arithmetic.subscribe(dm)
dm.subscribe(misty_action)
misty_action.subscribe(debug)


while True:
    arithmetic.run()
    mic.run()
    asr.run()
    nlu.run()
    misty_camera.run()
    objdet.run()
    extractor.run()
    dm.run()
    misty_action.run()
    print('running')

    debug.run()

    input()

    arithmetic.stop()
    mic.stop()
    asr.stop()
    nlu.stop()
    misty_camera.stop()
    objdet.stop()
    extractor.stop()
    dm.stop()
    
    misty_action.stop()
    debug.stop()

# import threading

# def monitor_speaking():
#     while True:
#         if arithmetic.speaking:
#             if mic.running:
#                 mic.stop()
#                 print("Mic stopped: Robot is speaking")
#         else:
#             if not mic.running:
#                 mic.run()
#                 asr.run()
#                 nlu.run()
#                 dm.run()
#                 debug.run()
#                 print("Mic running: Robot is not speaking")
#         time.sleep(0.1)  

# monitor_thread = threading.Thread(target=monitor_speaking, daemon=True)
# monitor_thread.start()



