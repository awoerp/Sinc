import numpy as np

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
        masterSlope = float(dy)/float(dx)
    except ZeroDivisionError:
        masterSlope = dy / length
    
    segmentLength = length / resolution
    
    segments = []
    
    startPoint = start
    for i in range(1, resolution + 1):
        endPoint = line[segmentLength * i]
        segments.append([startPoint, endPoint])
        startPoint = endPoint
    
    segmentSlopes = []
    
    for i in segments:
        start = i[0]
        end   = i[1]
        dy = end[0] - start[0]
        dx = end[1] - start[1]
        try:
            slope = dy/float(dx)
        except ZeroDivisionError:
            slope = (dy * resolution / length)
        segmentSlopes.append(slope)
     
    ave = np.average(segmentSlopes)   
    
    if(ave < (masterSlope + threshold) and ave > (masterSlope - threshold)):

        return True
        





