from matplotlib.pyplot import imread, imshow, show
from numpy import copy
im = imread("C:\Temp\Test.jpeg")
edge = imread("C:\Temp\EdgeBlur.png")

y,x = edge.shape
x = int(x)
y = int(y)

f = open("C:\Temp\edge.txt", "w")

f.write(str(x) + ' ' + str(y) + '\n')

for j in range(y):
    for i in range(x):
        f.write(str(int(edge[j][i])))
    f.write('\n')


f.close()