import tkinter as tk 
import time
class SleepFrame(tk.Frame):

    def __init__(self, root):

        self.root = root 
        tk.Frame.__init__(self, self.root)
        self.config_master()
        self.create_widgets_clock()

    def config_master(self):

        # cau hinh kich thuoc app
        self.master.geometry("{0}x{1}+0+0".format(1024, 768))
        self.master.resizable(0, 0) # khong the resize app
        self.master.config(bg = "#081923")
        # tat tieu de va fullsceen
        self.master.wm_attributes('-type', 'splash')
        self.master.wm_attributes('-fullscreen','true')
        self.master = tk.Frame(self.root,bg = "#081923", height = 768, width = 1024)
        self.show()
    
    def show(self):
        self.master.place(x = 0, y = 0)

    def hide(self):
        self.master.place_forget () 

    def create_widgets_clock(self):

        lbl_hr = tk.Label(self.master, text = "12", font = ("times new roman",50, "bold"), bg = "#0875B7", fg = "white")
        lbl_hr.place(x = 182 , y = 279 ,width = 150, height = 150 ) 

        lbl_hr2 = tk.Label(self.master, text = "HOUR", font = ("times new roman",20, "bold"), bg = "#0875B7", fg = "white")
        lbl_hr2.place(x = 182 , y = 439 ,width = 150, height = 50 ) 

        lbl_min = tk.Label(self.master, text = "12", font = ("times new roman",50, "bold"), bg = "#0875B7", fg = "white")
        lbl_min.place(x = 352 , y = 279 ,width = 150, height = 150 ) 

        lbl_min2 = tk.Label(self.master, text = "MINUTE", font = ("times new roman",20, "bold"), bg = "#0875B7", fg = "white")
        lbl_min2.place(x = 352, y = 439 ,width = 150, height = 50 ) 

        lbl_sec = tk.Label(self.master, text = "12", font = ("times new roman",50, "bold"), bg = "#DF002A", fg = "white")
        lbl_sec.place(x = 522 , y = 279 ,width = 150, height = 150 ) 

        lbl_sec2 = tk.Label(self.master, text = "SECOND", font = ("times new roman",20, "bold"), bg = "#DF002A", fg = "white")
        lbl_sec2.place(x = 522 , y = 439 ,width = 150, height = 50 ) 
        
        lbl_noon = tk.Label(self.master, text = "12", font = ("times new roman",50, "bold"), bg = "#DF002A", fg = "white")
        lbl_noon.place(x = 692 , y = 279 ,width = 150, height = 150 ) 

        lbl_noon2 = tk.Label(self.master, text = "NOON", font = ("times new roman",20, "bold"), bg = "#DF002A", fg = "white")
        lbl_noon2.place(x = 692 , y = 439 ,width = 150, height = 50 ) 

        def clock():
            h = str(time.strftime("%H"))
            m = str(time.strftime("%M"))
            s = str(time.strftime("%S"))
            
            if int(h) > 12 and int(m) > 0:
                lbl_noon['text'] = 'PM'
            
            else:
                lbl_noon['text'] = 'AM'

            if int(h) > 12:
                h = str( (int(h) - 12) )

            lbl_hr['text'] = h
            lbl_min['text'] = m
            lbl_sec['text'] = s

            lbl_hr.after(200, clock)
            
        return clock()
    
if __name__ == '__main__':

    root =  tk.Tk()
    app = SleepFrame(root)
    app.mainloop()
