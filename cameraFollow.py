import time
import picamera
import picamera.array
import cv2
import robohat
import math
import numpy as np

robohat.init()

max_range = 45
step_size = 2
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

try:
    with picamera.PiCamera() as camera:
        #camera.start_preview()
        camera.resolution = (160,120)
        camera.hflip = True
        camera.vflip = True
        time.sleep(2)
        while True:
            with picamera.array.PiYUVArray(camera) as stream:
                camera.capture(stream, format='yuv')
                # At this point the image is available as stream.array
                image = stream.array
                intensities = image[:,:,0]
                max_index = np.unravel_index(intensities.argmax(), intensities.shape)
                width = intensities.shape[1]
                height = intensities.shape[0]
                x = max_index[1]
                y = max_index[0]
                print(x, y)
                """if x < (width / 2):
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
                    print "Down" """
except KeyboardInterrupt:
    robohat.setServo(tiltId, 0)
    robohat.setServo(panId, 0)
    
finally:
    robohat.cleanup()
