# -*- coding: utf-8 -*-

# The aim of this module is to bring together the python script and its GUI

import sys,os,time
sys.path.insert(0,'scripts/')

import sign_detect2,resize,reass
from tools import *

from threading import Thread
#from PIL import Image, ImageTk
import PIL.Image, PIL.ImageTk
from math import floor


# Python Version Compatibility Modes

if int(sys.version[0]) == 2 :
    print("Using Python2 compatibility mode - For a better experience, please try running Python3")
    from Tkinter import *
    from ttk import *
    from Tkinter import Button,Frame # We import those items from the tkinter module because they easily allow to change their style 

elif int(sys.version[0]) == 3 :
    from tkinter import *
    from tkinter.ttk import *
    from tkinter import Button,Frame # We import those items from the tkinter module because they easily allow to change their style 

else :
    print("Unsupported Python version: please try running Python2 or greater - Fatal Error")
    sys.exit()




# This is the actual Graphical User Interface

FRAME_BACKGROUND = "#2c2929" # "dark gray"
WIDGET_BACKGROUND = "#565252" # "medium gray"
WIDGET_FOREGROUND =  "#ffffff" # "white"



class Interface(Frame) : # We define our window

    def __init__(self, window, picture, **kwargs) :
 
    
        style = Style()
        style.map('TCombobox', background=[('readonly',WIDGET_BACKGROUND)])


        # Window Background
        Frame.__init__(self, window, width=800, height=600, **kwargs)#,background=FRAME_BACKGROUND)
        self.pack(fill = BOTH, expand = YES)


        """
        # Greetings message
        self.message = Label(self, text = "Welcome in Super Radio Spectre Analyser!",background=FRAME_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.message.grid(row=1,column=2,pady=5,sticky=N+E+W)     # The grid method places a widget in the window; pady is a margin around the widget
        """

        # Quit Button
        self.Oquit_button = Button(self, text="Quit", command=self.quit_app, background=WIDGET_BACKGROUND, foreground=WIDGET_FOREGROUND)  # command = self.quit defines the callback function
        self.Oquit_button.grid(row=8,column=5,pady=2,padx=2,sticky=N+E+W)   # padx is a margin around the widget and weight is a resizing coefficient
        self.quitting = False


        # Compute Button
        self.Ocompute_button = Button(self, text="Compute", command=self.compute, background=WIDGET_BACKGROUND, foreground=WIDGET_FOREGROUND)
        self.Ocompute_button.grid(row=7,column=5,pady=2,padx=2,sticky=N+E+W)


        # Cancel flag
        self.cancel = mutex(False)


        # Spectrogram Image
        if os.path.exists(picture) :
            self.imagePath = str(picture)
        else :
            self.imagePath = "default.png"
        self.image_original = PIL.Image.open(self.imagePath)
        self.image_copy = self.image_original.copy()
        self.Oimage = PIL.ImageTk.PhotoImage(self.image_copy) # We use a label to display a picture
        self.Opic = Label(self,image=self.Oimage)
        self.Opic.grid(row=3,column=1,columnspan=3, rowspan=3, padx=10,sticky=N+W+S)
        self.Opic.bind('<Configure>',self.resize)
        self.resizeable = False # Security to avoid the resize function to get out of control
      

        # Carrier Signal Frequency
        self.frequency = "XXXXHz"
        self.Lfrequency = Label(self,text="Carrier signal's frequency: "+self.frequency,background=FRAME_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.Lfrequency.grid(row=6, column=2,pady=5,sticky=N+E+W)


        # Threshold       
        self.threshold = 3                                                 # In this, self.X is an attribute of the class, saving the current value
        self.Lthreshold = Label(self,text="Threshold",background=FRAME_BACKGROUND,foreground=WIDGET_FOREGROUND)                     # self.Lx is the label of the corresponding object
        self.Lthreshold.grid(row=7,column=1,padx=2,sticky=S+E+W)
        self.Othreshold = Spinbox(self, from_=2, to=6, increment=1, background=WIDGET_BACKGROUND, foreground=WIDGET_FOREGROUND)    # self.Ox is the actual object
        self.Othreshold.grid(row=8,column=1,padx=2,sticky=N+E+W)


        # Margin
        self.margin = 12
        self.Lmargin = Label(self,text="Margin",background=FRAME_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.Lmargin.grid(row=7,column=2,padx=2,sticky=S+E+W)   # Sticky allows to place a widget off-centered from its original position, according to the cardinal points
        self.Omargin = Spinbox(self, from_=10, to = 25, increment = 5, background=WIDGET_BACKGROUND, foreground=WIDGET_FOREGROUND)
        self.Omargin.grid(row=8,column=2,padx=2,sticky=N+E+W)


        # Box Width
        self.boxWidth = 6
        self.LboxWidth = Label(self,text="Box Width",background=FRAME_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.LboxWidth.grid(row=7,column=3,padx=2,sticky=S+E+W)
        self.OboxWidth = Spinbox(self, from_=4, to=10, increment = 2, background=WIDGET_BACKGROUND, foreground=WIDGET_FOREGROUND)
        self.OboxWidth.grid(row=8, column=3, padx=2, sticky=W+N+E)


        # Box Color
        self.color = [250,250,250] # RGB
        self.Lcolor = Label(self, text="Box Color",background=FRAME_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.Lcolor.grid(row=7, column=4,padx=2,sticky=W+S+E)
        self.Ocolor = Combobox(self, background=WIDGET_BACKGROUND, foreground=WIDGET_FOREGROUND)
        self.Ocolor.grid(row=8, column=4,padx=2,sticky=N+E+W)
        self.Ocolor['values'] = ["blue","purple","red","orange","yellow","green","white","black"]


        # Spectrogram
        self.file = "spectrograms/HF_3700_details2.jpg"
        self.Lfile = Label(self, text = "Select a file",background=FRAME_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.Lfile.grid(row=2,column=4,sticky=N+E+W)
        self.Ofile = Combobox(self, background=WIDGET_BACKGROUND, foreground=WIDGET_FOREGROUND)
        self.Ofile.grid(row=3,column=4,sticky=N+E+W)
        self.Ofile['values'] = os.listdir("spectrograms/")


        # Console-like messages
        self.console = ""
        self.Oconsole = Label(self,text=self.console, background=WIDGET_BACKGROUND, foreground=WIDGET_FOREGROUND)
        self.Oconsole.grid(row=4,column=4,sticky=N+E+W+S,columnspan=2,pady=5,padx=5)


        # Resizing column coefficients
        self.columnconfigure(1,weight=1,pad=10)
        self.columnconfigure(2,weight=1,pad=10)
        self.columnconfigure(3,weight=1,pad=10)
        self.columnconfigure(4,weight=3,pad=10)
        self.columnconfigure(5,weight=3,pad=10)


        # Resizing row coefficients
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.rowconfigure(3,weight=1)
        self.rowconfigure(4,weight=1)
        self.rowconfigure(5,weight=1)
        self.rowconfigure(6,weight=1)
        self.rowconfigure(7,weight=1)
        self.rowconfigure(8,weight=1)
        
        return


    def quit_app(self) :
        self.quitting = True
        self.quit()
        return

    
    def resize(self,event) : # This functions dynamically resizes the displayed picture
        
        #print(event.width,self.Opic.winfo_width(),self.image_original.size)

        if self.resizeable :
            r = self.image_copy.size
            #print(self.image_original.size)
            r = r[0]/r[1]
            height = int(event.height - 4)
            width = int(floor(height*r) -4) # New widget's dimensions
           
            self.image_original = self.image_copy.resize((width, height),PIL.Image.ANTIALIAS)
            self.Oimage = PIL.ImageTk.PhotoImage(self.image_original)
            self.Opic.configure(image = self.Oimage)
        else :
            self.resizeable = True

        self.update()

        return




    def compute(self) : # This function gets all parameters and launches the computation

        self.cancel.set(False)

        self.threshold = int(float(self.Othreshold.get()))
        self.margin = int(float(self.Omargin.get()))
        self.boxWidth = int(float(self.OboxWidth.get()))
        tmp = str(self.Ocolor.get())
        if tmp == "blue" :
            self.color = [15,65,220]
        elif tmp == "red" :
            self.color = [180,0,0]
        elif tmp == "green" :
            self.color = [35,200,10]
        elif tmp == "yellow" :
            self.color = [245,245,20]
        elif tmp == "orange" :
            self.color = [250,130,10]
        elif tmp == "purple" :
            self.color = [225,10,160]
        elif tmp == "white" :
            self.color = [250,250,250]
        elif tmp == "black" :
            self.color = [5,5,5]
        else :
            self.color = [250,250,250] # Default color is white

        if len(str(self.Ofile.get())) != 0 :
            self.file = "spectrograms/"+str(self.Ofile.get())
            #ProjetS4.compute(self.file, self.threshold, self.margin, self.boxWidth, self.color)


            ##/////////////////////##
            ### START OF THE MAIN ###
            ##\\\\\\\\\\\\\\\\\\\\\##


            self.setImage(str(self.file))
            self.setFrequency(str(self.file))

            if not self.cancel.get() :
                self.printOnConsole("Opening "+str(self.file)+"...")
                self.printOnConsole("Detecting signals...")
                files = sign_detect2.main(str(self.file),self.margin,self.threshold,True) # Detection of signals on the spectrogram
                self.printOnConsole("Done.")
            else :
                self.printOnConsole("Fatal Error: Aborting Signal detection")

            signals = list()
            for elt in files :
                if (elt[len(elt)-10:] == "signal.bmp" and os.path.exists(elt)) :
                    signals.append(elt)
            if len(signals) == 0 :
                self.printOnConsole("Error: No signal detected")
            else :

                W = 50 # Dimension of the ANN along the horizontal axis (wide)
                H = 37 # Dimension of the ANN along the vertical axis (height)
                
                #CNN_input = numpy.ndarray()
                
                for elt in signals :
                    if not self.cancel.get() :
                        self.printOnConsole("Optimizing signals...")
                        windows = resize.main(elt,W,H) # Resizing of detected signals
                        self.printOnConsole("Done.")
                    else :
                        self.printOnConsole("Fatal Error: Aborting Signal optimisation")

                    # CNN_input is a numpy.ndarray object caonting float32 dtype numbers.
                    # Each row corresponds to an image of which rows have been concatenated in order to form one long vector - in this case of 50x37 columns
                    """
                    v,h = windows.shape[0],windows.shape[1]
                    tmp = numpy.ndarray()
                    for i in range(0,v) :
                        tmp = numpy.hstack((tmp,windows(i,0:h)))
                          
                    CNN_input = numpy.vstack((CNN_input,tmp))
                    """
               
                """
                if not self.cancel.get() :
                    self.printOnConsole("Analysing signals...")
                    labels = ann.main(CNN_input) # Classification of detected signals
                    self.printOnConsole("Done.")
                else :
                    self.printOnConsole("Fatal Error: Aborting Signal classification",True)
                """

                if not self.cancel.get() :
                    self.printOnConsole("Merging files...")
                    reass.main(list(),self.margin,self.boxWidth,self.color,True) # Reassembly of the different parts for a labeled spectrogram
                    self.printOnConsole("Done.")
                    self.setImage("tmp/spectrogram.jpg")
                else :
                    printOnConsole("Fatal Error: Aborting Reassembly")


            ##///////////////////##
            ### END OF THE MAIN ###
            ##\\\\\\\\\\\\\\\\\\\##

        else :
            self.printOnConsole("Error: No file selected.")

        return



    def setImage(self,picture) : # This function updates the displayed image by replacing the old widget
        """
        self.Oimage = ImageTk.PhotoImage(Image.open(picture).resize((700,500),Image.ANTIALIAS))
        self.Opic.destroy()
        self.Opic = Label(self,image=self.Oimage)
        self.Opic.grid(row=4,column=1,columnspan=3,padx=10)
        """
        if os.path.exists(picture) :
            self.imagePath = picture
            self.image_original = PIL.Image.open(self.imagePath)
            self.image_copy = self.image_original.copy()
            self.image_copy = self.image_copy.resize((int(self.Opic.winfo_width()-4), int(self.Opic.winfo_height())-4),PIL.Image.ANTIALIAS)
            self.Oimage = PIL.ImageTk.PhotoImage(self.image_copy) # We use a label to display a picture
            self.Opic.destroy()
            self.resizeable = False # Security to avoid the resize function to get out of control
            self.Opic = Label(self,image=self.Oimage)
            self.Opic.grid(row=4,column=1,columnspan=3, padx=10,sticky=N+W+S)
            self.Opic.bind('<Configure>',self.resize)
            self.update()
        else :
            self.printOnConsole("Fatal Error: Wrong Path.")
        return



    def printOnConsole(self,text) : # This function allows to print console-like messages in a label, on the window
        self.console = self.console.split("\n")
        l = len(self.console)
        txt = str()
        text = str(text)

        W = int(self.Oconsole.winfo_width())
        H = int(self.Oconsole.winfo_height())

        if H==1 :
            H=30
        else :
            H-=4
            H = int(floor(H/15))
        if W==1 :
            W=30
        else :
            W-=4
            W = int(floor(W/7))

        L = len(text)

        i = 0
        while i*W < L :
            i+=1
            txt+=text[(i-1)*W:min(i*W,L)]+"\n"


        if l > H : # We do not want the label to be too long, otherwise, it will change the dimensions of the whole window
            self.console = "\n".join(self.console[l-1-30:])
        else :
            self.console = "\n".join(self.console)

        self.console = self.console + str("<$> "+txt+"\n")
        self.Oconsole.config(text=str(self.console))
        self.update()
        return


    
    def clean(self) :   # This cleans the console-like display
        self.Oconsole.destroy()
        self.console = ""
        self.Oconsole = Label(self,text=self.console,background=WIDGET_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.Oconsole.grid(row=4,column=4,sticky=N+E+W+S,columnspan=2,pady=5,padx=5)
        self.printOnConsole("\n"*50)
        return


    
    def switchToCancel(self) : # Switches the compute button to a cancel button
        self.Ocompute_button.destroy()
        self.Ocompute_button = Button(self, text="Cancel", command=self.canceling,background=WIDGET_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.Ocompute_button.grid(row=7,column=5,pady=2,padx=2,sticky=N+E+W)
        return



    def switchToCompute(self) : # Switches the cancel button to a compute button
        self.Ocompute_button.destroy()
        self.Ocompute_button = Button(self, text="Compute", command=self.compute,background=WIDGET_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.Ocompute_button.grid(row=7,column=5,pady=2,padx=2,sticky=N+E+W)
        return



    def canceling(self) : # Cancels the current calculation
        self.cancel.set(True)
        return



    def setFrequency(self,picturePath) : # Updates and displays the carrier signal's frequency
        f = picturePath.split("/")
        f = f[len(f)-1]
        f = f.split("_")
        if len(f) == 4 :
            frequency = f[2]
        else :
            frequency = "XXXXHz"
            self.printOnConsole("Error: Unknowm name format.")
        self.frequency = str(frequency)
        self.Lfrequency.destroy()
        self.Lfrequency = Label(self,text="Carrier signal's frequency: "+self.frequency,background=FRAME_BACKGROUND,foreground=WIDGET_FOREGROUND)
        self.Lfrequency.grid(row=6,column=2,pady=5,sticky=N+E+W)
        self.update()
        return





pic = "default.png"

# GUI initialization

window = Tk()

combostyle = Style() # We create a ttk style for all comboboxes
combostyle.theme_create('combostyle', parent='alt',settings = {'TCombobox':{'configure':{'selectbackground': WIDGET_BACKGROUND,'fieldbackground': WIDGET_BACKGROUND,'background': WIDGET_BACKGROUND, 'selectforeground': WIDGET_FOREGROUND, 'fieldforeground': WIDGET_FOREGROUND,'foreground': WIDGET_FOREGROUND}}})
combostyle.theme_use('combostyle') 

window.title("ProjetS4 - 52 : Utilisation de réseaux neuronaux profonds pour l'analyse du spectre radio")
window.option_add("*background",FRAME_BACKGROUND)

interface = Interface(window,pic)
interface.clean()
interface.printOnConsole("Waiting for instructions...")


# Initialization and launching of the threads

interface.mainloop()




