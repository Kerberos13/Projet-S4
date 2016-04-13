# -*- coding: utf-8 -*-

# The aim of this module is to offer a beautiful and convenient graphical user interface

import os
from tkinter import *
from PIL import Image, ImageTk
import ProjetS4
from tkinter.ttk import *



class Interface(Frame) :

    def __init__(self, window, **kwargs) :
        
        # Window Background
        Frame.__init__(self, window, width=768, height=576, **kwargs)
        self.pack(fill = BOTH)


        # Greetings message
        self.message = Label(self, text = "Welcome in Super Radio Spectre Analyser!")
        self.message.grid(row=1,column=2,pady=5)


        # Quit Button
        self.Oquit_button = Button(self, text="Quit", command=self.quit)
        self.Oquit_button.grid(row=7,column=5,pady=2,padx=2)


        # Compute Button
        self.Ocompute_button = Button(self, text="Compute", command=self.compute)
        self.Ocompute_button.grid(row=6,column=5,pady=2,padx=2)


        # Spectrogram Image
        self.Oimage = ImageTk.PhotoImage(Image.open("spectrograms/HF_3700_details2.jpg").resize((700,500),Image.ANTIALIAS))
        self.Opic = Label(self,image=self.Oimage)
        self.Opic.grid(row=4,column=2)
       

        # Threshold       
        self.threshold = 3
        self.Lthreshold = Label(self,text="Threshold")
        self.Lthreshold.grid(row=6,column=1,padx=2,sticky=S)
        self.Othreshold = Spinbox(self, from_=2, to=5, increment=0.5)
        self.Othreshold.grid(row=7,column=1,padx=2)


        # Margin
        self.margin = 12
        self.Lmargin = Label(self,text="Margin")
        self.Lmargin.grid(row=6,column=2,padx=2,sticky=S)
        self.Omargin = Spinbox(self, from_=5, to = 20, increment = 5)
        self.Omargin.grid(row=7,column=2,padx=2)


        # Box Width
        self.boxWidth = 6
        self.LboxWidth = Label(self,text="Box Width")
        self.LboxWidth.grid(row=6,column=3,padx=2,sticky=S)
        self.OboxWidth = Spinbox(self, from_=2, to=10, increment = 2)
        self.OboxWidth.grid(row=7, column=3,padx=2)


        # Box Color
        self.color = [120,120,250]
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




    def compute(self) :

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




    def setImage(self,picture) :

        """
        img2 = ImageTk.PhotoImage(Image.open(picture).resize((700,500),Image.ANTIALIAS))
        self.Oimage = img2
        self.Opic.configure(image = self.Oimage)
        self.Opic.update()
        #self.Opic.grid(row=2,column=2)
        """

        return


    def printConsole(self,text) :
        self.console = self.console.split("<$>")
        l = len(self.console)
        if l > 30 :
            self.console = "<$>".join(self.console[l-1-30:])
        else :
            self.console = "<$>".join(self.console)

        self.console = self.console + str("<$> "+text+"\n")
        self.Oconsole.config(text=str(self.console))
        return



def printOnConsole(text) :
    interf.printConsole(text)
    return




def disp_pic(picture) :

    interf.setImage(picture)
    interf.update()
    return





def launchApp(picture) :

    window = Tk()
    global interf
    interf = Interface(window)

    #tkimage = ImageTk.PhotoImage(Image.open(interface.image))
    #Label(interface, image=tkimage).pack(side=TOP)

    printOnConsole("Starting...")

    interf.mainloop()
    #interf.destroy()
    return


