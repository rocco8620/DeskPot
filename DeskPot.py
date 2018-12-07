import sys
import tkinter as tk
from PIL import Image, ImageTk
import time
import datetime
import os
import mss



class Unclosable_Fullscreen_Window:

    def __init__(self):

        self.take_screenshot()

        self.window = tk.Tk()
        self.frame = tk.Frame(self.window)
        self.frame.pack()
        self.window.attributes("-fullscreen", True)
        self.window.attributes("-topmost", True)
        self.window.bind("<Escape>", self.end_fullscreen)
        self.window.protocol('WM_DELETE_WINDOW', lambda: None)
        self.window.lift()

        self.setup_components()
       

    def take_screenshot(self):
        ms = mss.mss()
        self.img = ms.grab(ms.monitors[0])
        self.img = Image.frombytes("RGB", self.img.size, self.img.bgra, "raw", "BGRX")

       
    def setup_components(self):
        self.img = ImageTk.PhotoImage(self.img)
        panel = tk.Label(self.frame, image = self.img, bg='blue')

        # Il label occupa tutto lo schermo
        panel.pack(side = "bottom", fill = "both", expand = "yes")


    def end_fullscreen(self, event=None):
        sys.exit()


main = Unclosable_Fullscreen_Window()
main.window.mainloop()
main.window.overrideredirect(True)