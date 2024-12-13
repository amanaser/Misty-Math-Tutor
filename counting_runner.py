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


misty = Robot("192.168.0.101")
misty.move_head(0, 0, 0, velocity = 100)
counting = CountingModule(misty)

counting.run()

input()

counting.stop()