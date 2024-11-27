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
os.environ['WASR'] = '/home/slimuser/Desktop/HRI/misty project/retico-whisperasr'
os.environ['RASA'] = '/home/slimuser/Desktop/HRI/misty project/retico-rasanlu'
os.environ['MISTY'] = '/home/slimuser/Desktop/HRI/misty project/misty'

sys.path.append(os.environ['RETICO'])
sys.path.append(os.environ['RETICOV'])
sys.path.append(os.environ['RASA'])
sys.path.append(os.environ['WASR'])
sys.path.append(os.environ['MISTY'])

from retico_core.debug import DebugModule
from retico_core.audio import MicrophoneModule
from retico_whisperasr.whisperasr import WhisperASRModule
from retico_rasanlu.rasanlu import RasaNLUModule
from retico_core.dialogue import DialogueActIU
from retico_mistyrobot.mistyPy.Robot import Robot
from arithmetic import ArithmeticModule

model_dir = "models/nlu-20241126-132611-rapid-mast.tar.gz"

mic = MicrophoneModule()
asr = WhisperASRModule()
nlu = RasaNLUModule(model_dir=model_dir, incremental = False)
arithmetic = ArithmeticModule("192.168.0.101")
debug = DebugModule(print_payload_only=True)

mic.subscribe(asr)
asr.subscribe(nlu)
nlu.subscribe(arithmetic)
arithmetic.subscribe(debug)

mic.run()
asr.run()
nlu.run()
arithmetic.run()
print('ready')
debug.run()

input()

mic.stop()
asr.stop()
nlu.stop()
arithmetic.stop()
debug.stop()