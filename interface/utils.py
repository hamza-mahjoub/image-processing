import numpy as np

def generate_from_flat(width,height,flat_array):
    image =np.zeros((height,width),np.int32)
    for i in range(height):
        image[i] = flat_array[i*width:width*(i+1)]
    return image

def extract_from_struct(data):
    return data[0],data[1],data[2],data[3]