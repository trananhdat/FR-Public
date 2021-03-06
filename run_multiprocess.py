import argparse
import tkinter as tk
from frame import AppFrame
from frame_sleep import SleepFrame
"""
10◇May @tw1tt3rart
┈┈┈┈◢▇▇▇▇▇◣┈┈┈┈┈
┈┈┈┈▉◤◤◤◤◤▊▍#NgocTuHan
┈┈▕▔▉┏▅╮╭▅┓▍▏┈┈┈
┈┈┈╲◥╲▔▕▕▔▕╱┈┈┈┈
┈┈┈┈┈▍▔╱▔╲▕┈┈┈┈┈
┈┈┈┈▇◣╲▔▔▕◢▍┈┈┈┈
┈◢▇▇▊▊▕▇▇▏▉▇▇◣┈┈
"""

ap = argparse.ArgumentParser()

ap.add_argument("--video_src", type=int, default= 3,help="Source camera")
args = ap.parse_args()
   
root = tk.Tk()
main_app = AppFrame(root,args.video_src, 640, 480)

root.mainloop()


# root2.mainloop()
