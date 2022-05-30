import numpy as np
from utils import *
from stats import *
import random
import math

def otsu(data):
    width,height,max_l,image = extract_from_struct(data)

    flat_image = image.flatten("C")

    pixel_number = width * height
    mean_weigth = 2.0/pixel_number

    his, bins = np.histogram(flat_image, np.array(range(0, max_l+1)))
    final_thresh = -1
    final_value = -1
    for t in bins[1:-1]:
        Wb = np.sum(his[:t]) * mean_weigth
        Wf = np.sum(his[t:]) * mean_weigth

        mub = np.mean(his[:t])
        muf = np.mean(his[t:])

        value = Wb * Wf * (mub - muf) ** 2

        if value > final_value:
            final_thresh = t
            final_value = value
    
    final_image = flat_image.copy()
    final_image[flat_image > final_thresh] = 255
    final_image[flat_image < final_thresh] = 0
    new_image = generate_from_flat(width,height,final_image)

    return width,height,max_l,new_image

def dilatation(data, size):
    if (size % 2 == 0):
        size += 1
        
    width,height,max_l,image = extract_from_struct(data)

    border = size//2

    new_image = generate_from_flat(width,height,image.flatten('C'))
    
    for i in range(border,height-border):
        for j in range(border,width-border):
            pixels = []
            for k in range(i-border,i+border+1):
                for f in range(j-border,j+border+1):
                    pixels.append(image[k][f])
            pixels.sort()
            if(pixels[0] == 0 ):
                new_image[i][j] = 0 

    return width,height,max_l,new_image

def erosion(data, size):
    if (size % 2 == 0):
        size += 1
        
    width,height,max_l,image = extract_from_struct(data)

    border = size//2

    new_image = generate_from_flat(width,height,image.flatten('C'))
    
    for i in range(border,height-border):
        for j in range(border,width-border):
            pixels = []
            for k in range(i-border,i+border+1):
                for f in range(j-border,j+border+1):
                    pixels.append(image[k][f])
            pixels.sort()
            if(pixels[pow(size,2) - 1] == 255):
                new_image[i][j] = 255 

    return width,height,max_l,new_image

def opening(data,size):
    data_eros = erosion(data,size)
    width,height,max_l,ouv_image = dilatation(data_eros,size)
    
    return width,height,max_l,ouv_image

def closing(data,size):
    data_dilat = dilatation(data,size)
    width,height,max_l,ouv_image = erosion(data_dilat,size)

    return width,height,max_l,ouv_image
