import numpy as np
import argparse
import cv2
import os
from pdf2image import convert_from_path
from fpdf import FPDF
import sys
from PIL import Image
#%% Some constants
args = sys.argv
DATAPATH = 'input/'
OUTPUTPATH = 'generated_output/'
IMGPATH = 'img/'
INPUT_PDF = '42-1985.pdf'
# construct the argument parse and parse the arguments
# load the image from disk
# Convert pdf to image
inName = args[1] if len(args) > 1 else DATAPATH+INPUT_PDF
pages = convert_from_path(inName, dpi=200)
rotated_pages = []
blurred = []
#iterate through each page 
for i in range(len(pages)):
    
    #get image page
    currLoc = IMGPATH + str(i) + '.jpeg'
    pages[i].save(currLoc, 'JPEG')
    image = cv2.imread(currLoc)
    
    #invert colors
    # convert the image to grayscale and flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    thresh = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # grab the (x, y) coordinates of all pixel values that
    # are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all coordinates
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    
    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we
    # need to add 90 degrees to the angle
    if angle < -45:
        angle = -(90 + angle)

    else:
        # otherwise, just take the inverse of the angle to make
        # it positive
        angle = -angle
    
    #rotate and save image 
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
	flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    #save image
    rot_name = IMGPATH + str(i) +'rot.jpeg'
    cv2.imwrite(rot_name, rotated)
    rotated_pages.append(rot_name)
    # show the output image
    print("[INFO] angle: {:.3f}".format(angle))
    '''
    Written to add Blur to preprocessing
    blur = cv2.blur(rotated, (7,7))
    cv2.imwrite(IMGPATH+str(i)+'blur.jpeg', blur)
    blurred.append(IMGPATH+str(i)+'blur.jpeg')
    '''

pdf = FPDF()
imagelist = rotated_pages
outName = args[2] if len(args) > 2 else OUTPUTPATH+"edited.pdf"
images = []
#Convert images of pdf back into PDFs and merge the pdf into one file
for i in range(len(imagelist)):
    fname = imagelist[i]
    print(fname)
    im = Image.open(fname)
    if im.mode == "RGBA":
        im = im.convert("RGB")
    images.append(im)
images[0].save(outName, save_all = True, quality=100, append_images = images[1:])