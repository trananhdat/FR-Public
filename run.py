from main_frame import AppFrame
import tkinter as tk, cv2 
import threading
from schedule_restart import restart_device

if __name__ == '__main__':

    x = threading.Thread(target= restart_device, args=())
    x.daemon = True 
    x.start()

    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--video_src", type=int, default= 1,help="Source camera")
    args = ap.parse_args()
    
    cap = cv2.VideoCapture(args.video_src)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cap.set (cv2.CAP_PROP_FPS, 30)

    root = tk.Tk()

    root.geometry("{0}x{1}+0+0".format(1024, 768))
    root.resizable(0, 0) # khong the resize app
        
    # tat tieu de va fullsceen
    root.wm_attributes('-type', 'splash')
    root.wm_attributes('-fullscreen','true')
    root.configure(background='white')

    main_app = AppFrame(root, cap)
    root.mainloop()

   
