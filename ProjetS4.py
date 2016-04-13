# -*- coding: utf-8 -*-

# The aim of this module is to bring together the python script and its GUI


import main, gui
from threading import Thread


class Script(Thread) :

    def __init__(self,picture) :
        Thread.__init__(self)
        self.picture = picture
        return

    def run(self) :
        main.main(self.picture)
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
            gui.disp_pic(interf,"tmp/spectrogram.jpg")
        return




pic = "spectrograms/HF_3700_details2.jpg"



def compute(picture) :
    thread1.picture = picture
    thread1.start()
    return


thread1 = Script(pic)

thread2 = Gui(pic)
#interf = thread2.launchApp(pic)
thread2.start()


