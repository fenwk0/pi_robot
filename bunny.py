import robohat, time
import sys
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
import thread

robohat.init()

max_range = 45
step_size = 3
runtime = 10
if len(sys.argv) > 1 and sys.argv[1]:
    runtime = int(sys.argv[1])
panId = 0
tiltId = 1
panVal = 0
tiltVal = 0

robohat.setServo(panId, panVal)
robohat.setServo(tiltId, tiltVal)

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

def wallAvoid():
    speed = 80

    # main loop
    try:
        while True:
            rightSensor = robohat.irRight()
            leftSensor = robohat.irLeft()
            print "right:{0}, left:{1}".format(rightSensor, leftSensor)
            if rightSensor and leftSensor:
                robohat.spinLeft(speed)
                time.sleep(1)
            elif rightSensor:
                robohat.spinLeft(speed)
                time.sleep(0.2)
                print('Turn Left')
            elif leftSensor == True:
                robohat.spinRight(speed)
                time.sleep(0.2)
                print('Turn Right')
            else:
                robohat.forward(speed)

    except KeyboardInterrupt:
        robohat.stop()
        robohat.cleanup()


class FollowLight(picamera.array.PiYUVAnalysis):
    def analyse(self, a):
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
    thread.start_new_thread(wallAvoid, ("Thread-2", 4,))
    with picamera.PiCamera(framerate=10) as camera:
        camera.hflip = True
        camera.vflip = True
        print('starting camera')
        with FollowLight(camera) as output:
            camera.resolution = (320, 240)
            camera.start_recording(output, format='yuv')
            camera.wait_recording(runtime)
            camera.stop_recording()

finally:
    robohat.setServo(tiltId, 0)
    robohat.setServo(panId, 0)
    robohat.cleanup()


