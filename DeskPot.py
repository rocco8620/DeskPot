import sys
import tkinter as tk
from PIL import Image, ImageTk
import time
import datetime
import os
import mss
import time

MESSAGE = 'Intruder!'
MESSAGE_SIZE = 120


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

        self.event_counter = 0

        self.setup_components()
       

    def take_screenshot(self):
        ms = mss.mss()
        self.img = ms.grab(ms.monitors[0])
        self.img = Image.frombytes("RGB", self.img.size, self.img.bgra, "raw", "BGRX")

       
    def setup_components(self):
        self.img = ImageTk.PhotoImage(self.img)
        panel = tk.Label(self.frame, image = self.img)

        self.bind_events(panel)
        # Il label occupa tutto lo schermo
        panel.pack(side = "bottom", fill = "both", expand = "yes")

        self.message_label = tk.Label(panel, text = MESSAGE, font = ("Courier", MESSAGE_SIZE), bg='red', fg='yellow')


    def bind_events(self, element):
        element.bind("<Button-1>", self.user_event_handler)
        element.bind("<Key>", self.user_event_handler)

    def user_event_handler(self, evt):
        if self.event_counter != 4: # Numero di click/tasti da aspettare prima di triggherare la foto/video
            self.event_counter += 1
        else:
            # Cominciamo subito a fare foto
            #take_pictures_of_intruder()
            # Ma aspettiamo 2 secondi prima di avvertire il malcapitato
            self.window.after(2000, self.message_label.place, ({'relx':0.5, 'rely':0.5, 'anchor':'center'}))
            self.window.after(2000, self.flash_message)
            self.event_counter += 1

    def flash_message(self):
        fg = self.message_label.cget('bg')
        bg = self.message_label.cget('fg')
        self.message_label.configure(background=bg, foreground=fg)
        self.window.after(200, self.flash_message)

    def end_fullscreen(self, evt):
        sys.exit()

# L'opzione --no-wait evita di aspettare 3 secondi prima di far partire DeskPot
if not(len(sys.argv) > 1 and sys.argv[1] == '--no-wait'):
    time.sleep(3)

main = Unclosable_Fullscreen_Window()
main.window.mainloop()
main.window.overrideredirect(True)