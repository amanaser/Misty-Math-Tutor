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
os.environ['WAC'] = '/home/slimuser/Desktop/HRI/misty project/retico-wacnlu'
os.environ['RASA'] = '/home/slimuser/Desktop/HRI/misty project/retico-rasanlu'
os.environ['DM'] = '/home/slimuser/Desktop/HRI/misty project/retico-opendialdm'
os.environ['MISTY'] = '/home/slimuser/Desktop/HRI/misty project/misty'

sys.path.append(os.environ['RETICO'])
sys.path.append(os.environ['RETICOV'])
sys.path.append(os.environ['RASA'])
sys.path.append(os.environ['YOLO'])
sys.path.append(os.environ['CLIP'])
sys.path.append(os.environ['DM'])
sys.path.append(os.environ['WAC'])
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
from retico_wacnlu.words_as_classifiers import WordsAsClassifiersModule
from retico_opendialdm.dm import OpenDialModule
from misty_action import MistyActionModule
from colors import ColorModule
from color_check import ColorCheckModule


model_dir = "models_colors/nlu-20241208-165042-commutative-wall.tar.gz"
domain_dir = 'dialogue_colors.xml'
opendial_variables = ['expected_answer', 'user_input']

# opendial_variables = ['expected_answer',
#                           'user_input',
#                           'explanation'
#                           ]

# domain_dir = 'dialogue.xml'

wac_dir = 'wac'
train_wac = False

misty = Robot("192.168.0.101")

mic = MicrophoneModule()
asr = WhisperASRModule()

misty_camera = MistyCameraModule("192.168.0.101")
# misty.move_head(0, 0, 0, velocity = 100)
misty.move_head(30, 0, 0, velocity = 100)
objdet = Yolov8()
extractor = ExtractObjectsModule(num_obj_to_display=2, save=True) 
feats = ClipObjectFeatures()
wac = WordsAsClassifiersModule(train_mode=train_wac, wac_dir=wac_dir)
nlu = RasaNLUModule(model_dir=model_dir, incremental = False)
dm = OpenDialModule(domain_dir=domain_dir, variables=opendial_variables)
misty_action = MistyActionModule("192.168.0.101", mic)

colors = ColorModule("192.168.0.101")
color_check = ColorCheckModule("192.168.0.101", mic)


# mic = MicrophoneModule()
# asr = WhisperASRModule()
# nlu = RasaNLUModule(model_dir=model_dir, incremental = False)
# arithmetic = ArithmeticModule("192.168.0.101")
# dm = OpenDialModule(domain_dir=domain_dir, variables=opendial_variables)
# misty_action = MistyActionModule("192.168.0.101")
debug = DebugModule(print_payload_only=True)

misty.display_image("e_DefaultContent.jpg")



misty_camera.subscribe(objdet)
objdet.subscribe(extractor)
extractor.subscribe(feats)
mic.subscribe(asr)
asr.subscribe(nlu)
feats.subscribe(wac)
wac.subscribe(color_check)
nlu.subscribe(color_check)
color_check.subscribe(dm)
dm.subscribe(misty_action)
misty_action.subscribe(debug)


while True:
    misty_camera.run()
    objdet.run()
    extractor.run()
    mic.run()
    asr.run()
    nlu.run()
    feats.run()
    wac.run()
    color_check.run()
    dm.run()
    misty_action.run()
    debug.run()

    input()

    misty_camera.stop()
    objdet.stop()
    extractor.stop()
    mic.stop()
    asr.stop()
    nlu.stop()
    feats.stop()
    wac.stop()
    color_check.stop()
    dm.stop()
    misty_action.stop()
    debug.stop()

