import RPi.GPIO as GPIO
import json
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pwmPin1 = 20
pwmPin2 = 21
GPIO.setup(pwmPin1, GPIO.OUT)
GPIO.setup(pwmPin2, GPIO.OUT)

# set min & max % duty cycles (5 and 10 are default values, but play
# around to find optimum values for your motor)
dcMin = 3
dcMax = 12

pwm1 = GPIO.PWM(pwmPin1, 50) # PWM object at 50 Hz (20 ms period)
pwm2 = GPIO.PWM(pwmPin2, 50)
pwm1.start(0)
pwm1.start(0)

try:
  while True:
    # The next 3 lines are just in case file is empty or can't be opened:
    slider1_val = '3'
    slider2_val = '3'
    data = json.loads("'slider1':slider1_val, 'slider2':slider2_val")  

    # Get data from the file:
    with open("led-pwm-multiple.txt", 'r') as f:
      data = json.load(f)

    # Change the DC for the given LED:
    slider1_val = int(data['slider1'])
    slider2_val = int(data['slider2'])
    pwm1.ChangeDutyCycle(slider1_val)
    pwm2.ChangeDutyCycle(slider2_val)

    time.sleep(0.1)  # small sleep step to avoid re-opening the file too often
except KeyboardInterrupt:
  print("closing")
  GPIO.cleanup()