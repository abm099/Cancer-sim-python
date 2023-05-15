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

num_times = 100 # number of times the time step function will run
cell_pop = 0 # number of cells in the matrix
treat_applied = False # boolean to check if the treatment has been applied

prob_death_sens = 0.15 # probability of a sensitive cell dying
prob_death_res = 0.15 # probability of a sensitive cell dying
prob_birth_sens = 0.425 # probability of a non-mutated cell being born
prob_birth_res = 0.40 # probability of a resistant cell being born

prob_mutate = 0.001 # probability of a cell mutating

factor = 0.75 # factor by which the cell proliferates 

#this bools are to switch the treatments on and off
# false indicates treatment is off and true indicates treatment is on
treat_cell_kill = False
treat_cell_slow = False

def seed_setter():
    seed_value = int(time.time())
    random.seed(seed_value)
    return seed_value

matt = [[1,0,1],[0,1,0],[1,0,1]] 

    
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
        global prob_death_sens
        prob_death_sens = 2 * prob_death_sens
    
    # this function will apply the treatment where the probability of birth of a sensitive cell lowered by a factor
    def treat_cell_slow():
        global prob_birth_sens
        prob_birth_sens = factor * prob_birth_sens    
    
    def cell_treatment(cell_pop):
        global prob_death_sens, treat_applied
        if cell_pop > 2000:
            if treat_cell_kill == True:
                Solution.treat_cell_kill()
                treat_applied = True
            if treat_cell_slow == True:
                Solution.treat_cell_slow()
                treat_applied = True
        if treat_applied == True:
            print("Treatment applied")
     
    
#the time step function will print the matrix after each time step
    def runCycle(l, f):
        ic.create_img(l,0)
        global cell_pop
        f.write(f"Timestep, Sensitive cells, Resistant cells, Total cells \n")
        for a in range(num_times):
            if treat_applied == False:
                Solution.cell_treatment(cell_pop)
            cell_pop = 0
            sens, res = Solution.time(l)
            cell_pop = (sens + res)
            ic.create_img(l,a+1)
            f.write(f"{a+1}, {str(sens)}, {str(res)}, {str(cell_pop)} \n")
        return print("Done")

