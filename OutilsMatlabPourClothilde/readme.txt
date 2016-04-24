these scripts are used to generate signal with  a file '.data'.

all in one
lectureClothilde.m :
you should give the address of file '.data' to this script.
Output is located in current matlab workspce.
Output name is the name of the file '.data'.


we generate two outputs: one with axis, another without axis.

the one with axis "A" is for further signal processing( denoising, zooming..)
the one without axis "B" is for the reference of frequence information, because we need to
seperate each signal et zoom them according to the fixed scale 
( that is to say : 
 (1) we need to decide a scale for pixel and frequence (1 prequence = ? pixels)
 (2)  By watching "A" and  "B", for example, by looking "A", we get band width is 3.5*10^4 Hz
        and from "B", we know the width of image is 4800 pixel.  we can calculate that the scale now is 7.292 Hz/pixel
 (3)we need to zoom this scale to our scale fixed in (1)
)



PS: we can see that evan the central frequence changes( 3700kHz, 6500kHz...) We have the same ban width (0- 3.5*10^4 )
That is because that these signals are already moved to low frequence ("translater par la fr¨¦qence porteuse" in french)