
# this file is to convert the matrix to an image
from PIL import Image 
import numpy as np


# So that we can see the image clearly we will resize the image 
resize_factor = 100

matt = [[1,0,1],[0,2,0],[1,0,1]]

# write array to img
def create_img(cell_array,p):
    array = np.zeros((len(cell_array), len(cell_array[0]), 3), dtype=np.uint8)
    for x in range(0, len(cell_array)):
        for y in range(0, len(cell_array[0])):
            if cell_array[x][y] == 0:
                array[x][y] = (255, 255, 255) # white
            elif cell_array[x][y] == 1:
                array[x][y] = (0, 0, 0) # black
            elif cell_array[x][y] == 2:
                array[x][y] = (0, 0, 255) # blue

    # if not os.path.exists(dir_path):
    #     os.makedirs(dir_path)

    img = Image.fromarray(array) # fromarray() takes a numpy array and returns a PIL image
    img = img.resize([int(resize_factor*x) for x in img.size], Image.BOX) # resize the image
    img.save(f'../CellModel/results/img_{p}.jpeg')
    # img.show() # show the image



