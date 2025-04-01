
# this file is to convert the matrix to an image
from PIL import Image 
import numpy as np
import os 

# So that we can see the image clearly we will resize the image 
resize_factor = 100

# Commmit changes to the repository
def img_save_path(img, p, path):
    if not os.path.exists(path):
        os.makedirs(path)
    img.save(f'{path}/img_{p}.jpeg')
    
def create_img(cell_array,p,path):
    array = np.zeros((len(cell_array), len(cell_array[0]), 3), dtype=np.uint8)
    for x in range(0, len(cell_array)):
        for y in range(0, len(cell_array[0])):
            if cell_array[x][y] == 0:
                array[x][y] = (255, 255, 255)  # white
            elif cell_array[x][y] == 1:
                array[x][y] = (70, 114, 196)   # color 4672c4
            elif cell_array[x][y] == 2:
                array[x][y] = (237, 125, 49)   # color ed7d31
            elif cell_array[x][y] == 3:
                array[x][y] = (112, 173, 71)   # color 70ad47
    img = Image.fromarray(array) 
    img = img.resize([int(resize_factor*x) for x in img.size], Image.BOX) 
    img_save_path(img, p, path)
