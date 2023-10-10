# first we make the cell matrix 

import numpy as np 
import timeStep 
import imageConverter as ic

# this is to check whether the branch is being pushed to gihub

#these are the important parameters 
start_treat, stop_treat, factor_slow, factor_kill, treat_cell_kill, treat_cell_slow, inter_treat, control_treat = timeStep.send_parameters()

seed_value = timeStep.seed_setter()
print("Start simulation")
f = open(f"../../CellModel/simulation_Files/redearEditor_seed({seed_value}).txt", "w")
g = open(f"../../CellModel/simulation_Files/parameters_file({seed_value}).txt", "w")

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

# create glider in the matrix h
createGlider(50, 50, h)

# write a function to that the parameters and write them to a file g
def write_parameters(seed, start, stop, slow, kill, treat_cell_kill, treat_cell_slow, inter_treat, control_treat):
    g.write(f"seed: {seed}\n\n")
    g.write(f"Start: {start}\n")
    g.write(f"Stop: {stop}\n")
    g.write(f"factor_slow: {slow}\n")
    g.write(f"factor_kill: {kill}\n\n")
    g.write(f"FIXED PARAMETERS\n")
    g.write(f"Treatment to kill the increase the probability of death of the cell: {treat_cell_kill}\n")
    g.write(f"Treatment to slow the proliferation of cells: {treat_cell_slow}\n")
    g.write(f"Intermittent treatment: {inter_treat}\n")
    g.write(f"Adaptive treatment: {control_treat}\n")

# write the parameters to the file g
write_parameters(seed_value, start_treat, stop_treat, factor_slow, factor_kill ,treat_cell_kill, treat_cell_slow, inter_treat, control_treat)

# print(process_data(seed_value, factor_1, factor_2))
print(timeStep.Solution.runCycle(h, f))