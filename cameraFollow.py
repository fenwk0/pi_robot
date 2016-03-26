import time
import picamera
import picamera.array
import cv2
import robohat
import math
import numpy as np
import io
import random
import io
import time
import threading

robohat.init()

max_range = 45
step_size = 2
panId = 0
tiltId = 1
panVal = 0
tiltVal = 0

print('resetting servos...')
robohat.setServo(panId, panVal)
robohat.setServo(tiltId, tiltVal)
print('...servos reset')

def panDown():
    global panVal, panId
    panVal = max(-max_range, panVal-step_size)
    robohat.setServo(panId, panVal)

def panUp():
    global panVal, panId
    panVal = min(max_range, panVal+step_size)
    robohat.setServo(panId, panVal)

def tiltRight():
    global tiltVal, tiltId
    tiltVal = min(max_range, tiltVal+step_size)
    robohat.setServo(tiltId, tiltVal)

def tiltLeft():
    global tiltVal, tiltId
    tiltVal = max(-max_range, tiltVal-step_size)
    robohat.setServo(tiltId, tiltVal)



class FollowLight(picamera.array.PiYUVAnalysis):
    def analyse(self, a):
        print('analysing')
        intensities = a[:, :, 0]
        max_index = np.unravel_index(intensities.argmax(), intensities.shape)
        width = intensities.shape[1]
        height = intensities.shape[0]
        x = max_index[1]
        y = max_index[0]
        print(x, y)
        if x < (width / 2):
            tiltLeft()
            print "Left"
        else:
            tiltRight()
            print "Right"
        if y < (height / 2):
            panUp()
            print "Up"
        else:
            panDown()
            print "Down"


try:
    with picamera.PiCamera(framerate=5) as camera:
        camera.hflip = True
        camera.vflip = True
        print('starting camera')
        with FollowLight(camera) as output:
            camera.resolution = (320, 240)
            camera.start_recording(
                  '/dev/null', format='yuv')
            camera.wait_recording(10)
            camera.stop_recording()

except KeyboardInterrupt:
    robohat.setServo(tiltId, 0)
    robohat.setServo(panId, 0)
finally:
    robohat.cleanup()
