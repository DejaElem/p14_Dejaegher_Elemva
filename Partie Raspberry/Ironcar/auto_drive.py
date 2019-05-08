import busio
import board
from pivideostream import PiVideoStream
from keras.models import load_model
import adafruit_pca9685
from const import *
import numpy as np
import sys
import time
from adafruit_servokit import ServoKit
from constantes import *


#Load model
model = load_model(sys.argv[1])
print("Model loaded")

# Init engines and shield
i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)
kit = ServoKit(channels=16)

hat.frequency = 50
kit.servo[0].angle = 100
kit.servo[1].angle = 100    


vs = PiVideoStream().start()
time.sleep(2.0)

from PIL import Image
frame = vs.read()
img = Image.fromarray(frame)
#img.save("test.jpg")

was_direction = 0

#
print("Ready ! press CTRL+C to STOP :")

try:
    # loop over some frames...this time using the threaded stream
    while True:
            # grab the frame from the threaded video stream 
            frame = vs.read()
            image = np.array([frame]) / 255.0
            # Model prediction
            preds_raw = model.predict(image)
            preds = [np.argmax(pred, axis=0) for pred in preds_raw]
            # Action
            kit.servo[1].angle = SPEED_SLOW
            print(preds)
            if preds[0] == 1:
                if was_direction == 1:
                    #time.sleep(0.1)
                    was_direction = 0
                print('tout droit')
                kit.servo[0].angle = 100
            elif preds[0] == 0:
                print('gauche')
                kit.servo[0].angle = DIR_LEFT
                was_direction = 1
            elif preds[0] == 2:
                print('droite')
                kit.servo[0].angle = DIR_RIGHT
                was_direction = 1
            #time.sleep(0.1)
                
            
            
except KeyboardInterrupt:
    pass

# Stop the machine : put motors at initial angles
kit.servo[0].angle = 100
kit.servo[1].angle = 100    
vs.stop()
print("Stop")
