#the timestep function 
import imageConverter as ic
import random
import numpy as np
import time

# cell death and birth
# dead cell is denote by 0 are meant to be empty spaces
# sensitive cells are denote by 1 
# resistant cells are denote by 2 
# persistor cells are denote by 3 
 
# non-mutated cells are   and mutated cells are resistant to the treatment
# a time step is a single iteration of the matrix
# a cell can die or mutate or stay the same
# false indicates treatment is off and true indicates treatment is on

# THESE ARE THE VARIABLES THAT CAN BE CHANGED BY THE USER
treat_cell_kill = True # this bool is to enable the treatment to kill the increase the probability of death of the cell
treat_cell_slow = True # this bool is to enable the treatment to slow the proliferation of the cell
inter_treat = False # this bool is to enable the treatment to be applied at selected intervals
adapt_treat = True # this bool is to enable the treatment that is applied to be adaptive to the population of the cell
# inter and adapt treat cannot be true at the same time

num_times = 250 # number of times the time step function will run
cell_pop = 0 # number of cells in the matrix
treat_applied = False # boolean to check if the treatment has been applied

# these are the probabilities apoptosis of cells
prob_death_sens = 0.15 
prob_death_res = 0.15 
prob_death_pers = 0.15

# these are the probabilities of proliferation of cells
prob_birth_sens = 0.425 
prob_birth_res = 0.40 
prob_birth_pers = 0.425 

# these are the probabilities of mutation of cells
prob_mut_res = 0.00005 
prob_mut_per = 0.005 
prob_mut_per_res = 0.0005 

cell_applied_kill = False # this bool is to check if the treatment has been applied to the cell
cell_applied_slow = False # this bool is to check if the treatment has been applied to the cell
per_applicable = False # this bool is to check if the treatment is applicable to the persistent cells
per_counter = 0 # this counter will be the number of timesteps before the treatment is applicable to the persistent cells
per_change = 5  # timestep when the treatment is applied to the persistent cells

factor_slow = 0.75 # factor by which the cell proliferates
factor_kill = 1.65 # factor by which the cell dies
factor_kill_pers = 1.1 # factor by which the cell dies
factor_slow_pers = 0.9 # factor by which the cell proliferates
start_treat = 7600 # start of treatment
stop_treat = 7500 # stop of treatment
inter_steps = 4 # number of time steps the treatment will be applied for REMEMBER TO ALSO ADD ONE MORE THAN DESIRED NUMBER OF TIME STEPS
treatment_on_counter = 0 # counter to check how many times the treatment has been applied for
treatment_off_counter = 0 # counter to check how many times the treatment has been off for

# these function will send the values of the variables to the other files
def seed_setter():
    seed_value = int(time.time())
    random.seed(seed_value)
    return seed_value
def send_num_times():
    return num_times
def send_parameters():
    return start_treat, stop_treat, inter_steps, factor_slow, factor_kill, treat_cell_kill, treat_cell_slow, inter_treat, adapt_treat, factor_kill_pers, factor_slow_pers, per_change

# the persister cells are slightly resistant to the treatment
def pers_birth(prob_birth_pers, treat_applied):
    global per_applicable, per_counter
    if treat_applied == True:
        if per_applicable == False:
            per_counter += 1
            if per_counter == per_change:
                per_applicable = True
        if per_applicable == True:    
                prob_birth_pers = prob_birth_pers * factor_slow_pers
    else: 
        prob_birth_pers = prob_birth_pers
    return prob_birth_pers
def pers_death(prob_death_pers, treat_applied):
    if treat_applied == True:
        if per_applicable == True:
            prob_death_pers = prob_death_pers * factor_kill_pers
    else:
        prob_death_pers = prob_death_pers
    return prob_death_pers
    
# this function will kill a cell with a probability of prob_death
def cell_Death(k, i, j):
    if k[i][j] == 1 and random.random() < prob_death_sens:
        k[i][j] = 0
    elif k[i][j] == 2 and random.random() < prob_death_res:
        k[i][j] = 0
    elif k[i][j] == 3 and random.random() < pers_death(prob_death_pers, treat_applied):
        k[i][j] = 0
    return k
    
