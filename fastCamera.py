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


import io
import time
import threading
import picamera

# Create a pool of image processors
done = False
lock = threading.Lock()
pool = []

class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()

    def run(self):
        # This method runs in a separate thread
        global done
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    self.stream.seek(0)
                    # Read the image and do some processing on it
                    #Image.open(self.stream)
                    image = np.fromstring(self.stream.getvalue(), dtype=np.uint8)
                    #image = Image.open(self.stream)
                    print(type(image))
                    print(image)
                    intensities = image[:,:]
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
                        #...
                        #...
                        # Set done to True if you want the script to terminate
                    # at some point
                    #done=True
                finally:
                    done = True
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the pool
                    with lock:
                        pool.append(self)

def streams():
    while not done:
        with lock:
            if pool:
                processor = pool.pop()
            else:
                processor = None
        if processor:
            yield processor.stream
            processor.event.set()
        else:
            # When the pool is starved, wait a while for it to refill
            time.sleep(0.1)

with picamera.PiCamera() as camera:
    pool = [ImageProcessor() for i in range(4)]
    camera.resolution = (640, 480)
    camera.framerate = 10
    camera.start_preview()
    time.sleep(2)
    camera.capture_sequence(streams(), use_video_port=True)

# Shut down the processors in an orderly fashion
while pool:
    with lock:
        processor = pool.pop()
    processor.terminated = True
    processor.join()
