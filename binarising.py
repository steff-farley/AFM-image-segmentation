#!/usr/bin/env python
#coding=utf-8
# import openCV, a module used for preprocessing
import cv2

# import numPy, a module for carrying out mathematical functions on multi-dimensional arrays
import numpy as np

# import OS, a module for carrying out operations on files
import os

# import shutil, a module for carrying out operations on directories
import shutil  
from scipy import ndimage
from skimage import filters
import math

import random # module to generate pseudo-random numbers

import codecs # module for codec registry


def getAllImages(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            #allFiles = allFiles + getAllImages(fullPath)
            print("Directory")
        else:
            allFiles.append(fullPath)
                
    return allFiles
   
def dir_operation(path):
    if not os.path.exists(path):
        os.makedirs(path)


for path in getAllImages('/home/marmf/Deposition images/Images/Testing impact of noise/Originals/'):
    if path.endswith(".png"):
        name=path[path.rfind('/')+1:len(path)-4]
        img_need_gray = cv2.imread(path)
        img_need_thresh = cv2.cvtColor(img_need_gray, cv2.COLOR_BGR2GRAY)
        pmin = np.amin(img_need_thresh)
        pmax = np.amax(img_need_thresh)
        if pmin != pmax: #check if image is just one solid colour
            otsu = filters.threshold_otsu(img_need_thresh) #find otsu's threshold
        else:
	    otsu = 0
        ret,img_otsu = cv2.threshold(img_need_otsu,otsu,255,cv2.THRESH_BINARY)  #threshold with otsus threshold
	img_otsu_ds_need_thresh = ndimage.median_filter(img_otsu,size=3) #apply a despeckling to thresholded image
	ret,img_otsu_ds = cv2.threshold(img_otsu_ds_need_thresh,otsu,255,cv2.THRESH_BINARY) #despeckling leads to small variations in pixel values that make the image not binary, so threshold again
        cv2.imwrite('/home/marmf/Deposition images/Images/Testing impact of noise/Originals/Otsu/'+name+"_otsu.png",img_otsu_ds)
	
        img_localm = cv2.adaptiveThreshold(img_need_thresh, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 31, 10); #threshold with local mean
	img_localm_ds_need_thresh = ndimage.median_filter(img_localm,size=3) #despeckle
	ret,img_localm_ds = cv2.threshold(img_localm_ds_need_thresh,otsu,255,cv2.THRESH_BINARY) #threshold again
        cv2.imwrite('/home/marmf/Deposition images/Images/Testing impact of noise/Originals/Localm/'+name+"_localm.png",img_localm_ds)