# check 8 of the neighbours of the cell
def cells_Count(k,i,j,l,row,col): 
    if i > 0 and k[i-1][j] == 0: 
        l.append((i-1,j))
    if i > 0 and j > 0 and k[i-1][j-1] == 0: 
        l.append((i-1,j-1))
    if j > 0 and k[i][j-1] == 0: 
        l.append((i,j-1))
    if i < row-1 and j > 0 and k[i+1][j-1] == 0: 
        l.append((i+1,j-1))
    if i < row-1 and k[i+1][j] == 0: 
        l.append((i+1,j))
    if i < row-1 and j < col-1 and k[i+1][j+1] == 0: 
        l.append((i+1,j+1))
    if j < col-1 and k[i][j+1] == 0: 
        l.append((i,j+1))   
    if i > 0 and j < col-1 and k[i-1][j+1] == 0: 
        l.append((i-1,j+1))

# this function will take a cell in the matrix and check all the immediate neighbours of the cell and add them into a list
def nei_Check(k,i,j):
    row = len(k)
    col = len(k[0]) 
    if k[i][j] == 1:
        nei = []
        cells_Count(k,i,j,nei,row,col)
        if nei:
        # randomly choose one of the empty cells around the cell using the list of coordinates
            rand = random.randint(0, len(nei)-1)
            a , b = nei[rand]
            if random.random() < prob_mut_res:
                k[a][b] = 2
            elif random.random() < prob_mut_per:
                k[a][b] = 3
            elif random.random() < prob_birth_sens:
                k[a][b] = 1
    if k[i][j] == 2:
        mut = []
        cells_Count(k,i,j,mut,row,col)
        if mut:
            rand = random.randint(0, len(mut)-1)
            a , b = mut[rand]
            if random.random() < prob_birth_res:
                k[a][b] = 2
    if k[i][j] == 3:
        mut = []
        cells_Count(k,i,j,mut,row,col)
        if mut:
            rand = random.randint(0, len(mut)-1)
            a , b = mut[rand]
            if random.random() < pers_birth(prob_birth_pers, treat_applied):
                k[a][b] = 3
            elif random.random() < prob_mut_per_res:
                k[a][b] = 2

    
# how to make a function that returns one to one of the empty cells around a cell     
def time_run(k):  
    row = len(k) 
    col = len(k[0])
    listCells = []
    sens = 0
    res = 0
    pers = 0
    for j in range(col):
        for i in range(row):
            if k[i][j] in [1,2,3]:
                if k[i][j] == 2:
                    res += 1
                elif k[i][j] == 1:
                    sens += 1
                elif k[i][j] == 3:
                    pers += 1
                listCells.append((i,j))
            # loop that will randomly choose a live cell, check whether to kill it, if alive then it will grow by one cell
    while len(listCells) != 0:
        rand = random.randint(0, len(listCells)-1)
        a , b = listCells[rand]
        cell_Death(k, a, b)
        nei_Check(k, a, b)
        listCells.remove((a,b))
    return sens, res, pers

# this functions will change the rate of apoptosis and proliferation of the cells
def treat_cell_kill_on(): 
    global prob_death_sens, cell_applied_kill, treatment_on_counter
    prob_death_sens = factor_kill * prob_death_sens
    treatment_on_counter += 1
    cell_applied_kill = True    
def treat_cell_kill_off():
    global prob_death_sens, cell_applied_kill, treatment_off_counter
    prob_death_sens = prob_death_sens / factor_kill
    treatment_off_counter += 1
    cell_applied_kill = False
def treat_cell_slow_on():
    global prob_birth_sens, cell_applied_slow
    prob_birth_sens = factor_slow * prob_birth_sens
    cell_applied_slow = True
def treat_cell_slow_off():
    global prob_birth_sens, cell_applied_slow
    prob_birth_sens = prob_birth_sens / factor_slow
    cell_applied_slow = False
    
