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
from retico_wacnlu.words_as_classifiers import WordsAsClassifiersModule
from counting import CountingModule
from retico_mistyrobot.mistyPy.Robot import Robot
from retico_mistyrobot.mistyPy.RobotCommands import RobotCommands
# from retico_mistyrobot.mistyPy import Robot
from retico_mistyrobot.misty_camera import MistyCameraModule
from color_detector import ColorDetectionModule
import os
from transformers import AutoModel, AutoProcessor
from PIL import Image
import torch


if not os.path.exists('wac'):
        os.makedirs('wac')

wac_dir = 'wac'
train_wac = False

misty = Robot("192.168.0.101")
misty.move_head(30, 0, 0, velocity = 100)

mic = MicrophoneModule()
asr = WhisperASRModule()
misty_camera = MistyCameraModule("192.168.0.101")
objdet = Yolov8()
extractor = ExtractObjectsModule(num_obj_to_display=1, save=True) 
feats = ClipObjectFeatures()
# color = ColorDetectionModule()
debug = DebugModule(print_payload_only=True)


# misty_camera.subscribe(objdet)
# objdet.subscribe(color)
# color.subscribe(debug)

# misty_camera.run()
# objdet.run()
# color.run()

# input()

# misty_camera.stop()
# objdet.stop()
# color.stop()


wac = WordsAsClassifiersModule(train_mode=train_wac, wac_dir=wac_dir)
debug = DebugModule(print_payload_only=True)

misty_camera.subscribe(objdet)
objdet.subscribe(extractor)
extractor.subscribe(feats)
mic.subscribe(asr)
asr.subscribe(wac)
asr.subscribe(debug)
feats.subscribe(wac)
wac.subscribe(debug)

mic.run()
asr.run()
misty_camera.run()
objdet.run()
extractor.run()
feats.run()
wac.run()
debug.run()

input()

mic.stop()
asr.stop()
misty_camera.stop()
objdet.stop()
extractor.stop()
feats.stop()
wac.stop()
debug.stop()



