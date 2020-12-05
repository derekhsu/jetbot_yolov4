import os
import cv2
import subprocess
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO
import pycuda.autoinit
import time, queue, threading
from utils.yolo_classes import get_cls_dict
import numpy as np
from datetime import datetime
from jetbot import Robot

robot = Robot()

image_root = os.path.join("Pictures", datetime.utcnow().strftime('%Y%m%d%H%M%S'))

os.makedirs(image_root)



import RPi.GPIO as GPIO
#import time

GPIO.setmode(GPIO.BOARD)  # Set Jetson Nano to use pin number when referencing GPIO pins.

GPIO.setup(33, GPIO.OUT)  # Set GPIO pin 33 (PWM2) to output mode, pin 32 is PWM1.

pwm = GPIO.PWM(33, 5000)

# define frequency for each tone
B0  = 31
C1  = 33
CS1 = 35
D1  = 37
DS1 = 39
E1  = 41
F1  = 44
FS1 = 46
G1  = 49
GS1 = 52
A1  = 55
AS1 = 58
B1  = 62
C2  = 65
CS2 = 69
D2  = 73
DS2 = 78
E2  = 82
F2  = 87
FS2 = 93
G2  = 98
GS2 = 104
A2  = 110
AS2 = 117
B2  = 123
C3  = 131
CS3 = 139
D3  = 147
DS3 = 156
E3  = 165
F3  = 175
FS3 = 185
G3  = 196
GS3 = 208
A3  = 220
AS3 = 233
B3  = 247
C4  = 262
CS4 = 277
D4  = 294
DS4 = 311
E4  = 330
F4  = 349
FS4 = 370
G4  = 392
GS4 = 415
A4  = 440
AS4 = 466
B4  = 494
C5  = 523
CS5 = 554
D5  = 587
DS5 = 622
E5  = 659
F5  = 698
FS5 = 740
G5  = 784
GS5 = 831
A5  = 880
AS5 = 932
B5  = 988
C6  = 1047
CS6 = 1109
D6  = 1175
DS6 = 1245
E6  = 1319
F6  = 1397
FS6 = 1480
G6  = 1568
GS6 = 1661
A6  = 1760
AS6 = 1865
B6  = 1976
C7  = 2093
CS7 = 2217
D7  = 2349
DS7 = 2489
E7  = 2637
F7  = 2794
FS7 = 2960
G7  = 3136
GS7 = 3322
A7  = 3520
AS7 = 3729
B7  = 3951
C8  = 4186
CS8 = 4435
D8  = 4699
DS8 = 4978

# bufferless VideoCapture
class VideoCapture:

  def __init__(self, name):
    self.cap = cv2.VideoCapture(name, cv2.CAP_GSTREAMER)
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return self.q.get()

class MusicPlayer:

    def __init__(self, init_speed=0.1):
        #t = threading.Thread(target=self._play)
        #t.daemon = True
        self.speed = init_speed
        print("Start to play music")
        #t.start()

    def _play(self):
        print("Play music")
        pac_man = [B3, 0, B4, 0, FS4, 0, DS4, 0, B4, FS4, B3, 0,
           DS4, 0, 0, 0, C4, 0, C5, 0, G4, 0, E4, 0,
           C5, G4, C4, 0, E4, 0, 0, 0, B3, 0, B3, 0,
           FS3, 0, DS4, 0, B4, FS4, B3, 0, DS4, 0, 0, 0,
           DS4, E4, F4, 0, F4, FS4, G4, 0, G4, GS4,
           A4, 0, B4, 0, 0, 0]

        #while True:
        pwm.start(0)
        for i in pac_man:
            if i == 0:
                pwm.ChangeDutyCycle(0)
            else:
                pwm.ChangeFrequency(i)
        
            pwm.ChangeDutyCycle(30)

            time.sleep(self.speed)
        pwm.stop()

    def set_speed(self, speed):
        self.speed = speed

gst_elements = str(subprocess.check_output('gst-inspect-1.0'))

width = 416
height = 416

if 'nvcamerasrc' in gst_elements:
    # On versions of L4T prior to 28.1, you might need to add
    # 'flip-method=2' into gst_str below.
    gst_str = ('nvcamerasrc ! '
               'video/x-raw(memory:NVMM), '
               'width=(int)2592, height=(int)1458, '
               'format=(string)I420, framerate=(fraction)30/1 ! '
               'nvvidconv ! '
               'video/x-raw, width=(int){}, height=(int){}, '
               'format=(string)BGRx ! '
               'videoconvert ! appsink').format(width, height)
elif 'nvarguscamerasrc' in gst_elements:
    gst_str = ('nvarguscamerasrc ! '
               'video/x-raw(memory:NVMM), '
               'width=(int)1920, height=(int)1080, '
               'format=(string)NV12, framerate=(fraction)30/1 ! '
               'nvvidconv flip-method=2 ! '
               'video/x-raw, width=(int){}, height=(int){}, '
               'format=(string)BGRx ! '
               'videoconvert ! appsink').format(width, height)
else:
    raise RuntimeError('onboard camera source not found!')

cap = VideoCapture(gst_str)

print("Start to load YoloV4 model")
trt_yolo = TrtYOLO('yolov4_my-416', (416, 416), 4)

print("YoloV4 model is loaded.")

cls_dict = get_cls_dict(4)
vis = BBoxVisualization(cls_dict)

def detect_center(bboxes):
    center_x = (bboxes[0][0]/416 + bboxes[0][2]/416) / 2.0 - 0.5
    center_y = (bboxes[0][1]/416 + bboxes[0][3]/416) / 2.0 - 0.5
    return (center_x, center_y)


