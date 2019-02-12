import sys
import tkinter as tk
from PIL import Image, ImageTk
import time
import datetime
import os
import mss
import cv2
import pygame
import json
import screeninfo

###################
# START OF CONFIG #
###################
# this is the default config, if you want to make changes, use config.json file

# Message to flash to the intruder
MESSAGE = 'Intruder!'
# Character size of the message
MESSAGE_SIZE = 120
# Total number of click/keypresses to trigger the message and start of the photo shoot
EVENTS_TO_WAIT = 3
# Number of photos to shoot
N_OF_PHOTOS = 14
# Time between the photos in seconds
# Don't choose a too low value or this can make the script irresponsive
PHOTO_INTERVAL = 0.5
# Sound configuration: if enabled, plays a sound while the flashing message is displayed
AUDIO = 0
# if you want to add custom sounds, place audio files in folder 'audio'
# and edit this entry to the name of the file
AUDIO_SOURCE = "Spaceship_Alarm.mp3"
#audio_file = "Alarm_Clock.mp3"
#audio_file = "Man_Laugh_And_Knee_Slap.mp3"
ESCAPE_SHORTCUT = "<Control-Shift-S>"

# decommentare quando verra' fixato.
#   - Non verifica il tipo degli argomenti
#   - Rischia di caricare la configurazione a metà se il caricamento fallisce

# load configuration in file config.json
#try:
#        config_file = open("config.json", "r")
#        json_data = json.loads(config_file.read())
#        MESSAGE = json_data["message"]
#        MESSAGE_SIZE = json_data["message_size"]
#        EVENTS_TO_WAIT = json_data["events_to_wait"]
#        N_OF_PHOTOS = json_data["n_of_photos"]
#        PHOTO_INTERVAL = json_data["photo_interval"]
#        AUDIO = json_data["audio"]
#        AUDIO_SOURCE = json_data["audio_source"]
#        ESCAPE_SHORTCUT = json_data["escape_shortcut"]
#except:
#        pass

#################
# END OF CONFIG #
#################

class FakeWindow:
    def __init__(self, root, parent, image, geom):
        self.root = root
        self.parent = parent
        self.img = image

        self.frame = tk.Frame(self.parent)
        self.frame.pack()

        self.parent.geometry(geom)

        self.parent.attributes("-fullscreen", True)
        self.parent.attributes("-topmost", True)
        self.parent.bind(ESCAPE_SHORTCUT, self.root.end_fullscreen) # cambiare percorso handler
        self.parent.protocol('WM_DELETE_WINDOW', lambda: None)
        self.parent.lift()

        self.setup_components()


    def setup_components(self):
        self.img = ImageTk.PhotoImage(self.img)
        panel = tk.Label(self.frame, image = self.img)

        self.bind_events(panel)
        # The label takes up all the screen
        panel.pack(side = "bottom", fill = "both", expand = "yes")

        self.message_label = tk.Label(panel, text = MESSAGE, font = ("Courier", MESSAGE_SIZE), bg='red', fg='yellow')

    def bind_events(self, element):
        element.bind("<Button-1>", self.root.user_event_handler) # cambiare percorso handler
        element.bind("<Key>", self.root.user_event_handler)      # cambiare percorso handler


    def flash_message(self):
        fg = self.message_label.cget('bg')
        bg = self.message_label.cget('fg')
        self.message_label.configure(background=bg, foreground=fg)
        self.parent.after(200, self.flash_message)



## creazione fake windows 
    



class DeskPot:

    def __init__(self, root_window):
        self.root_window = root_window

        self.monitors = screeninfo.get_monitors()

        self.screenshoots = []
        self.fake_windows = []

        self.take_screenshots()

        for s, m in zip(self.screenshoots, self.monitors):
            # lancio le finstre con gli screenshots
            geometry = '200x200+' + str(m.x+10) + '+' + str(m.y+10)
            self.fake_windows.append(FakeWindow(self, tk.Toplevel(self.root_window), s, geometry))
        
        self.event_counter = 1
        self.took_photos = 0
        self.camera_handle = None

        self.intrusion_data_folder = "reports/hack_attemp_" + time.strftime("%d-%m-%y_%H:%M", time.localtime())

        

    def take_screenshots(self):
        with mss.mss() as ms:
            for i in range(0, len(self.monitors)):
                img = ms.grab(ms.monitors[i+1])
                self.screenshoots.append(Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX"))

        


    def user_event_handler(self, evt):
        if self.event_counter != EVENTS_TO_WAIT:
            self.event_counter += 1
        else:
            self.event_counter += 1
            # Setup intrusion data folder
            self.setup_intrusion_data_folder()
            # Setup photo environment
            self.camera_handle = cv2.VideoCapture(0)
            # Start taking photos
            self.take_pictures_of_intruder()
            # Play audio if set
            self.play_audio()

            # We wait 2 seconds before warning the intruder that something is off
            for fw in self.fake_windows:
                self.root_window.after(2000, fw.message_label.place, ({'relx':0.5, 'rely':0.5, 'anchor':'center'}))
                self.root_window.after(2000, fw.flash_message)



    def take_pictures_of_intruder(self):
        status, image = self.camera_handle.read()
        image_path = os.path.join(self.intrusion_data_folder, 'photos')
        cv2.imwrite(os.path.join(image_path,  str(self.took_photos) + '.png'), image)

        if self.took_photos < N_OF_PHOTOS:
            self.took_photos += 1
            self.root_window.after(int(PHOTO_INTERVAL*1000), self.take_pictures_of_intruder)

    def setup_intrusion_data_folder(self):
        try:
            # create reports directory if needed
            if not os.path.exists('reports'):
                os.makedirs('reports')
            # creates the main folder
            os.makedirs(self.intrusion_data_folder)
            # creates the photo folder
            os.makedirs(os.path.join(self.intrusion_data_folder, 'photos'))
        except Exception as e:
            print(str(e))
            sys.exit()

    def play_audio(self):
            if AUDIO:
                try:
                    pygame.mixer.init()
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.load('audio/' + AUDIO_SOURCE)
                    pygame.mixer.music.play()
                except:
                    pass

    def end_fullscreen(self, evt):
        sys.exit()



# with --no-wait the script takes the desktop's screenshoot right away instead of waiting 3 seconds.
if not(len(sys.argv) > 1 and sys.argv[1] == '--no-wait'):
    time.sleep(3)


root = tk.Tk()
main = DeskPot(root)
root.mainloop()


