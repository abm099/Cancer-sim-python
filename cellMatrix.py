import numpy as np 
import timeStep 
import imageConverter as ic

seed_value = timeStep.seed_setter()
# print("Start simulation")
# f = open(f"../../CellModel/simulation_Files/redearEditor_seed({seed_value}).txt", "w")
# g = open(f"../../CellModel/simulation_Files/parameters_file({seed_value}).txt", "w")

matrix_size = 100 
num_times = timeStep.send_num_times()
# create glider function
# def createGlider(i, j, matrix): 
    # glider = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    # width , height = glider.shape
    # matrix[i:i+width, j:j+height] = glider

# initialize the matrix
# h = np.zeros((matrix_size, matrix_size),np.int8) 
# createGlider(50, 50, h)
 #these are the important parameters 
start_treat, stop_treat, inter_steps, factor_slow, factor_kill, treat_cell_kill, treat_cell_slow, inter_treat, control_treat, factor_kill_pers, factor_slow_pers, per_change = timeStep.send_parameters()

# write a function to that the parameters and write them to a file g
def write_parameters(g, seed, start, stop, inter_steps, slow, kill, treat_cell_kill, treat_cell_slow, inter_treat, control_treat, factor_kill_pers, factor_slow_pers, per_change):
    g.write(f"seed: {seed}\n\n")
    g.write(f"Start: {start}\n")
    g.write(f"Stop: {stop}\n")
    g.write(f"Treatment interval: {inter_steps - 1}\n")
    g.write(f"factor_slow: {slow}\n")
    g.write(f"factor_kill: {kill}\n")
    g.write(f"factor_kill_pers: {factor_kill_pers}\n")
    g.write(f"factor_slow_pers: {factor_slow_pers}\n")
    g.write(f"per_change: {per_change}\n\n")
    g.write(f"FIXED PARAMETERS\n")
    g.write(f"Treatment to kill the increase the probability of death of the cell: {treat_cell_kill}\n")
    g.write(f"Treatment to slow the proliferation of cells: {treat_cell_slow}\n")
    g.write(f"Intermittent treatment: {inter_treat}\n")
    g.write(f"Adaptive treatment: {control_treat}\n")
    g.close()
# write_parameters(seed_value, start_treat, stop_treat, inter_steps, factor_slow, factor_kill ,treat_cell_kill, treat_cell_slow, inter_treat, control_treat, factor_kill_pers, factor_slow_pers, per_change)

# print("End simulation")

# Commmit changes to the repository