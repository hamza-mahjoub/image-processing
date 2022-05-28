import numpy as np
from utils import *
from stats import *
import random
import math

def add_noise(data):
    width,height,max_l,image = extract_from_struct(data)
    flat_image = image.flatten('C')
    for i in range(len(flat_image)):
        r = random.randint(0,20)
        if(r == 0):
            flat_image[i] = 0
        elif(r == 20):
            flat_image[i] = max_l
    
    new_image = generate_from_flat(width,height,flat_image)

    return (width,height,max_l,new_image)

def convolution(data,filt,size,isGauss = False):

    width,height,max_l,image = extract_from_struct(data)

    if (isGauss == False):
        avg = 1 / pow(size,2)
    
    border = size//2

    new_image = generate_from_flat(width,height,image.flatten('C'))

    for i in range(border,height-border):
        for j in range(border,width-border):
            sum_l = 0
            for k in range(i-border,i+border+1):
                for f in range(j-border,j+border+1):
                    sum_l += new_image[k][f] * filt[k - i][f - j]    
            if (isGauss == False):
                new_image[i][j] = int(sum_l * avg) 
            else:
                new_image[i][j] = int(sum_l) 
    
    for i in range(height):
        if(i < border):
            for j in range(width):
                new_image[i][j] = 0
                new_image[height - i -1][j] = 0
        else:
            for j in range(border):
                new_image[i][j] = 0
                new_image[i][width - j  -1] = 0

    return width,height,max_l,new_image

def convolution_no_average(data,filt,size):

    width,height,max_l,image = extract_from_struct(data)

    avg = 1 / pow(size,2)
    border = size//2

    new_image = generate_from_flat(width,height,image.flatten('C'))

    for i in range(border,height-border):
        for j in range(border,width-border):
            sum_l = 0
            for k in range(i-border,i+border+1):
                for f in range(j-border,j+border+1):
                    sum_l += new_image[k][f] * filt[k - i][f - j]    
            if (sum_l < 0):
                sum_l = 0
            if (sum_l > max_l):
                sum_l = max_l
            new_image[i][j] = int(sum_l)  
    
    for i in range(height):
        if(i < border):
            for j in range(width):
                new_image[i][j] = 0
                new_image[height - i -1][j] = 0
        else:
            for j in range(border):
                new_image[i][j] = 0
                new_image[i][width - j  -1] = 0

    return width,height,max_l,new_image

def average_filter(data, size):
    if (size % 2 == 0):
        size += 1
    filt = np.ones((size,size),np.int32)
    return convolution(data, filt, size)

def median_filter(data, size):
    if (size % 2 == 0):
        size += 1
        
    width,height,max_l,image = extract_from_struct(data)

    border = size//2

    new_image = generate_from_flat(width,height,image.flatten('C'))
    
    for i in range(border,height-border):
        for j in range(border,width-border):
            medians = []
            for k in range(i-border,i+border+1):
                for f in range(j-border,j+border+1):
                    medians.append(image[k][f])
            medians.sort()
            new_image[i][j] = medians[len(medians) // 2 + 1] 
    
    for i in range(height):
        if(i < border):
            for j in range(width):
                new_image[i][j] = 0
                new_image[height - i -1][j] = 0
        else:
            for j in range(border):
                new_image[i][j] = 0
                new_image[i][width - j  -1] = 0

    return width,height,max_l,new_image

def high_filter(data):
    filt = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    return convolution_no_average(data, filt, 3)


def laplace_filter(data):
    filt = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return convolution_no_average(data, filt, 3)


def gauss_filter(data, size):
    if (size % 2 == 0):
        size += 1
    filt = np.ones((size,size),np.float64)
    sum = 0
    center = size // 2
    for py in range(-center, center + 1):
        for px in range(-center, center + 1):
            filt[py + center][px + center] = 2 ** (center ** 2 - abs(py) - abs(px))
            sum += filt[py + center][px + center]
    for py in range(-center, center + 1):
        for px in range(-center, center + 1):
            filt[py + center][px + center] /= sum
    return convolution(data, filt, size, True)

def SNR(orig_data,new_data):
    mean,var = stat_image(orig_data)

    width,height,max_l,image = extract_from_struct(orig_data)
    width_new,height_new,max_l_new,image_new = extract_from_struct(new_data)

    S = 0
    B = 0
    for i in range(height):
        for j in range(width):
            S += (image[i][j] - mean) ** 2
            B += (image_new[i][j] - image[i][j]) ** 2
    if (B == 0):
        return 0.0

    snr = math.sqrt(S / B)
    return snr
