import cv2 # image processing functions
import numpy as np # manipulating arrays
import os # for navigating folders and files
import shutil  # operations on files
from scipy import ndimage # for applying filters to images (e.g. Gaussian filter)
import math # math functions
import random # generating random numbers
import codecs
import scipy.misc 
from skimage import filters # used for finding otsus threshold

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
            #allFiles = allFiles + getAllImages(fullPath)
            print("directory")
        else:
            allFiles.append(fullPath)
                
    return allFiles

def imgstripe(img):
    # function to add stripes to image
    rows,cols = img.shape
    rand_x = random.randint(15,rows-16) # randomised center x value of center stripe
    rand_y = random.randint(0,rows-11) # randomised center y value of center stripe
    rand_length = random.randint(0,rows-21) # randomised length of stripes in both y directions
    bow = random.randint(0,2) # 0 = black stripes, 1 = white stripes, 2 = random grey stripes
    numofs = random.randint(1,7) # randomised number of stripes
    if bow == 1:
	int = 255
    elif bow == 0:
	int = 0
    else:
	int = random.randint(1,254)
    if rand_y + rand_length + 20 > rows-1:
	if numofs >= 1:
            img[(rand_x-15):(rand_x-14),(rand_y+random.randint(0,10)):rows-1] = int
	if numofs >= 2:
            img[(rand_x-10):(rand_x-9),(rand_y+random.randint(0,10)):rows-1] = int
	if numofs >= 3:
            img[(rand_x-6):(rand_x-5),(rand_y+random.randint(0,10)):rows-1] = int
	if numofs >= 4:
            img[(rand_x-1):(rand_x+1),(rand_y+random.randint(0,10)):rows-1] = int
	if numofs >= 5:
            img[(rand_x+3):(rand_x+4),(rand_y+random.randint(0,10)):rows-1] = int
	if numofs >= 6:
            img[(rand_x+8):(rand_x+9),(rand_y+random.randint(0,10)):rows-1] = int
	if numofs >= 7:
            img[(rand_x+13):(rand_x+14),(rand_y+random.randint(0,10)):rows-1] = int
    else:
	if numofs >= 1:
            img[(rand_x-15):(rand_x-14),(rand_y+random.randint(0,10)):(rand_y+rand_length+random.randint(0,10))] = int
	if numofs >= 2:
            img[(rand_x-10):(rand_x-9),(rand_y+random.randint(0,10)):(rand_y+rand_length+random.randint(0,10))] = int
	if numofs >= 3:
            img[(rand_x-6):(rand_x-5),(rand_y+random.randint(0,10)):(rand_y+rand_length+random.randint(0,10))] = int
	if numofs >= 4:
            img[(rand_x-1):(rand_x+1),(rand_y+random.randint(0,10)):(rand_y+rand_length+random.randint(0,10))] = int
	if numofs >= 5:
            img[(rand_x+3):(rand_x+4),(rand_y+random.randint(0,10)):(rand_y+rand_length+random.randint(0,10))] = int
	if numofs >= 6:
            img[(rand_x+8):(rand_x+9),(rand_y+random.randint(0,10)):(rand_y+rand_length+random.randint(0,10))] = int
	if numofs >= 7:
            img[(rand_x+13):(rand_x+14),(rand_y+random.randint(0,10)):(rand_y+rand_length+random.randint(0,10))] = int
    if rand_y - rand_length - 20 < 0:
	if numofs >= 1:
            img[(rand_x-15):(rand_x-14),0:(rand_y-random.randint(0,10))] = int
	if numofs >= 2:
            img[(rand_x-10):(rand_x-9),0:(rand_y-random.randint(0,10))] = int
	if numofs >= 3:
            img[(rand_x-6):(rand_x-5),0:(rand_y-random.randint(0,10))] = int
	if numofs >= 4:
            img[(rand_x-1):(rand_x+1),0:(rand_y-random.randint(0,10))] = int
	if numofs >= 5:
            img[(rand_x+3):(rand_x+4),0:(rand_y-random.randint(0,10))] = int
	if numofs >= 6:
            img[(rand_x+8):(rand_x+9),0:(rand_y-random.randint(0,10))] = int
	if numofs >= 7:
            img[(rand_x+13):(rand_x+14),0:rand_y] = int
    else:
	if numofs >= 1:
            img[(rand_x-15):(rand_x-14),(rand_y-rand_length-random.randint(0,10)):(rand_y-random.randint(0,10))] = int
	if numofs >= 2:
            img[(rand_x-10):(rand_x-9),(rand_y-rand_length-random.randint(0,10)):(rand_y-random.randint(0,10))] = int
	if numofs >= 3:
            img[(rand_x-6):(rand_x-5),(rand_y-rand_length-random.randint(0,10)):(rand_y-random.randint(0,10))] = int
	if numofs >= 4:
            img[(rand_x-1):(rand_x+1),(rand_y-rand_length-random.randint(0,10)):(rand_y-random.randint(0,10))] = int
	if numofs >= 5:
            img[(rand_x+3):(rand_x+4),(rand_y-rand_length-random.randint(0,10)):(rand_y-random.randint(0,10))] = int
	if numofs >= 6:
            img[(rand_x+8):(rand_x+9),(rand_y-rand_length-random.randint(0,10)):(rand_y-random.randint(0,10))] = int
	if numofs >= 7:
            img[(rand_x+13):(rand_x+14),(rand_y-rand_length-random.randint(0,10)):(rand_y-random.randint(0,10))] = int

    return img

