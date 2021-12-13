import RPi.GPIO as GPIO
import json
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
lArmPin = 16
xRotPin = 20
yRotPin = 21
leftMPin = 19
#rightMPin = 26
GPIO.setup(xRotPin, GPIO.OUT)
GPIO.setup(yRotPin, GPIO.OUT)
GPIO.setup(lArmPin, GPIO.OUT)
GPIO.setup(leftMPin, GPIO.OUT)
#GPIO.setup(rightMPin, GPIO.OUT)

# set min & max % duty cycles for servos
dcMin = 3
dcMax = 12

pwmx = GPIO.PWM(xRotPin, 50) # controls x rotation servo
pwmy = GPIO.PWM(yRotPin, 50) # controls y rotation servo
pwmL = GPIO.PWM(lArmPin, 50) # controls launch arm servo
pwmM = GPIO.PWM(leftMPin, 50) # controls flywheels
pwmx.start(0)
pwmy.start(0)
pwmL.start(0)
#initialize to halfway to hold projectile in place
pwmL.ChangeDutyCycle(7)


try:
  while True:
    # The next 3 lines are just in case file is empty or can't be opened:
    slider1_val = '3'
    slider2_val = '3'
    data = json.loads("'slider1':slider1_val, 'slider2':slider2_val, 'launch':0")  

    # Get data from the file:
    with open("led-pwm-multiple.txt", 'r') as f:
      data = json.load(f)

    # Rotate the servos based on slider input
    slider1_val = int(data['slider1'])
    slider2_val = int(data['slider2'])
    pwmx.ChangeDutyCycle(slider1_val)
    pwmy.ChangeDutyCycle(slider2_val)
    # Run launch sequence if launch button is pressed
    if bool(data['launch']):
      pwmM.ChangeDutyCycle(100) #run flywheels
      time.sleep(0.5)
      pwmL.ChangeDutyCycle(3) #load projectile
      time.sleep(0.5)
      pwmL.ChangeDutyCycle(12) #push projectile into flywheels
    time.sleep(0.1)  # small sleep step to avoid re-opening the file too often
    

except KeyboardInterrupt:
  print("closing")
  GPIO.cleanup()