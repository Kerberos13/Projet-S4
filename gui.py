# -*- coding: utf-8 -*-

# The aim of this module is to offer a beautiful and convenient graphical user interface

import os
from tkinter import *
from PIL import Image, ImageTk
import ProjetS4
from tkinter.ttk import *



class Interface(Frame) : # We define our window

    def __init__(self, window, **kwargs) :
        
        # Window Background
        Frame.__init__(self, window, width=768, height=576, **kwargs)
        self.pack(fill = BOTH)


        # Greetings message
        self.message = Label(self, text = "Welcome in Super Radio Spectre Analyser!")
        self.message.grid(row=1,column=2,pady=5)     # The grid method places a widget in the window; pady is a margin around the widget


        # Quit Button
        self.Oquit_button = Button(self, text="Quit", command=self.quit)  # command = self.quit defines the callback function
        self.Oquit_button.grid(row=7,column=5,pady=2,padx=2)   # padx is a margin around the widget


        # Compute Button
        self.Ocompute_button = Button(self, text="Compute", command=self.compute)
        self.Ocompute_button.grid(row=6,column=5,pady=2,padx=2)


        # Spectrogram Image
        self.Oimage = ImageTk.PhotoImage(Image.open("spectrograms/HF_3700_details2.jpg").resize((700,500),Image.ANTIALIAS)) # We use a label to display a picture
        self.Opic = Label(self,image=self.Oimage)
        self.Opic.grid(row=4,column=2)
       

        # Threshold       
        self.threshold = 3                                                 # In this, self.X is an attribute of the class, saving the current value
        self.Lthreshold = Label(self,text="Threshold")                     # self.Lx is the label of the corresponding object
        self.Lthreshold.grid(row=6,column=1,padx=2,sticky=S)
        self.Othreshold = Spinbox(self, from_=2, to=5, increment=0.5)      # self.Ox is the actual object
        self.Othreshold.grid(row=7,column=1,padx=2)


        # Margin
        self.margin = 12
        self.Lmargin = Label(self,text="Margin")
        self.Lmargin.grid(row=6,column=2,padx=2,sticky=S)   # Sticky allows to place a widget off-centered from its original position, according to the cardinal points
        self.Omargin = Spinbox(self, from_=5, to = 20, increment = 5)
        self.Omargin.grid(row=7,column=2,padx=2)


        # Box Width
        self.boxWidth = 6
        self.LboxWidth = Label(self,text="Box Width")
        self.LboxWidth.grid(row=6,column=3,padx=2,sticky=S)
        self.OboxWidth = Spinbox(self, from_=2, to=10, increment = 2)
        self.OboxWidth.grid(row=7, column=3,padx=2)


        # Box Color
        self.color = [120,120,250] # RGB
        self.Lcolor = Label(self, text="Box Color")
        self.Lcolor.grid(row=6, column=4,padx=2,sticky=S)
        self.Ocolor = Combobox(self)
        self.Ocolor.grid(row=7, column=4,padx=2)
        self.Ocolor['values'] = ["blue","purple","red","orange","yellow","green","white","black"]


        # Spectrogram
        self.file = "spectrograms/HF_3700_details2.jpg"
        self.Lfile = Label(self, text = "Select a file")
        self.Lfile.grid(row=2,column=4)
        self.Ofile = Combobox(self)
        self.Ofile.grid(row=3,column=4)
        self.Ofile['values'] = os.listdir("spectrograms/")


        # Console-like messages
        self.console = ""
        self.Oconsole = Label(self,text=self.console,width=40)
        self.Oconsole.grid(row=4,column=3,sticky=N,columnspan=2)

        return




    def compute(self) : # This function gets all parameters and launches the computation

        self.threshold = int(float(self.Othreshold.get()))
        self.margin = int(float(self.Omargin.get()))
        self.boxWidth = int(float(self.OboxWidth.get()))
        #self.color = int(float(self.Ocolor.get().split(",")))
        tmp = str(self.Ocolor.get())
        if tmp == "blue" :
            self.color = [120,120,250]
        elif tmp == "red" :
            self.color = [250,120,120]
        elif tmp == "green" :
            self.color = [120,250,120]
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
            self.color = [120,120,250]

        #self.file = str(self.Ofile.get())
        if len(str(self.Ofile.get())) != 0 :
            self.file = "spectrograms/"+str(self.Ofile.get())
        

        ProjetS4.compute(self.file, self.threshold, self.margin, self.boxWidth, self.color)

        return



    def setImage(self,picture) : # This function updates the displayed image by replacing the old widget
        self.Opic.destroy()
        self.Oimage = ImageTk.PhotoImage(Image.open(picture).resize((700,500),Image.ANTIALIAS))
        self.Opic = Label(self,image=self.Oimage)
        self.Opic.grid(row=4,column=2)
        return



    def printConsole(self,text) : # This function allows to print console-like messages in a label, on the window
        self.console = self.console.split("<$>")
        l = len(self.console)
        if l > 25 : # We do not want the label to be too long, otherwise, it will change the dimensions of the whole window
            self.console = "<$>".join(self.console[l-1-25:])
        else :
            self.console = "<$>".join(self.console)

        self.console = self.console + str("<$> "+text+"\n")
        self.Oconsole.config(text=str(self.console))
        return


    def clean(self) :   # This cleans the console-like display
        self.Oconsole.destroy()
        self.console = ""
        self.Oconsole = Label(self,text=self.console,width=40)
        self.Oconsole.grid(row=4,column=3,sticky=N,columnspan=2)
        return



def printOnConsole(text) : # Prints the text in the window
    interf.printConsole(text)
    return




def disp_pic(picture) : # Displays a picture in the window
    interf.setImage(picture)
    interf.update()
    return


def clean() : # Cleans the console in the window
    interf.clean()
    interf.update()
    return




def launchApp(picture) : # Launches the GUI

    window = Tk()
    global interf
    interf = Interface(window)

    #tkimage = ImageTk.PhotoImage(Image.open(interface.image))
    #Label(interface, image=tkimage).pack(side=TOP)

    printOnConsole("Waiting for instructions...")

    interf.mainloop()
    #interf.destroy()
    return


