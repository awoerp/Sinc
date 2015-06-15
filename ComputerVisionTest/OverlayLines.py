import os
import matplotlib.pyplot as plt
os.chdir("C:\Users\Andy\Desktop\Sinc\Sinc\ComputerVisionTest")

from lineFinder2 import *
plt.close("all")
im1 = imread("C:\Temp\Photos\Im1.jpeg")
edge1 = imread("C:\Temp\Photos\Im1Corner1.png")

im2 = imread("C:\Temp\Photos\Im2.jpeg")
edge2 = imread("C:\Temp\Photos\Im1Corner2.png")

minLength = 15
maxLength = 1000
resolution = 10
threshold = 1



lines1 = FindLines(edge1, minLength, maxLength, resolution, threshold)
lines2 = FindLines(edge2, minLength, maxLength, resolution, threshold)

#plt.figure()
plt.subplot(131)
plt.imshow(im1)
plt.axis('off')
for i in lines1:
    
    plt.plot([i.endPoint1[1],i.endPoint2[1]],[i.endPoint1[0],i.endPoint2[0]],lw = 4)
    
#plt.figure()
plt.subplot(132)
plt.imshow(im2)
plt.axis('off')
for i in lines2:
    
    plt.plot([i.endPoint1[1],i.endPoint2[1]],[i.endPoint1[0],i.endPoint2[0]],'--',lw = 4)
    
#plt.figure()
plt.subplot(133)
plt.imshow(im1)
plt.axis('off')
for i in lines1:
    
    plt.plot([i.endPoint1[1],i.endPoint2[1]],[i.endPoint1[0],i.endPoint2[0]],lw = 4)
    
for i in lines2:
    
    plt.plot([i.endPoint1[1],i.endPoint2[1]],[i.endPoint1[0],i.endPoint2[0]],'--',lw = 4)

plt.show()
