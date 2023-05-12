# first we make the cell matrix 

import numpy as np 
import timeStep 

# this is to check whether the branch is being pushed to gihub

seed_value = timeStep.seed_setter()

f = open(f"./simulation_Files/redearEditor_seed({seed_value}).txt", "w") 

# working with square matrix
matrix_size = 100

# random matrix of 0's and 1's
k = np.random.randint(2, size=(matrix_size, matrix_size)) 


# create glider function
def createGlider(i, j, matrix): 
    glider = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    width , height = glider.shape
    matrix[i:i+width, j:j+height] = glider

# matrix of 0's
h = np.zeros((matrix_size, matrix_size),np.int8) 

# print(h)
# createGlider(0, 0, h)

createGlider(50, 50, h)
print(timeStep.Solution.runCycle(h, f))

f.close()
