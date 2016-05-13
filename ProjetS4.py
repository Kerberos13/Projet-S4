# -*- coding: utf-8 -*-

# The aim of this module is to bring together the python script and its GUI
# Because we want the GUI to work as the computation goes, we need to create several threads

import sys,os
sys.path.insert(0,'scripts/')

import main
from threading import Thread
import os,time


if int(sys.version[0]) == 2 :
    print("Using Python2 compatibility mode - For a better experience, please try running Python3")
    from scripts import gui2 as gui
elif int(sys.version[0]) == 3 :
    from scripts import gui3 as gui
else :
    print("Unsupported Python version: please try running Python2 or greater - Fatal Error")
    sys.exit()





# This thread is the calculation thread

class Script(Thread) :

    def __init__(self,picture) :
        Thread.__init__(self)
        self.picture = picture
        self.threshold = 3
        self.margin = 10
        self.size = 5
        self.color = [120,120,250]
        self.toCancel = main.mutex(False)
        #self.process = None
        return



    def run(self) :
       
        main.main(self.picture, self.threshold, self.margin, self.size, self.color, True)#, self.toCancel) # The last optional arguments are set to True to signify that the GUI is launched and to False in order not to cancel the script
        return




# This thread is the Graphical User Interface thread

class Gui(Thread) :

    def __init__(self,picture) :
        Thread.__init__(self)
        self.picture = picture
        self.calculationOver = False
        return

    def isOver(self) : # Calculation is over
        self.calculationOver = True
        gui.disp_pic("tmp/spectrogram.jpg")
        return

    def isNotOver(self) : # Calculation is not over
        self.calculationIsOver = False
        return

    def run(self) :
        gui.launchApp(self.picture)
        return



# This thread watches the Script thread and communicates with the GUI thread

class Watcher(Thread) :

    def __init__(self,threadToWatch,threadToNotify) :
        Thread.__init__(self)
        self.threadToWatch = threadToWatch
        self.threadToNotify = threadToNotify
        return

    def run(self) :
        self.threadToNotify.isNotOver()
        gui.switchToCancel()
        self.threadToWatch.join()
        self.threadToNotify.isOver()
        #self.threadToWatch.isOver()
        gui.switchToCompute()
        return



# This thread watches if the Script thread needs to be cancelled

class CancelWatcher(Thread) :

    def __init__(self,scriptThread,guiThread) :
        Thread.__init__(self)
        self.scriptThread = scriptThread
        self.guiThread = guiThread
        self.started = False
        return

    def run(self) :
        # Note: when running, up to 6 threads are launched, probably one for python, one for ProjetS4.py, one for the GUI, one for the script main.py, one for the Watcher and the last one for the CancelWatcher (by order of launch).
        # If the cancel button is pressed, it means that there should be 6 active threads (7 when counting the ps command line), of which the 4th is the script to interrupt.
        

        while (self.scriptThread.is_alive() or self.started == False) :

            if self.scriptThread.is_alive :
                self.started = True

            if gui.toCancel() : # gui.toCancel is a flag, main.toCancel is a mutex containing a flag
                if main.toCancel.lock() :
                    main.toCancel.set(True)
                    main.toCancel.unlock()

            time.sleep(.05) # We do not need the thread to run all the time, we might as well save some resources

        return


pic = "default.png"


def compute(picture, threshold, margin, size, color) : # This launches the calculation
    thread1 = Script(picture)
    thread1.picture = picture
    thread1.threshold = threshold
    thread1.margin = margin
    thread1.size = size
    thread1.color = color
    if main.toCancel.lock() :
        main.toCancel.set(False)
        main.toCancel.unlock()
    gui.disp_pic(picture)
    gui.updateFrequency(picture)
    gui.clean()
    thread1.start()
    thread3 = Watcher(thread1,thread2)
    thread3.start()
    thread4 = CancelWatcher(thread1,thread2)
    thread4.start()
    return

thread2 = Gui(pic) # This launches the GUI
thread2.start()
