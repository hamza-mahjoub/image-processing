import numpy as np
import matplotlib.pyplot as plt
import math

from utils import *

def stat_image(data):

    width,height,max_l,image = extract_from_struct(data)
    flat_image = image.flatten('C')

    mean = np.mean(flat_image)
    var = np.var(flat_image)

    return (mean,var)

def histogram(data):
    width,height,max_l,image = extract_from_struct(data)
    flat_image = image.flatten('C')
    plt.hist(flat_image,bins=data[2])
    plt.xlabel('Grey level')
    plt.ylabel('Number of points')
    # plt.show()

def Cumulitive_histogram(data):
    width,height,max_l,image = extract_from_struct(data)
    flat_image = image.flatten('C')
    plt.hist(flat_image, bins = max_l, cumulative = True, histtype = 'step', density = True, color = 'blue')
    plt.xlabel('Grey level')
    plt.ylabel('Cumulitive percentage')
    # plt.show()

def Full_histogram(data):
    width,height,max_l,image = extract_from_struct(data)
    flat_image = image.flatten('C')
    plt.hist(flat_image, bins = max_l, color = 'skyblue')
    plt.xlabel('valeurs')
    plt.ylabel('freq')
    ax2 = plt.gca().twinx()
    ax2.hist(flat_image, bins = max_l, cumulative = True, histtype = 'step', density = True, color = 'blue')
    ax2.set_ylabel('Cumulitive percentage')
    plt.tight_layout()

def generate_histograms(data):

    fig = plt.figure(figsize=(10, 7))
    rows = 1
    columns = 3

    fig.add_subplot(rows, columns, 1)
    histogram(data)
    plt.title("Histogram")

    fig.add_subplot(rows, columns, 2)
    Cumulitive_histogram(data)
    plt.title("Cumulitive Histogram")

    fig.add_subplot(rows, columns, 3)
    Full_histogram(data)
    plt.title("Histogram & Cumulitive Histogram")

    plt.show()

def generate_compare_histograms(orig_data,edit_data):

    fig = plt.figure(figsize=(10, 7))
    rows = 2
    columns = 3

    fig.add_subplot(rows, columns, 1)
    histogram(orig_data)
    plt.title("Original Histogram")

    fig.add_subplot(rows, columns, 2)
    Cumulitive_histogram(orig_data)
    plt.title("Original Cumulitive Histogram")

    fig.add_subplot(rows, columns, 3)
    Full_histogram(orig_data)
    plt.title("Original Histogram & Cumulitive Histogram")

    fig.add_subplot(rows, columns, 4)
    histogram(edit_data)
    plt.title("Edited Histogram")

    fig.add_subplot(rows, columns, 5)
    Cumulitive_histogram(edit_data)
    plt.title("Edited Cumulitive Histogram")

    fig.add_subplot(rows, columns, 6)
    Full_histogram(edit_data)
    plt.title("Edited Histogram & Cumulitive Histogram")

    plt.show()
    
def entropy(data):
    width,height,max_l,image = extract_from_struct(data)
    flat_image = image.flatten('C')
    nb_pixels = height*width
    ent = 0
    hist = [0] * (max_l + 1)
    for h in range(height):
        for w in range(width):
            hist[image[h][w]] += 1
    
    for g in range(max_l + 1):
        p = hist[g] / nb_pixels
        if (p != 0):
            ent += p * math.log2(1 / p)
    return ent