# this function will apply the treatment on and off for a certain number of time steps after it reaches a certain population
def intermittent_treatment(n, total_cells, num_times, inter_steps):
    global cell_applied_kill, cell_applied_slow, treat_applied
    if total_cells > 4000:
        x, y, z, w, v, t = 100, 125, 150, 175, 200, 225
        time_treatment = list(range(x, x+ inter_steps)) + list(range(y, y+ inter_steps)) + list(range(z, z+ inter_steps)) + list(range(w, w+ inter_steps)) + list(range(v, v+ inter_steps)) + list(range(t, t+ inter_steps))
        total_range = [c for c in range(num_times) if c not in time_treatment]
        if n in time_treatment:
            if treat_cell_kill == True:
                if cell_applied_kill == False:
                    treat_cell_kill_on()
            if treat_cell_slow == True:
                if cell_applied_slow == False:
                    treat_cell_slow_on()
        if n in total_range:
            if treat_cell_kill == True:
                if cell_applied_kill == True:
                    treat_cell_kill_off()
            if treat_cell_slow == True:
                if cell_applied_slow == True:
                    treat_cell_slow_off()        

# this function will apply the treatment to the cells if the population in a certain range
def adapt_treatment(total_cells):
    global cell_applied_kill, cell_applied_slow, treat_applied
    if total_cells > start_treat:
        if treat_cell_kill == True:
            if cell_applied_kill == False:
                treat_cell_kill_on()
        if treat_cell_slow == True:
            if cell_applied_slow == False: 
                treat_cell_slow_on()
    if total_cells < stop_treat:
        if treat_cell_kill == True:
            if cell_applied_kill == True:
                treat_cell_kill_off()
        if treat_cell_slow == True:
            if cell_applied_slow == True:
                treat_cell_slow_off()
    
# this function will apply the treatment to the cells if the population in a certain range      
def cell_treatment(n, cell_pop, num_times):
    global treat_applied
    if inter_treat == True:
        intermittent_treatment(n, cell_pop, num_times, inter_steps)
        treat_applied = True
    if adapt_treat == True:
        adapt_treatment(cell_pop)
        treat_applied = True   
    

#these functions will run the simulation
def run_Cycle(l, f):
    ic.create_img(l,0)
    global cell_pop
    f.write(f"Timestep, Sensitive cells, Resistant cells, Persistant cells, Total cells \n")
    for a in range(1, num_times):
        cell_treatment(a, cell_pop, num_times)
        cell_pop = 0
        sens, res, pers = time_run(l)
        cell_pop = (sens + res + pers)
        # ic.create_img(l,a)
        f.write(f"{a}, {str(sens)}, {str(res)}, {str(pers)}, {str(cell_pop)} \n")
    return "Done"

def create_Glider(i, j, matrix):
            glider = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
            width, height = glider.shape
            matrix[i:i+width, j:j+height] = glider

# the use of arrays and tuples here is to store the data of the simulation 
# the tuple will store the data of the simulation and the array will store the data of the simulation for the number of times the simulation will run

def run_Sim(num_times): 
    arr = []
    e_sum = 0
    e_values = []
    for a in range(1, 10):
        matrix_size = 100  # size of matrix
        l = np.zeros((matrix_size, matrix_size), np.int8)
        create_Glider(50, 50, l)
        # sim_list = []
        # print(f"Simulation # {a}")
        global cell_pop, treatment_off_counter, treatment_on_counter
        treatment_off_counter, treatment_on_counter = 0, 0
        for b in range(1,num_times):
            cell_treatment(b, cell_pop, num_times)
            cell_pop = 0
            sens, res, pers = time_run(l)
            cell_pop = (sens + res + pers)
            # out_put = (sens, res, pers, cell_pop, treatment_off_counter, treatment_on_counter)
            # print(b, cell_pop)
            # sim_list.append(out_put)
            # arr.append(sim_list)
            # print(f"CURRENT LIST {list}") 
        e_sum += treatment_on_counter
    e_mean = e_sum / 10
    e_values.append(e_mean)
    return e_values

# the parameter array is used to store the outputs of the simulations with different parameters
# parameter_array = []
# testing varies parameters
def parameter_testing(output_path): 
    global start_treat, stop_treat
    parameter_list = [(i, i-100) for i in range(2100, 4901, 1000)]
    # h = open(output_path, "w")
    for (x,y) in parameter_list: 
        start_treat = x
        stop_treat = y
        print(f"Start: {start_treat}, Stop: {stop_treat}")
        e_values = run_Sim(num_times)
        # parameter_array.append(k)
    return parameter_list, e_values 

