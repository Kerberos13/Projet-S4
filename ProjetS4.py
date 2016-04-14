# -*- coding: utf-8 -*-

# The aim of this module is to bring together the python script and its GUI


import main, gui
from threading import Thread


class Script(Thread) :

    def __init__(self,picture) :
        Thread.__init__(self)
        self.picture = picture
        self.threshold = 3
        self.margin = 10
        self.size = 5
        self.color = [120,120,250]
        return

    def run(self) :
        main.main(self.picture, self.threshold, self.margin, self.size, self.color, True)
        return




class Gui(Thread) :

    def __init__(self,picture) :
        Thread.__init__(self)
        self.picture = picture
        return

    def run(self) :
        gui.launchApp(self.picture)
        print(thread1.is_alive())
        if not thread1.is_alive() :
            gui.disp_pic("tmp/spectrogram.jpg")
        # Need to clean the console display when before starting the calculations
        return




pic = "spectrograms/HF_3700_details2.jpg"



def compute(picture, threshold, margin, size, color) :
    thread1 = Script(picture)
    thread1.picture = picture
    thread1.threshold = threshold
    thread1.margin = margin
    thread1.size = size
    thread1.color = color
    thread1.start()
    return


#thread1 = Script(pic)

thread2 = Gui(pic)
#interf = thread2.launchApp(pic)
thread2.start()


