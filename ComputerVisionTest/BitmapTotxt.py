from matplotlib.pyplot import imread, imshow, show
from numpy import copy

def PrintToTxt(im, location):
    y,x = im.shape
    x = int(x)
    y = int(y)
    
    f = open(location, "w")
    
    f.write(str(x) + ' ' + str(y) + '\n')
    
    for j in range(y):
        for i in range(x):
            f.write(str(int(im[j][i])))
        f.write('\n')
    
    
    f.close()