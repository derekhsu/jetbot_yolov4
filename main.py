import cv2
import subprocess
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO
import pycuda.autoinit
import time, queue, threading
from utils.yolo_classes import get_cls_dict

from jetbot import Robot

robot = Robot()

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


speed = 0.4
turn_gain = 0.2
center = None

while(True):

    # Capture frame-by-frame
    frame = cap.read()  # ret = 1 if the video is captured; frame is the image

    # Our operations on the frame come here
    img = cv2.flip(frame,1)   # flip left-right
    img = cv2.flip(img,0)     # flip up-down

    boxes, confs, clss = trt_yolo.detect(img, 0.6)

    if len(boxes) == 0 and center != None:
        if center[0] >= 0:
            robot.left(0.3)
        else:
            robot.right(0.3)
        time.sleep(0.3)
        robot.stop()
        cv2.imshow('Video Capture', img)
        continue
    elif len(boxes) == 0 and center == None:
        robot.stop()
        cv2.imshow('Video Capture', img)
        continue

    #Stop condition checking
    target_fit = (boxes[0][2] - boxes[0][0]) / 416
    print("Target fit: %f"% target_fit)
    if target_fit > 0.6:
        robot.stop()
        cv2.imshow('Video Capture', img)
        continue

    center = detect_center(boxes)
  
    print("Center: %f" % center[0])

    if abs(center[0]) > 0.2:
        robot.set_motors(
            float(speed + turn_gain * center[0]),
            float(speed - turn_gain * center[0])
        )

        time.sleep(0.2)
        robot.stop()
    else:
        robot.forward(0.3)        
    
    r_img = vis.draw_bboxes(img.copy(), boxes, confs, clss)
 
    # Display the resulting image
    cv2.imshow('Video Capture', r_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
        break


# When everything done, release the capture
robot.stop()
cap.release()
cv2.destroyAllWindows()
