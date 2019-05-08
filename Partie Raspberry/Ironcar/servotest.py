import time
import board
import busio
from adafruit_servokit import ServoKit
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)

 
# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)

hat.frequency = 50

kit.servo[1].angle = 112 #value to test
time.sleep(2)
kit.servo[1].angle = 100 #change to sleep position once determined
time.sleep(2)



