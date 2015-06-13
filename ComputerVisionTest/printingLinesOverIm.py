import os
import matplotlib.pyplot as plt
os.chdir("C:\Users\Andy\Desktop\Sinc\Sinc\ComputerVisionTest")

from lineFinder2 import *

im = imread("C:\Temp\Test.jpeg")
edge = imread("C:\Temp\EdgeBlur3.png")
plt.clf()
lines = FindLines(edge, 25, 120, 20, 10)
plt.subplot(121)
plt.imshow(im)

for i in lines:
    plt.plot([i.endPoint1[1],i.endPoint2[1]],[i.endPoint1[0],i.endPoint2[0]], lw = 4)

plt.subplot(122)
plt.gray()
plt.imshow(edge)
#for i in lines:
 #   plt.plot([i.endPoint1[1],i.endPoint2[1]],[i.endPoint1[0],i.endPoint2[0]], lw = 4)

plt.show()
