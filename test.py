import sys
import tkinter as tk
from PIL import Image, ImageTk
import time
import datetime
import os
import mss



class FakeWindow:
    def __init__(self, root, parent, image):
        self.root = root
        self.parent = parent
        self.img = image

        self.parent.geometry("500x500+0+0")
        self.parent.attributes("-fullscreen", True)
        self.parent.attributes("-topmost", True)
        self.frame = tk.Canvas(self.parent, bd=0, highlightthickness=0)
        self.frame.pack(side = "bottom", fill = "both", expand = "yes")

        self.setup_components()


    def setup_components(self):
        self.img = ImageTk.PhotoImage(self.img)
        
        self.frame.create_image(0, 0, image=self.img, anchor='nw')
        #pix = self.img.load()
        #pix[10, 10] = (0, 255, 0)


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

        base = os.path.dirname(os.path.realpath(__file__))
        self.intrusion_data_folder = os.path.join(base, "reports/hack_attemp_" + time.strftime("%d-%m-%y_%H:%M", time.localtime()))

        

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
with mss.mss() as ms:
    img = ms.grab(ms.monitors[2])

img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")

main = FakeWindow(None, root, img)
root.mainloop()


