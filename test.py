import os, sys

os.environ['MISTY'] = '/home/slimuser/Desktop/HRI/misty project/misty'
sys.path.append(os.environ['MISTY'])



from retico_mistyrobot.mistyPy import Robot

misty = Robot.Robot(ip="192.168.0.101")
misty.speak("hi")