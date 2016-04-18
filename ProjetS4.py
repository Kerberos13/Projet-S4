# -*- coding: utf-8 -*-

# The aim of this module is to bring together the python script and its GUI
# Because we want the GUI to work as the computation goes, we need to create several threads

import main,gui
from threading import Thread
#import subprocess
import os,time




# This is a mutex, a shared resource with mutual exclusion in order to avoid conflict

class mutex() :

    def __init__(self,value) :
        self.toCancel = value
        self.locked = False
        return

    def set(value) :
        self.toCancel = value
        return

    def get() :
        return self.toCancel

    def lock() :
        i = 0
        while (i<10) : # We allow up to 10 tries
            if self.get() : # The lock has already been taken
                i+=1
                time.sleep(.1)
            else : # The lock is free
                self.set(True)
                return True # Locking was a success
        return False # Locking was a failure

    def unlock() :
        self.set(False)
        return
        



# This thread is the calculation thread

class Script(Thread) :

    def __init__(self,picture) :
        Thread.__init__(self)
        self.picture = picture
        self.threshold = 3
        self.margin = 10
        self.size = 5
        self.color = [120,120,250]
        #self.process = None
        return

    """
    def stop(self) :
        if self.process is not None:
            self.process.terminate()
            self.process = None
        return
    """

    """
    def isOver(self) :
        self.process = None
        return
    """

    def run(self) :
        """
        cmd = [ "bash", 'process.sh']
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        """
        main.main(self.picture, self.threshold, self.margin, self.size, self.color, True) # The last optional argument is set to True to signify that the GUI is launched
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
        """
        while(self.threadToNotify.is_alive()) :
            if(not self.threadToWatch.is_alive()) :
                threadToNotify.isOver()
            else :
                threadToNotify.isNotOver()
        """
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
        """
        while(self.scriptThread.is_alive() and self.guiThread.is_alive()) :
            if gui.toCancel :
                #main.toCancel = True
                self.scriptThread.stop()
        """
        while (self.scriptThread.is_alive() or self.started == False) :

            if self.scriptThread.is_alive :
                self.started = True

            if gui.toCancel() :

                res = list()
                p = os.popen('ps -eLF | grep "ProjetS4" | grep "python"','r')
                while True :
                    line = p.readline()
                    if not line :
                        break
                    else :
                        res.append(str(line))

                if (len(res) == 7) : # We are capable of stoping the thread
                    res = res[3].split(" ")
                    # The thread ID is the 7th item in the list
                    res = res[6]
                    gui.printOnConsole("Canceling thread ID "+str(res))
                    print("Canceling thread ID "+str(res))
                    os.popen('kill '+str(res),"r")
                else :
                    gui.printOnConsole("Error: calculation cannot be cancelled")
                    print("Calculation cannot be cancelled - Error")

            time.sleep(.1) # We do not need the thread to run all the time, we might as well save som resources

        return


pic = "default.png"


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
    thread3 = Watcher(thread1,thread2)
    thread3.start()
    thread4 = CancelWatcher(thread1,thread2)
    thread4.start()
    return

thread2 = Gui(pic) # This launches the GUI
thread2.start()
