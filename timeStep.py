#the timestep function 
import imageConverter as ic
import random
import numpy as np
import time

# cell death and birth 
# non-mutated cell is denote by 1 and dead cell is denote by 0 and mutated cell is denote by 2
# non-mutated cells are sensitive to the treatment and mutated cells are resistant to the treatment
# a time step is a single iteration of the matrix
# a cell can die or mutate or stay the same
# false indicates treatment is off and true indicates treatment is on

num_times = 250 # number of times the time step function will run
cell_pop = 0 # number of cells in the matrix
treat_applied = False # boolean to check if the treatment has been applied

prob_death_sens = 0.15 # probability of a sensitive cell dying
prob_death_res = 0.15 # probability of a sensitive cell dying
prob_birth_sens = 0.425 # probability of a non-mutated cell being born
prob_birth_res = 0.40 # probability of a resistant cell being born

prob_mutate = 0.001 # probability of a cell mutating
cell_applied_kill = False # this bool is to check if the treatment has been applied to the cell
cell_applied_slow = False # this bool is to check if the treatment has been applied to the cell

factor_slow = 0.65 # factor by which the cell proliferates
factor_kill = 1.05 # factor by which the cell dies

# THESE ARE THE VARIABLES THAT CAN BE CHANGED BY THE USER
treat_cell_kill = True # this bool is to enable the treatment to kill the increase the probability of death of the cell
treat_cell_slow = True # this bool is to enable the treatment to slow the proliferation of the cell
inter_treat = True # this bool is to enable the treatment to be applied at selected intervals
control_treat = False # this bool is to enable the treatment that is applied to be controlled by the population of the cell
# inter and control treat cannot be true at the same time

# this function will set the seed value for the random function
def seed_setter():
    seed_value = int(time.time())
    random.seed(seed_value)
    return seed_value
    
