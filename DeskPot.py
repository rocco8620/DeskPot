import sys
import tkinter as tk
from PIL import Image, ImageTk
import time
import datetime
import os
import mss
import time

###################
# START OF CONFIG #
###################

# Message to flash to the intruder
MESSAGE = 'Intruder!'
# Character size of the message
MESSAGE_SIZE = 120
# Total number of click/keypresses to trigger the message and start of the photo shoot
EVENTS_TO_WAIT = 4
# Number of photos to shoot
N_OF_PHOTOS = 20
# Time between the photos in seconds
# Don't choose a too low value or this can make the script irresponsive
PHOTO_INTERVAL = 0.5

#################
# END OF CONFIG #
#################

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
        # The label takes up all the screen
        panel.pack(side = "bottom", fill = "both", expand = "yes")

        self.message_label = tk.Label(panel, text = MESSAGE, font = ("Courier", MESSAGE_SIZE), bg='red', fg='yellow')


    def bind_events(self, element):
        element.bind("<Button-1>", self.user_event_handler)
        element.bind("<Key>", self.user_event_handler)

    def user_event_handler(self, evt):
        if self.event_counter != EVENTS_TO_WAIT:
            self.event_counter += 1
        else:
            # Start taking photos
            #take_pictures_of_intruder()
            # We wait 2 seconds before warning the intruder that something is off
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

# with --no-wait the script takes the desktop's screenshoot right away instead of waiting 3 seconds. 
if not(len(sys.argv) > 1 and sys.argv[1] == '--no-wait'):
    time.sleep(3)

main = Unclosable_Fullscreen_Window()
main.window.mainloop()
main.window.overrideredirect(True)