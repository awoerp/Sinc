# Prints out the edges of an image give regular image and canny edge detection


from matplotlib.pyplot import imread, imshow, show
from numpy import copy
im = imread("C:\Temp\Test.jpeg")
edge = imread("C:\Temp\EdgeBlur.png")

im2 = copy(im)

x,y,z = im2.shape


class line:
    """
    Line object that contains a line within a specific image
    """
    
    def __init__(self):
        self.length
        self.endPoint1
        self.endPoint2
        self.midpoint
        self.baseImage
    

def Correlation(line):
    start = line[0]
    end   = line[-1]
    
    dy = end[0] - start[0]
    dx = end[1] - start[1]
    
    
    
    
    
    

def TestGrid(im,x,y):
"""
given a bitmap image and a true pixel, it searches for another true pixel
that is adjacent to it.  it then returns a bool determining if a true pixel
was found and an integer corresponding to that pixels position.
"""

    try:
        up    = im[y-1][x]
        down  = im[y+1][x]
        right = im[y][x+1]
        left  = im[y][x-1]
        
        upRight  = im[y-1][x+1]
        upLeft   = im[y-1][x-1]
        lowRight = im[y+1][x+1]
        lowLeft  = im[y+1][x-1]
        grid = [upLeft,up,upRight,left,0,right,lowLeft,down,lowRight]
        for index in range(len(grid)):
            if(grid[index] == 1):
                return True, index
        return False, -1
    except IndexError:
        return False, -1
   
                              
   
def TestPossibleLine(im,x,y,minLength):

    line = []
    pixelLength = 1
    flag = True
    while(flag):
    
        flag, index = TestGrid(im,x,y)
        if(flag):
            if(index == 2):
                line.append([y,x])
                pixelLength +=1
                im[y][x] = 2
                x = x + 1
                y = y - 1
                
            elif(index == 5):
                line.append([y,x])
                pixelLength +=1
                im[y][x] = 2
                x = x + 1
                
            elif(index == 8):
                line.append([y,x])
                pixelLength +=1
                im[y][x] = 2
                x = x + 1
                y = y + 1
                
            elif(index == 1):
                line.append([y,x])
                pixelLength +=1
                im[y][x] = 2
                y = y - 1
                
            elif(index == 7):
                line.append([y,x])
                pixelLength +=1
                im[y][x] = 2
                y = y + 1
                
            if(index == 0):
                line.append([y,x])
                pixelLength +=1
                im[y][x] = 2
                x = x - 1
                y = y - 1
                
            elif(index == 3):
                line.append([y,x])
                pixelLength +=1
                im[y][x] = 2
                x = x - 1
                
            elif(index == 6):
                line.append([y,x])
                pixelLength +=1
                im[y][x] = 2
                x = x - 1
    
    if(len(line) >= minLength and Correlation(line)):
        
        print(line)
        
        

def FindLines(im, minLength):
    """
    Input a canny edge detected image and the minimum length of a line in pixles
    0 = pixle is not a part of a line
    1 = pixle may be a part of a line
    2 = pixle is a part of the line undertest
    3 = pixle is a part of a line
    """
    
    y, x = im.shape
    for j in range(1,y-1):
        for i in range(1,x-1):
            if(im[j][i] == 1):
                im[j][i] = 2
                TestPossibleLine(im, j, i, 50)

 
 
FindLines(edge, 7)
