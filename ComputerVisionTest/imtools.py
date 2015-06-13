""" Tools that will help with image analysis """

import os
from PIL import Image
from numpy import *
from scipy.ndimage import filters
import matplotlib.pyplot as plt


def GetImList(path,fileType = '.jpg'):
    """ Returns a list of filenames for all files of a specific file
        type in the directory
    """
    
    return [os.path.join(path,f) for f in os.linstdir(path)
            if f.endswith(fileType)]
      
                  
def ImResize(im, size):
    """
    Resizes an image array using PIL
    """
    IM = Image.fromarray(uint8(im))
    return array(IM.resize(size))
    
    
def HistEqualize(im, numBins = 256):
    """
    Histogram equalization of a grayscale image.
    """
    # get image histogram
    
    imHist, bins = histogram(im.flatten(),numBins,normed = True)
    cdf = imHist.cumsum() # cumulative distribution function
    cdf = 255 * cdf / cdf[-1] # normalize
    
    # use linear interpolation of cdf to find new pixel values
    
    im2 = interp(im.flatten(),bins[:-1],cdf)
    
    return im2.reshape(im.shape), cdf
    
    
def ComputeAverage(imList):
    """
    Computes the average of a list of images.
    """
    
    # open fist image and make into an array of floats
    
    averageIm = array(Image.open(imList[0]),'f')
    
    for imname in imList[1:]:
        try:
            averageIm += array(Image.open(imname))
        except:
            print(imname + "...skipped")
        averageIm /= len(imList)
        
    # return average as unit8
    
    return array(averageIm, 'uint8')
    
def pca(X):
    """
    Principal Component Analysis
    Input:  X, a matrix with training data stored as flattened arrays in rows
    Return: projection matrix (with important dimensions first),
            variance and mean
    """
    
     # get dimensions
    numData,dim = X.shape()
     
    # Center Data
    meanX = X.mean(axis = 0)
    X = X - meanX
     
    if dim > numData:
        #PCA - compact trick used
        M = dot(X,X.T) #convariance matrix
        e, EV = linalg.eigh(M) #EigenValues and EigenVectors
        tmp = dot(X.T,EV).T # This is the compact trick
        V = tmp[::-1]
        S = sqrt(e)[::-1]
        for i in range(V.shape[1]):
            V[:,i] /= S
    else:
        #PCA - Singular value decomposition (SVD) used
        U, S, V = linalg.svd(X)
        V = V[:numData] # only makes sense to return the first numData
        
    # Return projection matrix, the variance, and the mean
    return V, S, meanX
     
     
def denoise(im, U_init, tolerance = 0.1, tau = 0.125, tv_weight = 100):
    """
    An implementation of the Rudin-Oshre-Fatemi (ROF) denoising model
    using numerical procedure presented in eq (11) p. 23
    
    Input:  noisy input image (greyscale), initial guess for U, weight
            weight of the TC-regularizing term, steplength, tolerance
            for stop criterion.
           
    Output: denoised and detextured image, texture residual.
    """
    
    m,n = im.shape # size of noisy image
    
    # initialize
    U  = U_init
    Px = im # x-component to the dual field
    Py = im # y-component to the dual field
    error = 1
    
    while (error > tolerance):
        Uold = U
        
        #gradient of primal variable
        GradUx = roll(U,-1,axis = 1) - U # x-component of U's gradient
        GradUy = roll(U,-1,axis = 0) - U # y-component of U's gradient
        
        #update the dual variable
        PxNew = Px + (tau / tv_weight) * GradUx
        PyNew = Py + (tau / tv_weight) * GradUy
        NormNew = maximum(1,sqrt(PxNew**2 + PyNew**2))
        
        Px = PxNew / NormNew
        Py = PyNew / NormNew
        
        # update primal variable
        
        RxPx = roll(Px,1,axis = 1)
        RyPy = roll(Py,1,axis = 0)
        
        DivP = (Px - RxPx) + (Py - RyPy)
        
        U = im + tv_weight * DivP
        
        error = linalg.norm(U - Uold) / sqrt(n*m)    
    
        return U, im - U
    
    
def compute_harris_response(im, sigma = 3):
    """
    Compute the Harris corner detector response function for each pixel in
    a greylevel image
    """
    
    #derivatives
    imx = zeros(im.shape)
    filters.gaussian_filter(im, (sigma, sigma), (0,1), imx)
    
    imy = zeros(im.shape)
    filters.gaussian_filter(im, (sigma, sigma), (1,0), imy)    
    
    #compute components of the Harris matrix
    Wxx = filters.gaussian_filter(imx*imx, sigma)
    Wxy = filters.gaussian_filter(imx*imy, sigma)
    Wyy = filters.gaussian_filter(imy*imy, sigma)
    
    #determinant and trace
    Wdet = Wxx * Wyy - Wxy**2
    Wtr = Wxx + Wyy
    
    return Wdet / Wtr
    
def get_harris_points(harrisim, min_dist = 10, threshold = 0.1):
    """
    Return corners from a Harris response image
    min_dist is the minimum number of pixels separating
    corners and image boundary.
    """
    
    #find top corner candidates above a threshold
    corner_threshold = harrisim.max() * threshold
    harrisim_t = (harrisim > corner_threshold) * 1
    
    #get coordinates of candidates
    coords = array(harrisim_t.nonzero()).T
    
    #... and their values
    candidate_values = [harrisim[c[0],c[1]] for c in coords]
    
    #sort candidates
    index = argsort(candidate_values)
    
    #store allowed point location in array
    allowed_locations = zeros(harrisim.shape)
    allowed_locations[min_dist:-min_dist,min_dist:-min_dist] = 1
    
    #select the best poins taking min_distance into account
    filtered_coords = []
    for i in index:
        if allowed_locations[coords[i,0],coords[i,1]] == 1:
            filtered_coords.append(coords[i])
            allowed_locations[(coords[i,0]-min_dist):(coords[i,0]+min_dist),
                (coords[i,1]-min_dist):(coords[i,1]+min_dist)] = 0
    
    return filtered_coords
    
def plot_harris_points(image,filtered_coords):
    """
    Plots corner found in image.
    """
    plt.clf()
    plt.figure()
    plt.gray()
    plt.imshow(image)
    plt.plot([p[1] for p in filtered_coords],[p[0] for p in filtered_coords],'*')
    plt.axis('off')
    plt.show()
    
    
def PlotInstPoints(im,sigma = 3, min_dist = 10, threshold = 0.1):
    harrisim = compute_harris_response(im,sigma)
    points   = get_harris_points(harrisim, min_dist, threshold)
    plt.clf()
    plt.gray()
    plt.imshow(im)
    plt.plot([p[1] for p in points],[p[0] for p in points],'*')
    plt.axis('off')
    plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    