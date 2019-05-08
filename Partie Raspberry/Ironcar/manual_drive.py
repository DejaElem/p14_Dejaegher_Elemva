import evdev
from evdev import InputDevice, categorize, ecodes, UInput
import time
import board
import busio
from adafruit_servokit import ServoKit
import adafruit_pca9685
import time
import sys
from picamera import PiCamera
from picamera.array import PiRGBArray
from PIL import Image
from threading import Thread
from constantes import *

i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
kit = ServoKit(channels=16)
capture = False
kill_received = False
vitesse = 0
direction = 0

#############################################

#loop and filter by event code and print the mapped label

class Camera(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.delay = float(sys.argv[1])
        
        # Setup Camera
        self.camera = PiCamera()
        self.camera.resolution = IM_SIZE
        self.camera.framerate = 60
        self.camera.rotation = IM_ROTATION 
        rawCapture = PiRGBArray(self.camera, size = IM_SIZE)
        self.rawCapture = PiRGBArray(self.camera, size = IM_SIZE)


    def run(self):
            start = time.time()
            i=0
            for frame in self.camera.capture_continuous(self.rawCapture, format="rgb", use_video_port=True):
                if kill_received == True:
                    break
                # convert img as Array
                image = frame.array
                # take an image
                if vitesse != 0 and capture == True:
                    if time.time() - start > self.delay:
                        im = Image.fromarray(image, 'RGB')
                        t_stamp = time.time()
                        #picname = "/home/pi/Desktop/Ironcar/image/" + str(vitesse) + "_" + str(direction) + "_" + str(t_stamp) + ".jpg"
                        picname = IM_PATH + str(t_stamp) + "_" + str(vitesse) + "_" + str(direction)  + ".jpg"
                        im.save(picname)
                        print(str(i) + " - snap : " + picname)
                        i += 1
                        start = time.time()
                # Clean image before the next comes
                self.rawCapture.truncate(0)

        
class Controler(Thread):    

    def __init__(self):
        Thread.__init__(self)
        hat.frequency = 50
        kit.servo[0].angle = DIR_STRAIGHT
        kit.servo[1].angle = SPEED_STOP     
        
    def run(self):
        global capture
        global direction
        global vitesse
        
        for device in devices:
            if('Xbox' in device.name):
                gamepad = InputDevice('/dev/input/event'+device.path.split("event")[1])

        for event in gamepad.read_loop():
                
             #RECUPERER LE NOM DE L'EVENEMENT
             if event.type in ecodes.bytype:
                    codename = ecodes.bytype[event.type][event.code]

             #BOUTONS A, B, X, Y
             if event.type == ecodes.EV_KEY:
                if event.value == 1: 
                    if 'BTN_NORTH' in codename:
                        print("Y")
                    elif 'BTN_EAST' in codename:
                        print("B")
                        kit.servo[1].angle = SPEED_REVERSE
                    elif 'BTN_A' in codename:
                        print("A")
                        kit.servo[1].angle = SPEED_SLOW
                        vitesse = 1
                    elif 'BTN_C' in codename:
                        print("X")
                    elif 'BTN_TR' in codename:
                        print('start')
                        
                elif event.value == 0: 
                    if 'BTN_NORTH' in codename:
                        print("Y relache")
                        capture = not capture #active/desactive la capture d'image
                        print("capture = " + str(capture))
                    elif 'BTN_EAST' in codename:
                        print("B relache")
                        kit.servo[1].angle = SPEED_STOP
                    elif 'BTN_A' in codename:
                        print("A relache")
                        kit.servo[1].angle = SPEED_STOP
                        vitesse = 0
                    elif 'BTN_C' in codename:
                        print("X relache")
                    elif 'BTN_TR' in codename:
                        global kill_received
                        kill_received = True
                        break
                    

             if event.type == ecodes.EV_ABS:
                if event.value == 1: 
                    if 'ABS_HAT0Y' in codename:
                        print("bas")
                    elif 'ABS_HAT0X' in codename:
                        print("droite")
                        kit.servo[0].angle = DIR_RIGHT
                        direction = 1
                elif event.value == -1:
                    if 'ABS_HAT0Y' in codename:
                        print("haut")
                    elif 'ABS_HAT0X' in codename:
                        print("gauche")
                        kit.servo[0].angle = DIR_LEFT
                        direction = -1
                elif event.value == 0: 
                    if 'ABS_HAT0Y' in codename:
                        print("vertical relache")
                    elif 'ABS_HAT0X' in codename:
                        print("horizontal relache")
                        kit.servo[0].angle = DIR_STRAIGHT
                        direction = 0

def main():
        controller_found = False       
        for device in devices:
            if('Xbox' in device.name):
                controller_found = True
                print("Manette Xbox trouvée !")
        if(controller_found == False):
            print("Manette Xbox non connectée\nFin du programme")
            return 0
                 
        print("Usage : press 'Y' to start/stop taking pictures | press 'start' to stop the prog")
        
        thread_1 = Camera()
        thread_2 = Controler()

        thread_1.start()
        thread_2.start()
 
        thread_1.join()
        thread_2.join()
    

if __name__ == "__main__":
    main()
