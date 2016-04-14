# -*- coding: utf-8 -*-

# The aim of this module is to bring together the python script and its GUI


import main,gui
from threading import Thread


# This thread is the calculation thread

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
        main.main(self.picture, self.threshold, self.margin, self.size, self.color, True) # The last optional argument is set to True to signify that the GUI is launched
        return



# This thread is the Graphical User Interface thread

class Gui(Thread) :

    def __init__(self,picture) :
        Thread.__init__(self)
        self.picture = picture
        return

    def run(self) :
        gui.launchApp(self.picture)
        if not thread1.is_alive() :
            gui.disp_pic("tmp/spectrogram.jpg")
        
        # Need to clean the console display before starting the calculations
        return



pic = "spectrograms/HF_3700_details2.jpg"


def compute(picture, threshold, margin, size, color) : # This launches the calculation
    thread1 = Script(picture)
    thread1.picture = picture
    thread1.threshold = threshold
    thread1.margin = margin
    thread1.size = size
    thread1.color = color
    gui.disp_pic(picture)
    gui.clean()
    thread1.start()
    return


thread2 = Gui(pic) # This launches the GUI
thread2.start()

