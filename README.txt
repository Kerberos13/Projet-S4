            #-#-#    R E A D   M E   #-#-#


In order to launch the software, two options are currently available. You can either run it directly in a console by typing
"python main.py <file_path>" where <file_path> is the relative path to the spectrogram, or run it via the Graphical User
Interface by typing "python ProjetS4.py".

It is expected that your spectrogram is in the folder "spectrograms/". Splitted images of signals and final analyzed spectrogram
are available in the "tmp/" folder depending on the stage of the calculation.


Python is highly sensitive to indentation. Current files are written with an indentation of four spaces. If you happen to modify
something in one or several of those files, please respect this indentation system or it will not compile.

This software has some dependencies and needs several items to be installed in order to work: Python 3 (a compatibility mode is
integrated for Python2 though), numpy, PIL.

The GUI runs on tkinter, which comes by default with Python.


The software has several modules. Basically, the main module starts by calling the sign_detect2 module in order to detect 
signals. After that, it calls the resize module to generate matrixes directly usable by the ANN. Finally, it will call the reass
module that will reassemble the complete spectrogram. If the GUI is used, then the ProjetS4 module will display the GUI and proceed
similarly to the main module. Almost all modules have some functions in common that are in the tools module.


Contact: s4-projet-52-2016@mlistes.telecom-bretagne.eu

