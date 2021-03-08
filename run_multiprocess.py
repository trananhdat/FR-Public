import argparse
import tkinter as tk
from main_frame import AppFrame
from frame_sleep import SleepFrame

ap = argparse.ArgumentParser()

ap.add_argument("--video_src", type=int, default= 0,help="Source camera")
args = ap.parse_args()
   
root = tk.Tk()
main_app = AppFrame(root,args.video_src, 640, 480)

root.mainloop()


# root2.mainloop()
