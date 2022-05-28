import numpy as np
from collections import Counter
from utils import *

class Point:
    def __init__(self,x,y,max_n,func):
        self.x = fix_point(x,max_n,func)
        self.y = fix_point(y,max_n,func)
        
def fix_point(x,max_n,func):
    if (x < 0): 
        func(f"{x} not in 0 - {max_n} ( {x} < 0 ) ------> fixing to 0")
        return 0
    if (x > max_n):
        func(f"{x} not in 0 - {max_n} ( {x} > {max_n} ) ------> fixing to {max_n}")
        return max_n
    return x

def check_points(A,B):
    if(A.x < B.x):
        return True
    else: return False

def contrast_modifier(A,B,data):
 
    width,height,max_l,image = extract_from_struct(data)

    new_GL =np.zeros(max_l+1,np.int32)
    for i in range(len(new_GL)):
        if(A.x != 0 ):
            if(i < A.x):
                new_GL[i] = i * (A.y//A.x)

            if(i < B.x):
                new_GL[i] = i * ((B.y - A.y)//(B.x - A.x)) + ( A.y - ((B.y - A.y)//(B.x - A.x)) * A.x )

            if(i >= B.x):
                new_GL[i] = i * ((max_l - B.y)//(max_l - B.x)) + ( B.y - ((max_l - B.y)//(max_l - B.x)) * B.x  )
        elif(A.y != 0):
            if(i <= B.x):
                new_GL[i] = i * ((B.y - A.y)//(B.x - A.x)) + A.y

            if(i > B.x):
                new_GL[i] = i * ((max_l - B.y)//(max_l - B.x)) + ( B.y - ((max_l - B.y)//(max_l - B.x)) * B.x  )
        else:
            if(i <= B.x):
                new_GL[i] = i * (B.y//B.x)

            if(i > B.x):
                new_GL[i] = i * ((max_l - B.y)//(max_l - B.x)) + ( B.y - ((max_l - B.y)//(max_l - B.x)) * B.x  )

    flat_image = image.flatten('C')
    
    for i in range(len(flat_image)):
        if(new_GL[flat_image[i]] > max_l):
            flat_image[i] = max_l
        else:
            flat_image[i] = new_GL[flat_image[i]]

    final_image = generate_from_flat(width,height,flat_image)
    
    # plt.imshow(Image.fromarray(final_image))

    return (width,height,max_l,final_image)

def Histogram_egalisation(data):
    width,height,max_l,image = extract_from_struct(data)

    new_val = width * height // max_l 
    flat_image = image.flatten('C')
    counter_image = Counter(flat_image)

    H_n =np.zeros(max_l+1,np.int32)
    for i in range(max_l+1):
        H_n[i] = counter_image[i]

    P_n = np.zeros(max_l+1,np.float16)
    for i in range(max_l+1):
        P_n[i] = H_n[i]/(width * height)

    Pc_n = np.zeros(max_l+1,np.float16)
    Pc_n[0] = P_n[0]
    for i in range(1,max_l+1):
        Pc_n[i] = Pc_n[i-1]+P_n[i]

    Hp_n = [new_val] * (max_l+1)

    A = np.zeros(max_l+1,np.float16)
    for i in range(max_l+1):
        A[i] = max_l * Pc_n[i]
    
    n1 =  np.zeros(max_l+1,np.int16)
    for i in range(max_l+1):
        n1[i] = int(A[i])
    
    new_image =np.zeros(height*width,np.int32)
    for i in range(len(flat_image)):
        new_image[i] = n1[flat_image[i]]
    
    final_image = generate_from_flat(width,height,new_image)

    # plt.imshow(Image.fromarray(final_image))

 
    # print( width)
    return (width,height,max_l,final_image)