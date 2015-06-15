import os
import matplotlib.pyplot as plt
os.chdir("C:\Users\Andy\Desktop\Sinc\Sinc\ComputerVisionTest")

from lineFinder2 import *

im = imread("C:\Temp\Room.jpeg")
edge = imread("C:\Temp\RoomEdge.png")
plt.clf()
lines = FindLines(edge, 15, 1000, 10, 1)
#plt.subplot(121)
plt.title("Image 2 With Straight Line Recognition")
plt.imshow(im)
plt.axis('off')
j = 1
for i in lines:
    
    plt.plot([i.endPoint1[1],i.endPoint2[1]],[i.endPoint1[0],i.endPoint2[0]], '--',lw = 4, label = "line %d" %(j))
    j += 1
"""
plt.subplot(122)
plt.gray()
plt.imshow(im)

plt.title("Original Image")
#plt.legend()
plt.axis('off')
"""
plt.show()
