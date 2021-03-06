import cv2
import base64
import numpy as np
# from numba import jit
import urllib.request
from scipy.spatial import distance
from datetime import date

# used for linear mapping...
def linear_mapping(img):
    return (img - img.min()) / (img.max() - img.min())

# pre-processing the image...
def pre_process(img):
    # get the size of the img...
    height, width = img.shape
    img = np.log(img + 1)
    img = (img - np.mean(img)) / (np.std(img) + 1e-5)
    # use the hanning window...
    window = window_func_2d(height, width)
    img = img * window

    return img

def window_func_2d(height, width):
    win_col = np.hanning(width)
    win_row = np.hanning(height)
    mask_col, mask_row = np.meshgrid(win_col, win_row)

    win = mask_col * mask_row

    return win

def random_warp(img):
    a = -180 / 16
    b = 180 / 16
    r = a + (b - a) * np.random.uniform()
    # rotate the image...
    matrix_rot = cv2.getRotationMatrix2D((img.shape[1]/2, img.shape[0]/2), r, 1)
    img_rot = cv2.warpAffine(np.uint8(img * 255), matrix_rot, (img.shape[1], img.shape[0]))
    img_rot = img_rot.astype(np.float32) / 255
    return img_rot

def covert_imgarr2base64(img_arr):

    try:
        _, img_encoded = cv2.imencode('.jpg', img_arr)
        jpg_as_text = base64.b64encode(img_encoded).decode("utf-8") 
        return jpg_as_text
    except:
        return None

def covertimgarr2string(img_arr):
    try:
        _, img_encoded = cv2.imencode('.jpg', img_arr)
        return img_encoded.toString()
    except:
        return None
    
def nomarlize_box(face):
    try:
        h, w = face[2] - face[0],face[3] - face[1]
        if h > w:
            return (face[0],face[1] - (h-w) // 2 , face[2], face[3] + (h-w) // 2)
        elif h < w:
            return (face[0] - (w-h) // 2, face[1], face[2] + (w-h) // 2, face[3])
        else:
            return face
    except Exception as e:
        print(e)
        return face

def get_date():
    today = date.today()
    # Textual month, day and year	
    #d2 = today.strftime("%b-%d-%Y")
    return today

def bb_intersection_over_union(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])
	# compute the area of intersection rectangle
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
	boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = interArea / float(boxAArea + boxBArea - interArea)
	# return the intersection over union value
	return iou

def overlap(new_faces, old_face):
    
    ious = [bb_intersection_over_union(face, old_face.rect) for face in new_faces]    
    return np.argmax(ious), np.max(ious)

def live_face(frame_ir, rect):

    #try:
    rect = [i - 15 for i in rect]
    IMG_CUT = frame_ir[rect[0] : rect[2], rect[1] : rect[3]]
   
    _, thresh = cv2.threshold(IMG_CUT, 120, 255, cv2.THRESH_BINARY)
	
    if np.mean(IMG_CUT) > 120:
        
        return True
    return False

def url_to_image(url):
    resp = urllib.request.urlopen(url)	
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image 
    
