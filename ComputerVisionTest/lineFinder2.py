from matplotlib.pyplot import imread, show
from numpy import copy, average, sqrt, arctan
import os

edge = imread("C:\Temp\Edge2.png")


class lineObject:
    """
    Line object that contains a line within a specific image
    """
       
    def __init__(self, line):
        self.length = len(line)
        self.endPoint1 = line[0]
        self.endPoint2 = line[-1]
        self.midpoint = [abs(self.endPoint1[0] - self.endPoint2[0]) / 2,
                         abs(self.endPoint1[1] - self.endPoint2[1]) / 2]
    

def Correlation(line, resolution, threshold):
    """
    Given an array of adjacent pixel locations, it will determine
    if the line is straight enought to be considered a line.
    it uses the two endpoints to create the line to which its
    correlation is measured. The line is split into 'resolution'
    lines whose slopes are then compared to the ideal line.
    'threshold' is the variability allowed in the difference
    between these slopes
    """
    
    start = line[0]
    end   = line[-1]
    length = len(line)
    dy = end[0] - start[0]
    dx = end[1] - start[1]
    try:
        masterAngle = arctan(abs(dy/dx))
        if (dy/dx < 0 or (dy < 0 and dx < 0)):
            masterAngle += 3.1415  # pi or 180 degrees
    except ZeroDivisionError:
        if dy > 0:
            masterAngle = 1.57 # 90deg in radians
        else:
            masterAngle = -1.57
        
    
    segmentLength = length / resolution
    
    segments = []
    
    startPoint = start
    for i in range(1, resolution + 1):
        endPoint = line[segmentLength * i - 1]
        segments.append([startPoint, endPoint])
        startPoint = endPoint
    
    segmentSlopes = []
    
    for i in segments:
        start = i[0]
        end   = i[1]
        dy = end[0] - start[0]
        dx = end[1] - start[1]
        try:
            angle = arctan(abs(dy/dx))
            if (dy/dx < 0 or (dy < 0 and dx < 0)):
                angle += 3.1415  # pi or 180 degrees       
        except ZeroDivisionError:
            if dy > 0:
                angle = 1.57 # 90deg in radians
            else:
                angle = -1.57

        segmentSlopes.append(angle)
     
    ave = average(segmentSlopes)
    
    
    if(ave < (masterAngle + threshold) and ave > (masterAngle - threshold)):

        return True
    
    else:
        return False
    
    

def TestGrid(im,x,y):
    """
    given a bitmap image and a true pixel, it searches for another true pixel
    that is adjacent to it.  It then returns a bool telling if a true pixel
    was found and an integer corresponding to that pixel's position.
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
   
                              
   
def TestPossibleLine(im,y,x,minLength, maxLength, resolution, threshold):
    """
    given a bitmap image and a true pixel, it will iterativly call
    TestGrid to find the next pixel in a possible line until TestGrid
    returns false.  It then check to see if the line is long enough
    and whether it is straight enough using the correlation function.
    Additionally, it ensures it is only adding straight points to
    "linePoints" by checking the mostcommon direction index ( retruned
    after calling TestGrid) against the most common direction index of
    the previous numIndexVals number of points.  This mitigates against
    a problem where the lines would follow doglegs.
    """
    numIndexVals = 4
    linePoints = []
    flag, index = TestGrid(im,x,y)
    totalIndex = []
    lastIndex = []
    for i in range(numIndexVals):
        lastIndex.append(0)
    count = 0
    while(flag):
        count += 1
        if(flag):
            if(index == 2):
                linePoints.append([y,x])
                im[y][x] = 2
                x = x + 1
                y = y - 1
                
            elif(index == 5):
                linePoints.append([y,x])
                im[y][x] = 2
                x = x + 1
                
            elif(index == 8):
                linePoints.append([y,x])
                im[y][x] = 2
                x = x + 1
                y = y + 1
                
            elif(index == 1):
                linePoints.append([y,x])
                im[y][x] = 2
                y = y - 1
                
            elif(index == 7):
                linePoints.append([y,x])
                im[y][x] = 2
                y = y + 1
                
            if(index == 0):
                linePoints.append([y,x])
                im[y][x] = 2
                x = x - 1
                y = y - 1
                
            elif(index == 3):
                linePoints.append([y,x])
                im[y][x] = 2
                x = x - 1
                
            elif(index == 6):
                linePoints.append([y,x])
                im[y][x] = 2
                x = x - 1
                
            totalIndex.append(index)
            lastIndex.insert(0,index)
            lastIndex.pop()
            flag, index = TestGrid(im,x,y)
            if count % 5 == 0:    
                mostCommonTotal = max(set(totalIndex), key=totalIndex.count)
                mostCommonLast = max(set(lastIndex), key=lastIndex.count)
                if mostCommonTotal != mostCommonLast:
                    flag = False
                    for i in range(numIndexVals):
                        linePoints.pop()
            
            
            
        
    if(len(linePoints) != 0):    
        lineLength = sqrt((linePoints[0][0] - linePoints[-1][0])**2 + (linePoints[0][1] - linePoints[-1][1])**2)
        if(lineLength >= minLength and lineLength <= maxLength and Correlation(linePoints,resolution,threshold)):
            for i in linePoints:
                im[i[0]][i[1]] = 3
            return lineObject(linePoints), im
        
    return "notLine", im
        
        

def FindLines(im, minLength, maxLength, resolution, threshold):
    """
    Input a canny edge detected image and the minimum length of a line in pixles
    0 = pixle is not a part of a line
    1 = pixle may be a part of a line
    2 = pixle is a part of the line undertest
    """
    
    lines = [] # array of line objects
    y, x = im.shape
    for j in range(1,y-1):
        for i in range(1,x-1):
            if(im[j][i] == 1):
                im[j][i] = 4
                line,im = TestPossibleLine(im, j, i, minLength, maxLength, resolution, threshold)
                if (line != "notLine"):
                    lines.append(line)
                    
    return lines
    
#lines = FindLines(edge, 50, 500, 20, 2)
    