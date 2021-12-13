#Libraries
#from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import RPi.GPIO as GPIO
import time
import multiprocessing
import smbus			#import SMBus module of I2C
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 25
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(3) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

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
    time.sleep(0.5)

def readAngle(angles,accel,rot):
  while True:

	  #Read Gyroscope raw value
	  gyro_x = read_raw_data(GYRO_XOUT_H)
	  gyro_y = read_raw_data(GYRO_YOUT_H)
	  gyro_z = read_raw_data(GYRO_ZOUT_H)
	
    #Read Accelerometer raw value
	  acc_x = read_raw_data(ACCEL_XOUT_H)
	  acc_y = read_raw_data(ACCEL_YOUT_H)
	  acc_z = read_raw_data(ACCEL_ZOUT_H)

	  #Full scale range +/- 250 degree/C as per sensitivity scale factor
	
	  angles[0] = gyro_x/131.0
	  angles[1] = gyro_y/131.0
	  angles[2] = gyro_z/131.0

    accel[0] = acc_x/16384.0
	  accel[1] = acc_y/16384.0
	  accel[2] = acc_z/16384.0


    rot[0] = -math.degrees(math.atan2(accel[0], dist(accel[1],accel[2])))
    rot[1] =  math.degrees(math.atan2(accel[1], dist(accel[0],accel[2])))
	  time.sleep(1)

#Run ultrasonic code
dist = multiprocessing.Value('f')
us = multiprocessing.Process(target=distance,args=(dist,))
us.daemon = True
us.start()

#Run Gyroscope code
angles = multiprocessing.Array('f',3)
accel = multiprocessing.Array('f',3)
rot = multiprocessing.Array('f',2)
gyro = multiprocessing.Process(target=readAngle,args=(angles,accel,rot))
gyro.daemon = True
gyro.start()

lcd = LCD()
def safe_exit(signum, frame):
    exit(1)
try:
  #signal(SIGTERM, safe_exit)
  #signal(SIGHUP, safe_exit)
  while True:
    lcd.text("Dist = %.1f cm" % dist.value, 1)
    lcd.text("Gx=%.2f " % rot[0] + "Gy=%.2f " % rot[1],2)
    #pause()
except KeyboardInterrupt:
  GPIO.cleanup()
  us.terminate()
  gyro.terminate()
finally:
  lcd.clear()