from utils import *

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def read_pgm(path,orig_image):
    try:
        f = open(path, 'r')
        t = f.readline()
    except UnicodeDecodeError:
        f = open(path, 'rb')
        t = f.readline().decode()
    if t == 'P2\n':
        data = read_pgma(f)
    elif t == 'P5\n':
        data = read_pgmb(f)
    else:
        print("can't read file !")
        return False

    orig_image.set_data(data[0], data[1], data[2],data[3], path)

def read_pgma(f):

    lines = f.readlines()

    # Ignores commented lines
    for l in list(lines):
        if l[0] == '#':
            lines.remove(l)
    
    # Get width and height of the image
    width,height =[int(c) for c in lines[0].split()]
    
    # get maximum of grey level
    max_l = int(lines[1])

    # Converts data to a list of integers
    data = []
    for line in lines[2:]:
        data.extend([int(c) for c in line.split()])
    
    image = generate_from_flat(width,height,data)
        

    return (width,height,max_l,image)

def read_pgmb(f):
    
    while True:
        line = f.readline()
        if line[0] != '#':
             break

    width,height =[int(c) for c in line.split()]
    max_l = int(f.readline())
    data = []
    byte = f.read(1)
    while byte:       
        data.append(ord(byte))
        byte = f.read(1)
    
    image = generate_from_flat(width,height,data)
        
    plt.imshow(Image.fromarray(image)) # Usage example

    return (width,height,max_l,image)


def write_pgm(data,name):

    width,height,max_l,image = extract_from_struct(data)

    f = open(name, "w")
    
    f.write("P2\n")
    f.write("# This is my image\n")
    f.write(f"{width} {height}\n")

    flat_image = image.flatten('C')
    
    f.write(f"{max_l}\n")

    for i in flat_image:
        f.write(f'{i} ')

    f.close()