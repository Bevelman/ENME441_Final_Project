#Libraries
#from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import RPi.GPIO as GPIO
import time
import multiprocessing
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 25
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#Read distance fromUltrasonic Sensor
def distance(dist):
  while True:

    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    dist.value = (TimeElapsed * 34300) / 2
    time.sleep(1)
 
dist = multiprocessing.Value('f')
p = multiprocessing.Process(target=distance,args=(dist,))
p.daemon = True
p.start()

lcd = LCD()
def safe_exit(signum, frame):
    exit(1)
try:
  #signal(SIGTERM, safe_exit)
  #signal(SIGHUP, safe_exit)
  while True:
    lcd.text("Dist = %.1f cm" % dist.value, 1)
    time.sleep(1)
    #pause()
except KeyboardInterrupt:
  GPIO.cleanup()
  p.terminate()
finally:
  lcd.clear()