speed = 0.5
turn_gain = 0.3
center = None

bypass_number = 0
found_number = 0
barrier_center = -1

player = MusicPlayer()

try:
    while(True):

        print("bypass_number: ", bypass_number)
    
        # Capture frame-by-frame
        frame = cap.read()  # ret = 1 if the video is captured; frame is the image

        # Our operations on the frame come here
        img = cv2.flip(frame,1)   # flip left-right
        img = cv2.flip(img,0)     # flip up-down

        boxes, confs, clss = trt_yolo.detect(img, 0.65)
        print("boxes:", boxes)
        print("confs:", confs)
        print("clss:", clss)

        # Find target
        target_clss_index = clss < 3
        target_boxes = boxes[target_clss_index]

        if len(target_boxes) > 0:
            print("Found target ", len(target_boxes)  ," and set barrier_center = -1")
            barrier_center = -1

        # Find barriers
        barriers_clss_index = clss > 2
        if len(boxes[barriers_clss_index]) > 0:
            print("Found barriers")
            barriers_boxes = boxes[barriers_clss_index]
            largest_barrier_box = np.array([])
            largest_barrier_size = 0
            for barriers_box in barriers_boxes:
                barrier_size = barriers_box[2] - barriers_box[0]
                barrier_box = barriers_box
                if barrier_size > largest_barrier_size:
                    largest_barrier_size = barrier_size
                    largest_barrier_box = barrier_box
            print("largest_boxes_box:", largest_barrier_box)
            print("largest_boxes_size:", largest_barrier_size)
            if len(largest_barrier_box) > 0:
                if len(target_boxes) == 0 and largest_barrier_size <= 416*0.3:
                    print("Target is not found, toward the barrier")
                    target_boxes = np.array([largest_barrier_box])

                barrier_center = detect_center(np.array([largest_barrier_box]))
                print("lagest_barrier_box_center:", barrier_center)
                if abs(barrier_center[0]) < 0.2 and largest_barrier_size > 416*0.3:
                    bypass_number = 3
                    print("Bypassing barrier...")
                    if barrier_center[0] <= 0:
                        robot.right(0.3)
                    else:
                        robot.left(0.3)
                    #robot.set_motors(
                    #    float(speed - turn_gain * barrier_center[0]),
                    #    float(speed + turn_gain * barrier_center[0])
                    #)  
                    time.sleep(0.3)
                    robot.stop()
                    continue
                
        if bypass_number >= 0:
            print("Bypassing barrier.", bypass_number)
            #robot.forward(0.3)
            robot.set_motors(0.42, 0.4)
            time.sleep(0.35)
            robot.stop()
            bypass_number -= 1
            continue 

        if len(target_boxes) == 0 and center != None and found_number == 0:
            print("barrier_center:", barrier_center)
            
            if barrier_center == -1:
                print("In tracing modei, center: ", center[0])
                if center[0] >= 0:
                    print("Turn right")
                    robot.right(0.4)
                else:
                    print("Turn left")
                    robot.left(0.4)
            else:
                print("In bypassing mode")
                if barrier_center[0] >= 0:
                    print("Turn right")
                    robot.right(0.4)
                else:
                    print("Turn left")
                    robot.left(0.4)
            time.sleep(0.2)
            robot.stop()
            time.sleep(0.2)
            cv2.imshow('Video Capture', img)
            r_img = vis.draw_bboxes(img.copy(), boxes, confs, clss)
            cv2.imwrite(os.path.join(image_root, datetime.utcnow().strftime('%Y%m%d%H%M%S') + ".jpg"), r_img)
            continue
        elif len(target_boxes) == 0 and center == None and found_number == 0:
            robot.stop()
            cv2.imshow('Video Capture', img)
            r_img = vis.draw_bboxes(img.copy(), boxes, confs, clss)
            cv2.imwrite(os.path.join(image_root, datetime.utcnow().strftime('%Y%m%d%H%M%S') + ".jpg"), r_img)
            continue

        #Stop condition checking
        if len(target_boxes) > 0:
            target_fit = (target_boxes[0][2] - target_boxes[0][0]) / 416
            print("Target fit: %f"% target_fit)
            if target_fit > 0.35:
                print("Target is found")
                found_number = 10
                robot.stop()
                cv2.imshow('Video Capture', img)
                r_img = vis.draw_bboxes(img.copy(), boxes, confs, clss)
                cv2.imwrite(os.path.join(image_root, datetime.utcnow().strftime('%Y%m%d%H%M%S') + ".jpg"), r_img)
                player._play()
                continue
        else:
            if found_number > 0:
                found_number -= 1
                print("found_nubmer:", found_number)
            continue

        center = detect_center(target_boxes)
  
        print("Center: %f" % center[0])
    
        if abs(center[0]) > 0.2:
            robot.set_motors(
                float(speed + turn_gain * center[0]),
                float(speed - turn_gain * center[0])
        )   

            time.sleep(0.2)
            robot.stop()
        else:
            #robot.forward(0.3)
            robot.set_motors(0.42, 0.4)
            time.sleep(0.35)
            robot.stop()
    
        r_img = vis.draw_bboxes(img.copy(), boxes, confs, clss)
 
        # Display the resulting image
        cv2.imshow('Video Capture', r_img)
        cv2.imwrite(os.path.join(image_root, datetime.utcnow().strftime('%Y%m%d%H%M%S') + ".jpg"), r_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break
except Exception as e:
    print("error", e)

# When everything done, release the capture
robot.stop()
cv2.destroyAllWindows()
try:
    cap.release()
except:
    pass
#pwm.stop()                         # stop PWM
GPIO.cleanup()                     # resets GPIO ports used back to input mode