# path_in is the folder with clean images to be augmented
# path_out is the folder where augmentated images will be saved
path_in = "/home/marmf/Deposition images/Images/Testing impact of noise/Originals/"
path_out = "/home/marmf/Deposition images/Images/Testing impact of noise/Augmented/"

progress=0 # progress is an integer that is used in the augmented image file name when it's saved

for path in getAllImages(path_in): # get all full file names for all images from path_in and loop through them one by one
    
    name=path[path.rfind('/')+1:len(path)-4] # keep just the file name without extention
    
    # augmented image 1: adding stripes
    img = cv2.imread(path,0) # read image
    rows,cols = img.shape
    
    img_stripes = imgstripe(img)
    cv2.imwrite(path_out+name+"_"+str(progress+0)+".png",img_stripes)
    
    # augmented image 2 and 3: banding and banding + stripes
    img = cv2.imread(path,0)
    im_max = float(np.amax(img))/255 # max pixel value in image
    img_banding = img
    for y in range(0,rows-1): # create banding effect
        img_banding[:,y] = 0.5*((math.sin(float(y)/100)+3)/(2*max(im_max,0.004)))*img[:,y]
    cv2.imwrite(path_out+name+"_"+str(progress+1)+".png",img_banding)
    img_stripes2 = imgstripe(img_banding)
    cv2.imwrite(path_out+name+"_"+str(progress+2)+".png",img_stripes2)

    # augmented image 4: streaking
    img = cv2.imread(path,0)
    
    mask_need_crop = cv2.imread("/home/marmf/Deposition images/Images/For Unet/Training images/Clean only/Masks/Mask4.tif",0)
    
    #uncomment if streaking with a high-frequency horizontal banding
    #im_max = float(np.amax(img))/255
    #for x in range(0,rows-1):
        #img_streaking[x,:] = 0.5*((math.sin(float(x)/4)/2+3)/(2*max(im_max,0.004)))*img_[x,:]
    
    mask = mask_need_crop[0:rows, 0:rows]
    mask = cv2.resize(mask,(rows,rows),interpolation = cv2.INTER_CUBIC)
    flip = random.randint(0,1)
    if flip == 1:
        mask = cv2.flip(mask,1)
    scale = random.randint(0,1)
    if scale == 1:
	mask_need_crop = cv2.resize(mask,(rows+50,rows+50),interpolation = cv2.INTER_CUBIC)
	mask = mask_need_crop[25:rows+25,25:rows+25]
    pmin = np.amin(img)
    pmax = np.amax(img)
    if pmin != pmax:
        otsu = filters.threshold_otsu(img)
    else:
	otsu = 0
    img_streaking = img
    for i in range(0,rows-1):
	for j in range(0,rows-1):
	    if img_streaking[i,j] <= otsu:
		img_streaking[i,j] = min(0.1*mask[i,j]+img[i,j],255)
    
    cv2.imwrite(path_out+name+"_"+str(progress+3)+".png",img_streaking)

    # augmented image 5: inversion
    img = cv2.imread(path,0)
    rand_x = random.randint(2,rows-3) # randomised row for inversion
    img_inverted = img
    img_inverted[(rand_x-2):(rand_x+2),:] = 255 - img[(rand_x-2):(rand_x+2),:]
    cv2.imwrite(path_out+name+"_"+str(progress+4)+".png",img_inverted)
    
    # augmented image 6: blurring
    img = cv2.imread(path,0)
    rand_x = random.randint(10,rows-11) # randomised rows for blurring
    img_blurred = img
    img_blurred[(rand_x-10):(rand_x+10),:] = ndimage.median_filter(img[(rand_x-10):(rand_x+10),:],size=5)
    cv2.imwrite(path_out+name+"_"+str(progress+5)+".png",img_blurred)

    # augmented image 7: drift
    img = cv2.imread(path,0)
    rand_x = random.randint(2,rows-3) # randomised row for drift effect
    print(rand_x) # print row so easier to find in image
    img_drift = img
    # drift pixels in row by 5 places, in neighbouring rows by 3 places, and next rows by 1 place
    img_drift[rand_x,5:rows-1] = img[rand_x,0:rows-6]
    img_drift[rand_x,0:4] = img[rand_x,rows-5:rows-1]
    img_drift[(rand_x-1),3:rows-1] = img[(rand_x-1),0:rows-4]
    img_drift[(rand_x-1),0:2] = img[(rand_x-1),rows-3:rows-1]
    img_drift[(rand_x+1),3:rows-1] = img[(rand_x+1),0:rows-4]
    img_drift[(rand_x+1),0:2] = img[(rand_x+1),rows-3:rows-1]
    img_drift[(rand_x-2),1:rows-1] = img[(rand_x-2),0:rows-2]
    img_drift[(rand_x-2),0] = img[(rand_x-2),rows-1]
    img_drift[(rand_x+2),1:rows-1] = img[(rand_x+2),0:rows-2]
    img_drift[(rand_x+2),0] = img[(rand_x+2),rows-1]
    cv2.imwrite(path_out+name+"_"+str(progress+6)+".png",img_drift)

    # augmented image 8: varying contrast
    img = cv2.imread(path,0)
    mask_need_crop = cv2.imread("/home/marmf/Deposition images/Images/For Unet/Training images/Clean only/Masks/Mask4.tif",0)
    img_contrast = img
    mask = mask_need_crop[0:rows, 0:rows]
    mask = cv2.resize(mask,(rows,rows),interpolation = cv2.INTER_CUBIC)
    flip = random.randint(0,1)
    if flip == 1:
        mask = cv2.flip(mask,1)
    scale = random.randint(0,1)
    if scale == 1:
	mask_need_crop = cv2.resize(mask,(rows+50,rows+50),interpolation = cv2.INTER_CUBIC)
	mask = mask_need_crop[25:rows+25,25:rows+25]
    img_contrast_inv = img_contrast
    for i in range(0,rows-1):
	for j in range(0,rows-1):
	    img_contrast_inv[i,j] = 255-img_contrast[i,j]
    pmin = np.amin(img)
    pmax = np.amax(img)
    if pmin != pmax:
        otsu = filters.threshold_otsu(img)
    else:
	otsu = 0
    for i in range(0,rows-1):
	for j in range(0,rows-1):
	    if img_contrast_inv[i,j] <= otsu:
		img_contrast_inv[i,j] = min(0.1*mask[i,j]+img[i,j],255)
    for i in range(0,rows-1):
	for j in range(0,rows-1):
	    img_contrast[i,j] = 255-img_contrast_inv[i,j]
    cv2.imwrite(path_out+name+"_"+str(progress+7)+".png",img_need_contrast)
    
    progress+=8
