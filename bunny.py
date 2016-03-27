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
    print('Starting wall avoid')
    speed = 100
    time_end = time.time() + 4
    # main loop
    try:
       for i in range(2):
            time_end = time.time() + 6
            while time.time() < time_end:
                rightSensor = robohat.irRight()
                leftSensor = robohat.irLeft()
                if rightSensor and leftSensor:
                    robohat.spinLeft(speed)
                    time.sleep(1)
                elif rightSensor:
                    robohat.spinLeft(speed)
                    time.sleep(0.2)
                elif leftSensor == True:
                    robohat.spinRight(speed)
                    time.sleep(0.2)
                else:
                    robohat.forward(speed)
            robohat.forward(0)
            time.sleep(3)
            robohat.forward(speed)
            time.sleep(0.2)
            robohat.spinLeft(speed)
            time.sleep(4)

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
    thread.start_new_thread(wallAvoid, ())
    time.sleep(5)
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


