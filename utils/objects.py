import cv2
import numpy as np 
import math
from PIL import ImageTk, Image
from utils.graphic import in_frame
from datetime import datetime

def distance_box(box1, box2):
    p1_x = (box1[2] + box1[0]) // 2 
    p1_y = (box1[1] + box1[3]) // 2

    p2_x = (box2[2] + box2[0]) // 2 
    p2_y = (box2[1] + box2[3]) // 2

    distance = math.sqrt((p1_x - p2_x) ** 2 + (p1_y - p2_y) ** 2)

    if distance > 35:
        return False
    return True

class FaceObject:

    def __init__(self, id ,rect, frame):

        self.id = id  
        self.img = frame[rect[1]:rect[3],rect[0]:rect[2]] 
        self.frame_maintained = 1
        self.rect = rect
        self.name = ''
        self.call_again = True 
        self.remove_time = 0
        
    
    def checking_accept(self, rect):
        return distance_box(rect, self.rect)
        
    def update_from_detection(self, frame, rect):
        
        self.img = frame[rect[1]:rect[3],rect[0]:rect[2]]
        self.rect = rect
        self.frame_maintained += 1
        #if self.frame_maintained == 5:
            #self.tracker = MOSSE(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), rect)
            
class FaceHistory:

    def __init__(self, face, name, time):

        face = cv2.resize(face, (90,90))
        image = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
        self.face_view = ImageTk.PhotoImage(image)
        obj_now = datetime.now()
        self.name = name 
        self.time = str(obj_now.hour) + ":" + str(obj_now.minute) + ":" + str(obj_now.second)

        # hour, minute, second and microsecond

