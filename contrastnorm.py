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
import math


# define a function to return paths to images in a specified directory
def getAllImages(path):
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith(".png") or f.endswith(".tif") or f.endswith(".jpg")]


for path in getAllImages("/home/marmf/Deposition images/Images/NewPreProcessing/Median_Aligned_DoF_2_Poly_Detrends_All/Training/"):
        
    name=path[path.rfind('/')+1:len(path)-4] # keep only name of image from path
    
    img = cv2.imread(path,0)
    normimg = np.zeros((511,511))
    mean = np.mean(img)
    std = np.std(img)
    minv = int(round(max(0,mean-2*std)))
    maxv = int(round(min(255,mean+2*std)))
    #make all pixels be within two standard deviations of the mean, then normalise
    for k in range(minv+1):
	img[img==k] = minv
    for l in range(255-maxv+1):
	img[img==255-l] = maxv
    normimg = cv2.normalize(img,  normimg, 0, 255, cv2.NORM_MINMAX)
    cv2.imwrite("/home/marmf/Deposition images/Images/NewPreProcessing/Median_Aligned_DoF_2_Poly_Detrends_All/Training CN2sd/Originals/"+name+".png",normimg)


