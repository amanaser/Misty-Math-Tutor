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
from misty.retico_mistyrobot.mistyPy.Robot import Robot
from misty.retico_mistyrobot.mistyPy.RobotCommands import RobotCommands
from misty.retico_mistyrobot.mistyPy.Events import Events
from misty.retico_mistyrobot.misty_camera import MistyCameraModule
from color_detector import ColorDetectionModule
import os
from transformers import AutoModel, AutoProcessor
from PIL import Image
import torch

detected_objects = {}

def capture_speech_callback(data):
    print(data["message"])

    description = data["message"].get("description", "unknown")
    confidence = data["message"].get("confidence", 0)

    if description in detected_objects:
        detected_objects[description]["count"] += 1
    else:
        detected_objects[description] = {"count": 1, "confidence": confidence}


    print(f"detected_objects: {detected_objects}")

misty = Robot("192.168.0.101")
misty.move_head(30, 0, 0, velocity = 100)
misty.register_event(Events.ObjectDetection, "ObjectDetection", 
                     callback_function=capture_speech_callback, keep_alive=True)






