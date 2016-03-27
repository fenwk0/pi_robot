import robohat, time

speed = 80

robohat.init()

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
