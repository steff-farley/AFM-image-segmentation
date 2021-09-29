import numpy as np
import csv
import codecs
import os
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.measure import label, regionprops
from skimage.morphology import closing, square

def getAllImages(dirName):
    # function to create a list of file and sub directories names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getAllImages(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

'''
The following function calculates the modified Minkowski functionals

path_in: set the path containing images to extract Minkowski functionals from
path_out: csv file path destination containing extracted Minkowski functionals
'''

path_in = "/home/marmf/Deposition images/Paper 2/Data/Tiling/Scaling/"
path_out = "/home/marmf/Deposition images/Paper 2/Data/Tiling/Scaling/Stats new EC.csv"

def calculate_normalised_stats(path_in,path_out):


    csvfile_stats = open(path_out, 'w') # empty spreadsheet to fill with statistics, now define column headings
    writer = csv.writer(csvfile_stats)
    writer.writerow(["name","pctarea","SIA","SIP","SIE","H0","H1","tot_particle_area","average_particle_size","tot_perimeter","SIP2","SIE2","LogE2"])

    for path in getAllImages(path_in): # for every image in specified folder
        if path.endswith(".png"): # if your images are in a different file format, change this

            name=path[path.rfind('/')+1:len(path)-4] # remove extension from file path
            img3 = mpimg.imread(path) # read image
            if img3.ndim == 3: # convert to greyscale if not already
                img2 = img3[:,:,0]
            else:
                img2 = img3

            rows,cols = img2.shape

            assert len(np.unique(img2)) == 2, "Input image must be binary"

            if img2.max() == 255: # set pixel values to 0 and 1
                img = img2/255
            else:
                img = img2

            #  Find unique sections
            img_close = closing(img, square(3))
            img_close_inv = np.abs(1 - img_close)
            label_img = label(img_close)
            label_img_inv = label(img_close_inv)

            #  Get stats
            H0_unmod = label_img.max()
            H1_unmod = label_img_inv.max()

            # first need to weight H0 and H1 contributions if intersecting with bottom or right edge
            # weighted as described in thesis
            unique_rightH0 = np.unique(label_img[:,-1])
            unique_rightH0 = unique_rightH0[unique_rightH0 != 0]
            unique_bottomH0 = np.unique(label_img[-1,:])
            unique_bottomH0 = unique_bottomH0[unique_bottomH0 != 0]
            unique_rbH0 = np.concatenate((unique_rightH0,unique_bottomH0))
            matched_rbH0, freqH0 = np.unique(unique_rbH0, return_counts = True)
            count_rbH0 = np.count_nonzero(freqH0 == 2)
            H0_mod = H0_unmod - 3*(count_rbH0/4)
            unique_rightH0_mod = unique_rightH0.size - count_rbH0
            unique_bottomH0_mod = unique_bottomH0.size - count_rbH0
            H0 = H0_mod - unique_rightH0_mod/2 - unique_bottomH0_mod/2

            unique_rightH1 = np.unique(label_img_inv[:,-1])
            unique_rightH1 = unique_rightH1[unique_rightH1 != 0]
            unique_bottomH1 = np.unique(label_img_inv[-1,:])
            unique_bottomH1 = unique_bottomH1[unique_bottomH1 != 0]
            unique_rbH1 = np.concatenate((unique_rightH1,unique_bottomH1))
            matched_rbH1, freqH1 = np.unique(unique_rbH1, return_counts = True)
            count_rbH1 = np.count_nonzero(freqH1 == 2)
            H1_mod = H1_unmod - 3*(count_rbH1/4)
            unique_rightH1_mod = unique_rightH1.size - count_rbH1
            unique_bottomH1_mod = unique_bottomH1.size - count_rbH1
            H1 = H1_mod - unique_rightH1_mod/2 - unique_bottomH1_mod/2

            if H0 > H1:
                H = H0
                tot_particle_area = np.sum(label_img > 0)
                average_particle_size = tot_particle_area / H0
                scaling_factor = H0 * np.sqrt(average_particle_size)
            else:
                H = H1
                tot_particle_area = np.sum(label_img_inv > 0)
                average_particle_size = tot_particle_area / H1
                scaling_factor = H1 * np.sqrt(average_particle_size)

            perimeter = regionprops(img_close_inv.astype(int))[0]["perimeter"]
            edge_perimeter = np.sum(img_close_inv[0,:])+np.sum(img_close_inv[:,0])+np.sum(img_close_inv[rows-1,:])+np.sum(img_close_inv[:,cols-1])
            tot_perimeter = perimeter - edge_perimeter

            #  Make stats size invariant
            pctarea = float(float(np.sum(label_img > 0)) / float(np.size(label_img)))
            SIA = float(float(tot_particle_area) / float(np.size(label_img)))
            SIP = tot_perimeter / scaling_factor
            SIE = float(float(H0) / (float(H0)+float(H1)))
            SIP2 = SIP/(2*np.sqrt(math.pi))
            SIE2 = float((float(H0)+float(H1))/(2*float(H)))
            LogE2 = np.log(SIE2)

            writer.writerow([name,pctarea,SIA,SIP,SIE,H0,H1,tot_particle_area,average_particle_size,tot_perimeter,SIP2, SIE2, LogE2])

    csvfile_stats.close()

calculate_normalised_stats(path_in,path_out)