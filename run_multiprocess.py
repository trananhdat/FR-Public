import os
import gc
import cv2 
import time 
import tkinter as tk
from frame import AppFrame
from multiprocessing import Process, Manager

def run(src, q):
    print('Process to read: %s' % os.getpid())
    root = tk.Tk()
    main_app = AppFrame(root, src, q, 640, 480)
    root.mainloop()

def load(stack, cam, top: int) -> None:
    """
         :param cam: camera parameters
         :param stack: Manager.list object
         :param top: buffer stack capacity
    :return: None
    """
    print('Process to write: %s' % os.getpid())
    cap = cv2.VideoCapture(cam)
    #cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) # depends on fourcc available camera
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cap.set (cv2.CAP_PROP_FPS, 30)
    # print(fps)
    
    while True:

        _, img = cap.read()
        
        if _:
            stack.append(img)
            # Clear the buffer stack every time it reaches a certain capacity
            # Use the gc library to manually clean up memory garbage to prevent memory overflow
            if len(stack) >= top:
                del stack[:]
                gc.collect()
     
if __name__ == '__main__':

    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--video_src", type=int, default= 3 ,help="Source camera")
    ap.add_argument("--video_src_ir", type=int, default= 1 ,help="Source camera IR")
    args = ap.parse_args()
    
    q = Manager().list()
    pw = Process(target=load, args=(q, args.video_src_ir,24 ))
    pr = Process(target=run, args=(args.video_src, q, ))

    #---------------------------------------------------
    pw.start()
    pr.start()
    pr.join()
    pw.join()