class Solution:
    # this function will kill a cell with a probability of prob_death
    def cellDeath(k, i, j):
        if k[i][j] == 1 and random.random() < prob_death_sens:
            k[i][j] = 0
        elif k[i][j] == 2 and random.random() < prob_death_res:
            k[i][j] = 0
        return k
     
    # check 8 of the neighbours of the cell
    def cellsCount(k,i,j,l,row,col): 
        if i > 0 and k[i-1][j] == 0: #if cell above is empty
            l.append((i-1,j))
        if i > 0 and j > 0 and k[i-1][j-1] == 0: #if cell to the left and above is empty
            l.append((i-1,j-1))
        if j > 0 and k[i][j-1] == 0: #if cell to the left is empty
            l.append((i,j-1))
        if i < row-1 and j > 0 and k[i+1][j-1] == 0: #if cell to below and left is empty
            l.append((i+1,j-1))
        if i < row-1 and k[i+1][j] == 0: #if cell below is empty
            l.append((i+1,j))
        if i < row-1 and j < col-1 and k[i+1][j+1] == 0: #if cell to the right and below is empty
            l.append((i+1,j+1))
        if j < col-1 and k[i][j+1] == 0: #if cell right is empty
            l.append((i,j+1))   
        if i > 0 and j < col-1 and k[i-1][j+1] == 0: #if cell to the right and above is empty
            l.append((i-1,j+1))

    # this function will take a cell in the matrix and check all the immediate neighbours of the cell and add them into a list
    def neiCheck(k,i,j):
        row = len(k) # number of rows of the matrix
        col = len(k[0]) # number of columns of the matrix
        if k[i][j] == 1:
            nei = [] # list of coordinates of the empty cells around the cell
            Solution.cellsCount(k,i,j,nei,row,col)
            if nei:
            # randomly choose one of the empty cells around the cell using the list of coordinates
                rand = random.randint(0, len(nei)-1)
                a , b = nei[rand]
                if random.random() < prob_mutate:
                    k[a][b] = 2
                elif random.random() < prob_birth_sens:
                    k[a][b] = 1
        if k[i][j] == 2:
            mut = []
            Solution.cellsCount(k,i,j,mut,row,col)
            if mut:
            # randomly choose one of the empty cells around the cell using the list of coordinates
                if random.random() < prob_birth_res:
                    rand = random.randint(0, len(mut)-1)
                    a , b = mut[rand]
                    k[a][b] = 2

    # how to make a function that returns one to one of the empty cells around a cell     
    def time(k):  
        row = len(k) # number of rows of the matrix
        col = len(k[0]) # number of columns of the matrix
        listCells = [] # list of coordinates of the live cells
        sens = 0
        res = 0
        for j in range(col):
            for i in range(row):
                # this will return a random live cell 
                if k[i][j] in [1,2]:
                    if k[i][j] == 2:
                        res += 1
                    elif k[i][j] == 1:
                        sens += 1
                    listCells.append((i,j))
                # loop that will randomly choose a live cell, check whether to kill it, if alive then it will grow by one cell
        while len(listCells) != 0:
            rand = random.randint(0, len(listCells)-1)
            a , b = listCells[rand]
            Solution.cellDeath(k, a, b)
            # if the cell is alive then it will check if there is an empty cell around it and if there is then it will randomly choose one of the empty cells and check if it will mutate or grow
            Solution.neiCheck(k, a, b)
            listCells.remove((a,b))
        return sens, res # returns the matrix after one time step and the number of sensitive cells and resistant cells
    
    # this function will apply the treatment where the probability of death of a sensitive cell is doubled
    def treat_cell_kill(): 
        global prob_death_sens, cell_applied_kill
        prob_death_sens = factor_kill * prob_death_sens
        cell_applied_kill = True
    
    # this function will reset the treatment where the probability of death of a sensitive cell is halved    
    def treat_cell_kill_off():
        global prob_death_sens, cell_applied_kill
        prob_death_sens = prob_death_sens / factor_kill
        cell_applied_kill = False
    
    # this function will apply the treatment where the probability of birth of a sensitive cell lowered by a factor
    def treat_cell_slow():
        global prob_birth_sens, cell_applied_slow
        prob_birth_sens = factor_slow * prob_birth_sens
        cell_applied_slow = True
    
    # this function will reset the treatment where the probability of birth of a sensitive cell is increased by a factor
    def treat_cell_slow_off():
        global prob_birth_sens, cell_applied_slow
        prob_birth_sens = prob_birth_sens / factor_slow
        cell_applied_slow = False
        
    # this function will apply the treatment on and off for a certain number of time steps after it reaches a certain population
    def intermittent_treatment(n, total_cells, num_times):
        global cell_applied_kill, cell_applied_slow
        if total_cells > 4000:
            x, y, z, w, v, t = 100, 125, 150, 175, 200, 225
            num_steps = 13 # number of time steps the treatment will be applied for REMEMBER TO ALSO ADD ONE MORE THAN DESIRED NUMBER OF TIME STEPS
            time_treatment = list(range(x, x+ num_steps)) + list(range(y, y+ num_steps)) + list(range(z, z+ num_steps)) + list(range(w, w+ num_steps)) + list(range(v, v+ num_steps)) + list(range(t, t+ num_steps))
            total_range = [c for c in range(num_times) if c not in time_treatment]
            if n in time_treatment:
                if treat_cell_kill == True:
                    if cell_applied_kill == False:
                        Solution.treat_cell_kill()
                        print("kill on")
                if treat_cell_slow == True:
                    if cell_applied_slow == False:
                        Solution.treat_cell_slow()
                        print("slow on")
            if n in total_range:
                if treat_cell_kill == True:
                    if cell_applied_kill == True:
                        Solution.treat_cell_kill_off()
                        print("kill off")
                if treat_cell_slow == True:
                    if cell_applied_slow == True:
                        Solution.treat_cell_slow_off()
                        print("slow off")
    
    # this function will apply the treatment to the cells if the population in a certain range
    # the tumor should be maintained betweeen 4800 and 5200 cells
    def control_treatment(total_cells):
        global cell_applied_kill, cell_applied_slow
        if total_cells > 8800:
            if treat_cell_kill == True:
                if cell_applied_kill == False:
                    Solution.treat_cell_kill()
            if treat_cell_slow == True:
                if cell_applied_slow == False: 
                    Solution.treat_cell_slow()
        if total_cells < 8600:
            if treat_cell_kill == True:
                if cell_applied_kill == True:
                    Solution.treat_cell_kill_off()
            if treat_cell_slow == True:
                if cell_applied_slow == True:
                    Solution.treat_cell_slow_off()         
            
    def cell_treatment(n, cell_pop, num_times):
        global treat_applied
        if inter_treat == True:
            Solution.intermittent_treatment(n, cell_pop, num_times)
            treat_applied = True
        if control_treat == True:
            Solution.control_treatment(cell_pop)
            treat_applied = True
     
    
#the time step function will print the matrix after each time step
    def runCycle(l, f):
        ic.create_img(l,0)
        global cell_pop
        f.write(f"Timestep, Sensitive cells, Resistant cells, Total cells \n")
        for a in range(1, num_times):
            Solution.cell_treatment(a, cell_pop, num_times)
            cell_pop = 0
            sens, res = Solution.time(l)
            cell_pop = (sens + res)
            ic.create_img(l,a)
            f.write(f"{a}, {str(sens)}, {str(res)}, {str(cell_pop)} \n")
        return "Done"

