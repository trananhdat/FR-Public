import json
# import time
# import cv2
import requests
from getmac import get_mac_address as gma
from utils.utils import covert_imgarr2base64

def send_image_recognition(list_img: list, list_idx: list, prs):

    data = {'mode': 'identification'}
    data['images'] = []
    data['cameraId'] = prs.cameraId
    
    for i, img in enumerate(list_img):
        # cv2.imwrite(str(time.time()) + '.jpg', img)
        base64 = covert_imgarr2base64(img)
        if base64 is not None:
            data['images'].append({'id': str(list_idx[i]), 'image': base64})
    # send request to sever 
    
    try:  
        response = requests.post(prs.url_recogition ,json = data, headers= prs.headers)
        
        json_data = json.loads(response.text)
    
        return json_data 
        
    except Exception as e:
        # phân ghép nói với mất mangj tai day
        print(e)
        return None
        # Nêu e là liên quan về mất mạng 

def send_image_save2database(list_img: list, prs):

    data = {'mode': 'trainning'}
    data['images'] = []
    data['cameraId'] = prs.cameraId
    
    for i, img in enumerate(list_img):
        data['images'].append({'id': str(i), 'image': img})
        
    # send request to sever 
    try:   
        response = requests.post(prs.url_recogition ,json = data, headers= prs.headers)
        print(response.text)
        if response.status_code >= 200 and response.status_code < 300:
            return True 
        return False
        
    except Exception as e:
        # phân ghép nói với mất mangj tai day
        print("[INFOR]: Diem danh bi loi ", e)
        # Nêu e là liên quan về mất mạng 
        return False

def mac2mode(prs):

    try:
        respond = requests.get(url = prs.url_mac2mode.format(gma()))
        # print(respond.status_code)
        if respond.status_code >= 200 and respond.status_code < 222:
            data = respond.json()
          
            if data['mode'] != '':
                    # đã được đăng ký với hê thống
                return data['cameraId']
                    # self.mode = data['results'][0]['mode']
            else:
                # không cho khởi động app 
                print("[INFOR]: Chua duoc dang ki voi he thong")
                return None
    except:
        # không cho khởi động app 
        print("[INFOR]: Loi gi do khong lay dc cameraId")
        return None

def getMode(prs):

    url =  prs.url_mode.format(prs.cameraId)
   
    try:
        respond =  requests.get(url)
        json_data =  json.loads(respond.text)
        
        if json_data != '' :
            return json_data['mode']
    except:
        return None
        

