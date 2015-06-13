import os
import matplotlib.pyplot as plt
os.chdir("C:\Users\Andy\Desktop\Sinc\Sinc\ComputerVisionTest")

from lineFinder2 import *

im = imread("C:\Temp\image.jpeg")
edge = imread("C:\Temp\Edge.png")
plt.clf()
lines = FindLines(edge, 50, 500, 20, 1)
#plt.subplot(121)
plt.imshow(im)
j = 1
for i in lines:
    
    plt.plot([i.endPoint1[1],i.endPoint2[1]],[i.endPoint1[0],i.endPoint2[0]], lw = 4, label = "line %d" %(j))
    j += 1
"""
plt.subplot(122)
plt.gray()
plt.imshow(edge)
"""
#for i in lines:
 #   plt.plot([i.endPoint1[1],i.endPoint2[1]],[i.endPoint1[0],i.endPoint2[0]], lw = 4)
plt.legend()
plt.show()
