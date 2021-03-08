import os
import cv2
import time
#import acapture
import logging
import threading
import numpy as np
import tkinter as tk
from tkinter import *
import tkinter.font as font
from threading import Thread
from tkinter import messagebox
from PIL import ImageTk, Image
from playsound import playsound
from utils.prs import Parameters
from utils.wheather import Weather
from frame_sleep import SleepFrame
from utils.mapping import new2old, old2new
from utils.objects import FaceObject, FaceHistory
from utils.graphic import draw_fancy_box, in_frame
from detection.ultra_face_opencvdnn_inference import Light_Face
from utils.utils import covert_imgarr2base64, nomarlize_box, get_date, overlap, url_to_image
from utils.reques2api import send_image_recognition, send_image_save2database, mac2mode, getMode

class AppFrame(tk.Frame):

    def __init__ (self, master, video_src, CAM_WIDTH , CAM_HEIGHT):

        self.master = master
        tk.Frame.__init__(self, self.master)
       
        # tham số cấu hình bố cục ứng dụng
        self.image_frame = (576, 1024)
        self.header_frame = 51
        self.history_frame =  142
        self.color_history = 'white'

        # tạo ra các widget ban đầu ứng dụng        
        self.configure_gui()
        self.create_widgets()

        # configure camera
        self.cap = cv2.VideoCapture(video_src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cap.set (cv2.CAP_PROP_FPS, 30)
        # initial prs for application
        self.prs =  Parameters()
        self.init_machine()
        # detector initial
        self.detection = Light_Face(self.prs.txt, self.prs.caffe)

        # thung chua hinh anh view tren app va hinh anh hien tai dang dc xu ly
        self.panel, self.frame = None, None

        # prs work with better fps
        self.skip_frame, self.current_face, self.max_face, self.mode = 9, 0, 5, 'freeze'
        #  ['freeze', 'trainning', 'identification', 'delay']
    
        # dat ten cho các thread để sử dụng
        self.checking_face, self.checking_mode, self.sending_new_face = None, None, None

        # loop show image from 
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.video_load_loop, args=())
        
        self.thread.start()

        ## 2 thread for time and wheather
        thread_time = Thread(target=self.thread_time)
        thread_time.start()

        thread_wheather = Thread(target=self.thread_wheather)
        thread_wheather.start()

        # training varible
        self.list_FaceObject = []
        self.face_cut = []
        self.reset_after_time = 0

        # sleep mode
        self.start = None

    def init_machine(self):
        
        # kiem tra mac co hop le voi sever
        tmp = mac2mode(self.prs)
        if tmp is None:
            self.mode = 'freeze'
        else:     
            self.prs.cameraId = tmp
    def configure_gui(self):
        
        # cau hinh kich thuoc app
        self.master.geometry("{0}x{1}+0+0".format(1024, 768))
        self.master.resizable(0, 0) # khong the resize app
        
        # tat tieu de va fullsceen
        self.master.wm_attributes('-type', 'splash')
        self.master.wm_attributes('-fullscreen','true')

    def create_widgets(self):
        
        # sử dụng để show thời gian địa điểm
        self.header = tk.Frame(self.master, height = self.header_frame, width = 1024, bg = 'white')
        self.header.place(x = 0, y = 0)

        # header sẽ show logo và thơi gian có thể thêm thời tiết nếu muốn
        image = cv2.imread('images/log.jpg')
        image = cv2.resize(image, (155, self.header_frame)) 
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        image = ImageTk.PhotoImage(image)

        # set hinh nen 
        self.bg = tk.Label(self.header, image = image, height=self.header_frame, width = 155, borderwidth=0,compound="center",highlightthickness = 0)
        self.bg.image = image 
        self.bg.place(x = 20, y = -1)

        # -------------------------------------------------------------------------------------
        self.video = tk.Frame(self.master, height=self.image_frame[0], width = self.image_frame[1])
        self.video.place(x = -1, y = self.header_frame - 1)
        self.panel = None

         # -------------------------------------------------------------------------------------
        self.history = tk.Frame(self.master,bg = self.color_history, height = self.history_frame, width = 1024)
        self.history.place(x = 0, y = self.header_frame + self.image_frame[0] - 1)
    
        self.title = tk.Label(self.history, text = 'Lịch sử điểm danh:  {}'.format(get_date()),height=3, width= 30, justify ='left', bg = self.color_history,font=("Helvetica", "12", 'bold'), foreground="black")
        self.title.place(x = 0, y = 0)

        # moi block h1, h2, h3, h4 se gom co 1 anh va 2 text gom ten va time checkin

        pad_left =  25
        image_shape = 90
        text_shape = 85
        padding = 10
        height =  43
        
        self.canvas1 = tk.Canvas(self.history, width = image_shape, height = image_shape, bg = self.color_history, highlightthickness=0, relief='ridge')
        self.T1 = tk.Label(self.history, height=6, width= 11, justify ='left', bg = self.color_history,font=("Helvetica", "10" , "bold"), foreground="red")
        self.canvas1.place(x = pad_left, y = height)
        x = pad_left + image_shape + padding
        self.T1.place(x = x, y = height)
        x =  x + text_shape + padding

        self.canvas2 = tk.Canvas(self.history, width = image_shape, height = image_shape, bg = self.color_history, highlightthickness=0, relief='ridge')
        self.T2 = tk.Label(self.history, height=6, width= 11, justify ='left', font=("Helvetica", "10"), bg = self.color_history, foreground="black") 
        self.canvas2.place(x = x, y = height)
        x = x+ image_shape +  padding
        self.T2.place(x = x, y = height)
        x = x+ text_shape + padding

        self.canvas3 = tk.Canvas(self.history, width = image_shape, height = image_shape,bg = self.color_history, highlightthickness=0, relief='ridge')
        self.T3 = tk.Label(self.history, height=6, width= 11, justify ='left', font=("Helvetica", "10"), bg = self.color_history, foreground="black")
        self.canvas3.place(x = x, y = height)
        x = x+ image_shape +  padding
        self.T3.place(x = x, y = height)
        x = x+ text_shape + padding
       
        self.canvas4 = tk.Canvas(self.history, width = image_shape, height = image_shape, bg = self.color_history, highlightthickness=0, relief='ridge')
        self.canvas4.place(x = x, y = height)
        x = x+ image_shape +  padding
        self.T4 = tk.Label(self.history, height=6, width= 11, justify ='left', font=("Helvetica", "10"), bg = self.color_history, foreground="black") 
        self.T4.place(x = x, y = height)
        x = x+ text_shape + padding
        
        self.canvas5 = tk.Canvas(self.history, width = image_shape, height = image_shape, bg = self.color_history, highlightthickness=0, relief='ridge') 
        self.canvas5.place(x = x, y = height)
        x = x+ image_shape +  padding
        self.T5 = tk.Label(self.history, height=6, width= 11, justify ='left', font=("Helvetica", "10"), bg = self.color_history, foreground="black")
        self.T5.place(x = x,  y = height)
    
        self.canvas1.image, self.canvas2.image, self.canvas3.image, self.canvas4.image, self.canvas5.image = None, None, None, None, None 

    def video_load_loop(self) -> None:
        
        frame_step = 0
        while True:
            #timer = time.time()    
            
            ret, self.src_frame = self.cap.read()
            if self.mode == 'sleep':
                
                if frame_step % 3 == 0:
                    faces =  self.detection.predict_face(self.frame)
                    if len(faces) > 0:
                        # mở lại app
                        self.app.hide()
                        del self.app
                        self.mode = 'identification'
                        self.header.place(x = 0, y = 0)
                        self.video.place(x = -1, y = self.header_frame - 1)
                        self.history.place(x = 0, y = self.header_frame + self.image_frame[0] - 1)
            if ret:
                #self.frame = cv2.cvtColor(self.src_frame,cv2.COLOR_BGR2RGB)
                self.frame = cv2.resize(self.src_frame, (1024, 768))
                if self.mode == 'identification':
                    if frame_step % 3 == 0:
                        frame_step = 0; 
                        remove_objs, used, new_faces = [], [], []
                        faces = self.detection.predict_face(self.frame)
                        if len(faces) == 0:
                            # sử dụng cái object tracking mà tracking box mới
                            self.list_FaceObject = []
                            self.current_face = 0
                            self.reset_after_time = 0
                        else:
							
                            self.reset_after_time = 0; 
                            if len(self.list_FaceObject) > 0:
                                for i in range(len(self.list_FaceObject)):
                                    id_max, max_iou = overlap(faces, self.list_FaceObject[i])
                                    if max_iou > 0.1: # overlap beetween 2 box is 0.3 
                                        self.list_FaceObject[i].update_from_detection(self.frame, nomarlize_box(faces[id_max]))
                                        used.append(id_max)
                                    else:
                                        remove_objs.append(i)

                                self.remove_object(remove_objs)
                                for i in range(len(faces)):
                                    if i not in used:
                                        new_faces.append(faces[i])
                                self.create_list_object(new_faces); 
                            else:
                                self.create_list_object(faces)
                                 
                   
                    self.draw_box()
                    # tạo một luồng điểm danh
                    if self.checking_face is None or self.checking_face.is_alive() == False:
                        
                        self.checking_face =  Thread(target=self.update_name, args = ())
                        self.checking_face.daemon = True
                        self.checking_face.start()
                elif self.mode == 'freeze':
                 
                    # update camerad id và mode
                   
                    if self.prs.cameraId is None and frame_step % self.skip_frame * 6 == 0:
                        self.init_machine()
                    # update mode
                    elif self.prs.cameraId is not None and frame_step % self.skip_frame * 2 == 0:
                        frame_step = 0
                        if self.checking_mode is None or self.checking_mode.is_alive() == False:
                            self.checking_mode = Thread(target=self.update_mode, args = ())
                            self.checking_mode.daemon = True
                            self.checking_mode.start()
                
                elif self.mode == 'delay' and frame_step % self.skip_frame * 3 == 0:
                   
                    frame_step = 0
                    if self.checking_mode is None or self.checking_mode.is_alive() == False:

                        self.checking_mode = Thread(target=self.update_mode, args = ())
                        self.checking_mode.daemon = True
                        self.checking_mode.start()
               
                elif self.mode == 'trainning':
                   
                    # vẽ một box để lấy face trong đó
                    st, en = self.draw_frame_trainning()

                    if frame_step % self.skip_frame == 0 and len(self.face_cut) < 5:
                        
                        frame_step = 0
                        img_crop = self.frame[st[1]:en[1],st[0]:en[0]]
                        faces = self.detection.predict_face(img_crop)

                        self.guide_get_box(img_crop, faces)
                    
                    # đã đủ số lượng khuôn mặt để gửi đi hay chưa
                    if len(self.face_cut) > 4:

                        if self.sending_new_face is None or self.sending_new_face.is_alive() == False:                            
                            self.sending_new_face = Thread(target=self.upload_image2sever, args = ())
                            self.sending_new_face.daemon = True 
                            self.sending_new_face.start()

                    percent = int( (len(self.face_cut) / 5)  * 100) 
                    cv2.putText(self.frame, str(percent) + ' %',(400, 560),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 211, 84), 2)

                # tang dem frame len một đơn vị
                frame_step += 1; #print(1/(time.time() - timer))

                # view image result
                image = Image.fromarray(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))
                image = ImageTk.PhotoImage(image)

                
                if self.panel is None:
                    self.panel = tk.Label(self.video, image = image, height= self.image_frame[0])
                    self.panel.image = image 
                    self.panel.place(x =-1, y = -1)
                
                else:
                    self.panel.configure(image = image)
                    self.panel.image = image
                
            else:
                messagebox.showinfo("Lỗi camera", "Không thể kết nối tới camera")
                
    def create_list_object(self, faces):
        
    
        if len(faces) == 0:
            if self.start is None:
                self.start = time.time()
            else:
                if time.time() - self.start > 3 * 60:
                    self.mode = 'sleep'
                    self.start = None
                    self.video.place_forget()
                    self.header.place_forget() 
                    self.history.place_forget()
                    x = Thread(target= self.create_clock_frame)
                    x.start()
            
            return 
        
        self.start =  None
        for face in faces: # loop into list face
            if self.current_face > self.max_face:
                break
            if face[2] - face[0] > 250 or face[3] - face[1] > 250 or face[2] - face[0] < 90 or face[3] - face[1] < 90:
                 continue
            self.current_face += 1 # số lượng face tăng lên
            rect = nomarlize_box(face)
            #if self.ir_frame is not None and live_face(self.ir_frame, rect):
            # if overlap(self.list_FaceObject, rect):
            id_obj = str(time.time()).split('.')[1]
            self.list_FaceObject.append(FaceObject(id_obj,rect, self.frame))
            
    def draw_box(self):

        if len(self.list_FaceObject) == 0:
            return
        for img_face in self.list_FaceObject:
            x1,y1,x2,y2 = img_face.rect
            cv2.rectangle(self.frame, (x1-2,y1-2), (x2+2,y2+2 ), (0,255,0), 2) 
            cv2.putText(self.frame, img_face.name, (x1 , y1 - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 211, 84), 2)
           
    def draw_frame_trainning(self):
        
        h,w = self.frame.shape[:-1]
        st = (w // 5, h // 5) 
        en = (w - w // 5, h - h//5)
        cv2.rectangle(self.frame, st, en, (60, 76, 231), 2) 
        cv2.putText(self.frame, "Di chuyen khuon mat vao box ben duoi", (150,60),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 211, 84), 2)
        return st, en

    def update_name(self):

        
        list_img = [obj.img for obj in self.list_FaceObject if obj.call_again == True and obj.frame_maintained >=3 and obj.frame_maintained < 20]
        list_idx = [obj.id for obj in self.list_FaceObject if obj.call_again  == True and obj.frame_maintained >=3 and obj.frame_maintained < 20] 

        if len(list_img) == 0:   
            return 

        result = send_image_recognition(list_img, list_idx, self.prs)
        if result is None:
            # set call again all object
            for i in range(len(self.list_FaceObject)):
                if self.list_FaceObject[i].name == '':
                    self.list_FaceObject[i].call_again = True
                       
        else:
            # set call again == True for object not aceepted
            if result['status'] == 'OK' and result['mode'] == 'identification':
                for i in range(len(self.list_FaceObject)):  
                    if self.list_FaceObject[i].name == '': 
                        self.list_FaceObject[i].call_again = True 

                # set call again == False  for object accepted
                for person in result['result']:
                    id_obj = person['id']
                    
                    name = person['name']
                    for i in range(len(self.list_FaceObject)):
                        if self.list_FaceObject[i].id ==  id_obj:
                            self.list_FaceObject[i].call_again = False 
                            self.list_FaceObject[i].name = name
                            if name != 'Unknow':
                                
                                x = threading.Thread(target=self.create_object_face, args = (name,  person['id_person'] ,))
                                x.start()

                                #playsound('images/ting_cut.mp3')
                            else:
                                self.list_FaceObject[i].call_again = True 

            
            elif result['mode'] == 'trainning':
                self.mode = 'trainning'
        
    def update_mode(self):
        
        # Cập nhật lại mode cho ứng dụng sau khi lấy khuôn mặt 
        mode = getMode(self.prs)
       
        if mode is not None:
            self.mode = mode

    def upload_image2sever(self):

        stt = send_image_save2database(self.face_cut, self.prs)
        if stt == True:
            logging.info("Da gui di thanh cong")
            self.mode = 'delay'
        else:
            
            logging.info("Gui anh di that bai")
            self.mode = 'freeze'
        self.face_cut = []

    def guide_get_box(self, img_crop, faces):

        for face in faces:
            rect = nomarlize_box(face)
            draw_fancy_box(img_crop, (rect[0], rect[1]), (rect[2], rect[3]), (255, 255, 255), 2, 25)
            try:
                base64 = covert_imgarr2base64(img_crop[rect[1]:rect[3], rect[0]:rect[2]])
                if base64 is not None:
                    self.face_cut.append(base64)
            except:
                print('loi covert')
                logging.error("covert from img array to base64 error")
            break
    
    def remove_object(self, list_id):
        
        if len(list_id) == 0:
            return 

        for i,idx in enumerate(list_id):
            del self.list_FaceObject[idx - i]
            self.current_face -= 1

    def create_object_face(self, name, id_person):


        face_new = FaceHistory(url_to_image(self.prs.url_avt.format(id_person)), name, time.time())
        
        # move from 4 -> 5
        self.canvas5.create_image(0, 0, anchor=NW, image=self.canvas4.image)
        self.canvas5.image = self.canvas4.image
        self.T5['text'] =  self.T4['text']

        # move from 3 -> 4
        self.canvas4.create_image(0, 0, anchor=NW, image=self.canvas3.image)
        self.canvas4.image = self.canvas3.image
        self.T4['text'] =  self.T3['text']

        # move from  2 -> 3
        self.canvas3.create_image(0, 0, anchor=NW, image=self.canvas2.image)
        self.canvas3.image = self.canvas2.image
        self.T3['text'] =  self.T2['text']

        # move from 1 -> 2
        self.canvas2.create_image(0, 0, anchor=NW, image=self.canvas1.image)
        self.canvas2.image = self.canvas1.image
        self.T2['text'] = self.T1['text']

        # append into 1
        self.canvas1.create_image(0, 0, anchor=NW, image=face_new.face_view)
        self.canvas1.image = face_new.face_view
        self.T1['text'] = "{}\n\n{}\n\n{}".format(face_new.name, face_new.time, get_date())

    def thread_time(self):

        label = tk.Label(self.header, height=1, width= 11, justify ='left', bg = 'white',font=("Helvetica", "15", 'bold'), foreground="black")
        label.place(x = 880, y = 15)
        def digitalclock():
            text_input = time.strftime("%H:%M:%S")
            label.config(text=text_input)
            label.after(200, digitalclock)
        digitalclock()

    def thread_wheather(self):
        
        name, temp = Weather()
       # header sẽ show logo và thơi gian có thể thêm thời tiết nếu muốn
        image = cv2.imread('images/clouds.png')
        image = cv2.resize(image, (self.header_frame, self.header_frame)) 
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        image = ImageTk.PhotoImage(image)
        # set hinh nen 
        weather_icon = tk.Label(self.header, image = image, height=self.header_frame, width = self.header_frame, borderwidth=0,compound="center",highlightthickness = 0)
        weather_icon.image = image 
        weather_icon.place(x = 800, y = -1)

        # set text 
        label = tk.Label(self.header, height=1, width= 15, justify ='left', bg = 'white',font=("Helvetica", "15", 'bold'), foreground="black")
        label.place(x = 550, y = 15)
        label.config(text=name + " " + str(temp) + '°C')    
    
    def create_clock_frame(self):

        self.app = SleepFrame(self.master)

