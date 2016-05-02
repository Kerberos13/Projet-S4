# -*- coding: utf-8 -*-

# The aim of this module is to offer a beautiful and convenient graphical user interface

import os
from tkinter import *
from PIL import Image, ImageTk
import ProjetS4
from tkinter.ttk import *
from tkinter import Button,Frame # We import those items from the tkinter module because they easily allow to change their style 


FRAME_BACKGROUND = "#2c2929" #"black"
WIDGET_BACKGROUND = "#565252" #"gray"
WIDGET_FOREGROUND =  "#ffffff" #"white"


class Interface(Frame) : # We define our window

    def __init__(self, window, picture, **kwargs) :
      
        style = Style()
        style.map('TCombobox', background=[('readonly',WIDGET_BACKGROUND)])


        # Window Background
        Frame.__init__(self, window, width=768, height=576, **kwargs,background=FRAME_BACKGROUND)
        self.pack(fill = BOTH)


        # Greetings message
        self.message = Label(self, text = "Welcome in Super Radio Spectre Analyser!",background=FRAME_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.message.grid(row=1,column=2,pady=5)     # The grid method places a widget in the window; pady is a margin around the widget


        # Quit Button
        self.Oquit_button = Button(self, text="Quit", command=self.quit, background=WIDGET_BACKGROUND, foreground=WIDGET_FOREGROUND)  # command = self.quit defines the callback function
        self.Oquit_button.grid(row=8,column=5,pady=2,padx=2)   # padx is a margin around the widget


        # Compute Button
        self.Ocompute_button = Button(self, text="Compute", command=self.compute, background=WIDGET_BACKGROUND, foreground=WIDGET_FOREGROUND)
        self.Ocompute_button.grid(row=7,column=5,pady=2,padx=2)


        # Cancel flag
        self.cancel = False


        # Spectrogram Image
        if os.path.exists(picture) :
            self.image = str(picture)
        else :
            self.image = "default.png"
        self.Oimage = ImageTk.PhotoImage(Image.open(self.image).resize((700,500),Image.ANTIALIAS)) # We use a label to display a picture
        self.Opic = Label(self,image=self.Oimage)
        self.Opic.grid(row=4,column=1,columnspan=3, padx=10)
      

        # Carrier Signal Frequency
        self.frequency = "XXXXHz"
        self.Lfrequency = Label(self,text="Carrier signal's frequency: "+self.frequency,background=FRAME_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.Lfrequency.grid(row=6, column=2,pady=5)


        # Threshold       
        self.threshold = 3                                                 # In this, self.X is an attribute of the class, saving the current value
        self.Lthreshold = Label(self,text="Threshold",background=FRAME_BACKGROUND,foreground=WIDGET_FOREGROUND)                     # self.Lx is the label of the corresponding object
        self.Lthreshold.grid(row=7,column=1,padx=2,sticky=S)
        self.Othreshold = Spinbox(self, from_=2, to=6, increment=0.5, background=WIDGET_BACKGROUND, foreground=WIDGET_FOREGROUND)    # self.Ox is the actual object
        self.Othreshold.grid(row=8,column=1,padx=2)


        # Margin
        self.margin = 12
        self.Lmargin = Label(self,text="Margin",background=FRAME_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.Lmargin.grid(row=7,column=2,padx=2,sticky=S)   # Sticky allows to place a widget off-centered from its original position, according to the cardinal points
        self.Omargin = Spinbox(self, from_=5, to = 50, increment = 5, background=WIDGET_BACKGROUND, foreground=WIDGET_FOREGROUND)
        self.Omargin.grid(row=8,column=2,padx=2)


        # Box Width
        self.boxWidth = 6
        self.LboxWidth = Label(self,text="Box Width",background=FRAME_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.LboxWidth.grid(row=7,column=3,padx=2,sticky=S)
        self.OboxWidth = Spinbox(self, from_=4, to=10, increment = 2, background=WIDGET_BACKGROUND, foreground=WIDGET_FOREGROUND)
        self.OboxWidth.grid(row=8, column=3, padx=2, sticky=W)


        # Box Color
        self.color = [250,250,250] # RGB
        self.Lcolor = Label(self, text="Box Color",background=FRAME_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.Lcolor.grid(row=7, column=4,padx=2,sticky=S)
        self.Ocolor = Combobox(self, background=WIDGET_BACKGROUND, foreground=WIDGET_FOREGROUND)
        self.Ocolor.grid(row=8, column=4,padx=2)
        self.Ocolor['values'] = ["blue","purple","red","orange","yellow","green","white","black"]


        # Spectrogram
        self.file = "spectrograms/HF_3700_details2.jpg"
        self.Lfile = Label(self, text = "Select a file",background=FRAME_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.Lfile.grid(row=2,column=4)
        self.Ofile = Combobox(self, background=WIDGET_BACKGROUND, foreground=WIDGET_FOREGROUND)
        self.Ofile.grid(row=3,column=4)
        self.Ofile['values'] = os.listdir("spectrograms/")


        # Console-like messages
        self.console = ""
        self.Oconsole = Label(self,text=self.console,width=40, background=WIDGET_BACKGROUND, foreground=WIDGET_FOREGROUND)
        self.Oconsole.grid(row=4,column=4,sticky=N,columnspan=2,pady=5)

        return




    def compute(self) : # This function gets all parameters and launches the computation

        self.threshold = int(float(self.Othreshold.get()))
        self.margin = int(float(self.Omargin.get()))
        self.boxWidth = int(float(self.OboxWidth.get()))
        tmp = str(self.Ocolor.get())
        if tmp == "blue" :
            self.color = [120,120,250]
        elif tmp == "red" :
            self.color = [250,60,60]
        elif tmp == "green" :
            self.color = [60,250,120]
        elif tmp == "yellow" :
            self.color = [250,250,60]
        elif tmp == "orange" :
            self.color = [250,170,20]
        elif tmp == "purple" :
            self.color = [250,20,250]
        elif tmp == "white" :
            self.color = [250,250,250]
        elif tmp == "black" :
            self.color = [5,5,5]
        else :
            self.color = [250,250,250] # Default color is white

        if len(str(self.Ofile.get())) != 0 :
            self.file = "spectrograms/"+str(self.Ofile.get())
            ProjetS4.compute(self.file, self.threshold, self.margin, self.boxWidth, self.color)
        else :
            self.printConsole("Error: No file selected.")

        self.cancel = False

        return



    def setImage(self,picture) : # This function updates the displayed image by replacing the old widget
        self.Oimage = ImageTk.PhotoImage(Image.open(picture).resize((700,500),Image.ANTIALIAS))
        self.Opic.destroy()
        self.Opic = Label(self,image=self.Oimage)
        self.Opic.grid(row=4,column=1,columnspan=3,padx=10)
        return



    def printConsole(self,text) : # This function allows to print console-like messages in a label, on the window
        self.console = self.console.split("<$>")
        l = len(self.console)
        if l > 30 : # We do not want the label to be too long, otherwise, it will change the dimensions of the whole window
            self.console = "<$>".join(self.console[l-1-30:])
        else :
            self.console = "<$>".join(self.console)

        self.console = self.console + str("<$> "+text+"\n")
        self.Oconsole.config(text=str(self.console))
        return


    def clean(self) :   # This cleans the console-like display
        self.Oconsole.destroy()
        self.console = ""
        self.Oconsole = Label(self,text=self.console,width=40,background=WIDGET_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.Oconsole.grid(row=4,column=4,sticky=N,columnspan=2,pady=5)
        return


    def switchToCancel(self) : # Switches the compute button to a cancel button
        self.Ocompute_button.destroy()
        self.Ocompute_button = Button(self, text="Cancel", command=self.canceling,background=WIDGET_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.Ocompute_button.grid(row=7,column=5,pady=2,padx=2)
        return


    def switchToCompute(self) : # Switches the cancel button to a compute button
        self.Ocompute_button.destroy()
        self.Ocompute_button = Button(self, text="Compute", command=self.compute,background=WIDGET_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.Ocompute_button.grid(row=7,column=5,pady=2,padx=2)
        return


    def canceling(self) : # Cancels the current calculation
        self.cancel = True
        return


    def setFrequency(self,frequency) : # Updates and displays the carrier signal's frequency
        self.frequency = str(frequency)
        self.Lfrequency.destroy()
        self.Lfrequency = Label(self,text="Carrier signal's frequency: "+self.frequency,background=FRAME_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.Lfrequency.grid(row=6,column=2,pady=5)
        return



def printOnConsole(text) : # Prints the text in the window
    interf.printConsole(str(text))
    return




def disp_pic(picture) : # Displays a picture in the window
    if os.path.exists(picture) :
        interf.setImage(picture)
        interf.update()
    else :
        printOnConsole("Fatal Error: Wrong Path.")
    return


def clean() : # Cleans the console in the window
    interf.clean()
    interf.update()
    return


def switchToCancel() : # Switches the compute button to a cancel button
    interf.switchToCancel()
    interf.update()
    return


def switchToCompute() : # Switches the cancel button to a compute button
    interf.switchToCompute()
    interf.update()
    return


def toCancel() : # Returns the cancel flag
    return interf.cancel


def updateFrequency(picture) : # Updates and displays the carrier signal's frequency
    f = picture.split("/")
    f = f[len(f)-1]
    f = f.split("_")
    if len(f) == 4 :
        interf.setFrequency(f[2])
    else :
        interf.setFrequency("XXXXHz")
        print("Unknowm name format - Error.\n")
    interf.update()
    return


def launchApp(picture) : # Launches the GUI

    window = Tk()
    #window.configure(background=FRAME_BACKGROUND)

    combostyle = Style() # We create a ttk style for all comboboxes
    combostyle.theme_create('combostyle', parent='alt',settings = {'TCombobox':{'configure':{'selectbackground': WIDGET_BACKGROUND,'fieldbackground': WIDGET_BACKGROUND,'background': WIDGET_BACKGROUND, 'selectforeground': WIDGET_FOREGROUND, 'fieldforeground': WIDGET_FOREGROUND,'foreground': WIDGET_FOREGROUND}}})
    combostyle.theme_use('combostyle') 

    window.title("ProjetS4 - 52 : Utilisation de réseaux neuronaux profonds pour l'analyse du spectre radio")

    global interf
    interf = Interface(window,picture)

    printOnConsole("Waiting for instructions...")

    interf.mainloop()
    return

