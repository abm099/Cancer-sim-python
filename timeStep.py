#the timestep function
import imageConverter as ic
import random
import numpy as np
import time
import pandas as pd
import os

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
inter_treat = True # this bool is to enable the treatment to be applied at selected intervals
adapt_treat = False # this bool is to enable the treatment that is applied to be adaptive to the population of the cell
const_treat = False # this bool is to enable the treatment to be applied at a constant rate
exp_treat = False # this bool is to enable the treatment to be applied at a constant rate
# inter and adapt treat cannot be true at the same time

num_times = 350 # number of times the time step function will run
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
prob_mut_per = 0.005 # 0.005
prob_mut_per_res = 0.0005

cell_applied_kill = False # this bool is to check if the treatment has been applied to the cell
cell_applied_slow = False # this bool is to check if the treatment has been applied to the cell
per_applicable = False # this bool is to check if the treatment is applicable to the persistent cells
per_counter = 0 # this counter will be the number of timesteps before the treatment is applicable to the persistent cells
per_change = 5  # timestep when the treatment is applied to the persistent cells

factor_slow = 0.60 # factor by which the cell proliferates 60
factor_kill = 1.75 # factor by which the cell dies 1.75
factor_kill_pers = 1.50 # factor by which the cell dies 1.50
factor_slow_pers = 0.70 # factor by which the cell proliferates 70
start_treat = 7500 # start of treatment
stop_treat = 7000 # stop of treatment
inter_steps = 5 # number of time steps the treatment will be applied for REMEMBER TO ALSO ADD ONE MORE THAN DESIRED NUMBER OF TIME STEPS
treatment_on_counter = 0 # counter to check how many times the treatment has been applied for
treatment_off_counter = 0 # counter to check how many times the treatment has been off for

exp_treat_bool_app = False
metric = 50
flag = False

exp_count = 0
pers_global = 0
sens_global = 0

# these variables are dead counters for the cells
sens_dead = 0
res_dead = 0
pers_dead = 0
coun = 0

# these function will send the values of the variables to the other files
def seed_setter():
    seed_value = int(time.time())
    random.seed(seed_value)
    return seed_value
def send_num_times():
    return num_times
def send_parameters():
    return start_treat, stop_treat, inter_steps, factor_slow, factor_kill, treat_cell_kill, treat_cell_slow, inter_treat, adapt_treat, factor_kill_pers, factor_slow_pers, per_change

def pers_birth(prob_birth_pers, cell_applied_kill):
    pla_birth = prob_birth_pers
    if cell_applied_kill == True:
        if per_applicable == True:
            pla_birth = prob_birth_pers * factor_slow_pers
        else:
            pla_birth = prob_birth_pers * factor_slow
    return pla_birth
def pers_death(prob_death_pers, cell_applied_kill):
    pla_death = prob_death_pers
    if cell_applied_kill == True:
        if per_applicable == True:
            pla_death = prob_death_pers * factor_kill_pers
        else:
            pla_death = prob_death_pers * factor_kill
    return pla_death
def pers_counter(per_change):
    global per_applicable, per_counter
    if cell_applied_kill == True:
        if per_counter >= per_change:
            per_applicable = True
        else:
            per_counter += 1

# this function will kill a cell with a probability of prob_death
def cell_Death(k, i, j):
    global sens_dead, res_dead, pers_dead
    if k[i][j] == 1 and random.random() < prob_death_sens:
        k[i][j] = 0
        sens_dead += 1
    elif k[i][j] == 2 and random.random() < prob_death_res:
        k[i][j] = 0
        res_dead += 1
    elif k[i][j] == 3 and random.random() < pers_death(prob_death_pers, cell_applied_kill):
        k[i][j] = 0
        pers_dead += 1
    return k
def reset_dead():
    global sens_dead, res_dead, pers_dead
    sens_dead = 0
    res_dead = 0
    pers_dead = 0

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
            if random.random() < prob_birth_sens:
                k[a][b] = 1
            elif random.random() < prob_mut_res:
                k[a][b] = 2
            elif random.random() < prob_mut_per:
                k[a][b] = 3
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
            if random.random() < pers_birth(prob_birth_pers, cell_applied_kill):
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
    if total_cells > 1200:
        start_values = [50, 60, 70, 80, 90, 100]
        time_treatment = []
        for start in start_values:
            time_treatment += list(range(start, start + inter_steps))
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
    global cell_applied_kill, cell_applied_slow
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

def const_treatment(total_cells):
    if total_cells > start_treat:
        if treat_cell_kill == True:
            if cell_applied_kill == False:
                treat_cell_kill_on()
        if treat_cell_slow == True:
            if cell_applied_slow == False:
                treat_cell_slow_on()

sen_pop_treat = 5
def exp_treatment(total_cells,sens):
    global exp_treat_bool_app, exp_count, flag
    if exp_treat_bool_app == False:
        if total_cells > 5000 and sens > sen_pop_treat:
            if treat_cell_kill == True:
                if cell_applied_kill == False:
                    treat_cell_kill_on()
            if treat_cell_slow == True:
                if cell_applied_slow == False:
                    treat_cell_slow_on()
            flag = True
        elif sens < sen_pop_treat and flag == True:
            if treat_cell_kill == True:
                if cell_applied_kill == True:
                    treat_cell_kill_off()
                    exp_treat_bool_app = True
            if treat_cell_slow == True:
                if cell_applied_slow == True:
                    treat_cell_slow_off()
    if exp_treat_bool_app == True:
        if exp_count < metric:
            exp_count += 1
        else:                   
            if total_cells > 5000:
                if treat_cell_kill == True:
                    if cell_applied_kill == False:
                        treat_cell_kill_on()
                if treat_cell_slow == True:
                    if cell_applied_slow == False:
                        treat_cell_slow_on()

# this function will apply the treatment to the cells if the population in a certain range
def cell_treatment(n, cell_pop, sens, num_times):
    global treat_applied
    if inter_treat == True:
        intermittent_treatment(n, cell_pop, num_times, inter_steps)
        treat_applied = True
    if adapt_treat == True:
        adapt_treatment(cell_pop)
        treat_applied = True
    if const_treat == True:
        const_treatment(cell_pop)
        treat_applied = True
    if exp_treat == True:
        exp_treatment(cell_pop, sens)
        treat_applied = True


#these functions will run the simulation
def run_Cycle(l, f, path):
    ic.create_img(l,0, path)
    global cell_pop
    f.write(f"Timestep, Sensitive cells, Resistant cells, Persistant cells, Total cells \n")
    for a in range(1, num_times):
        cell_treatment(a, cell_pop, num_times)
        cell_pop = 0
        sens, res, pers = time_run(l)
        cell_pop = (sens + res + pers)
        ic.create_img(l,a, path)
        f.write(f"{a}, {str(sens)}, {str(res)}, {str(pers)}, {str(cell_pop)} \n")
    return "Done"

def create_Glider(i, j, matrix):
            glider = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
            width, height = glider.shape
            matrix[i:i+width, j:j+height] = glider

def reset_parameters():
    global cell_pop, treatment_on_counter, prob_death_sens, prob_death_res, prob_death_pers, prob_birth_sens, prob_birth_res, prob_birth_pers, cell_applied_kill, cell_applied_slow, per_applicable, per_counter, treatment_off_counter, sens_dead, res_dead, pers_dead, flag, exp_treat_bool_app
    cell_pop = 0
    treatment_on_counter = 0
    treatment_off_counter = 0
    prob_death_sens = 0.15
    prob_death_res = 0.15
    prob_death_pers = 0.15
    prob_birth_sens = 0.425
    prob_birth_pers = 0.425
    cell_applied_kill = False
    cell_applied_slow = False
    per_applicable = False
    per_counter = 0
    sens_dead = 0
    res_dead = 0
    pers_dead = 0
    flag = False
    exp_treat_bool_app = False
# the use of arrays and tuples here is to store the data of the simulation
# the tuple will store the data of the simulation and the array will store the data of the simulation for the number of times the simulation will run


def run_Sim(simulations, para_path):
    global per_change, pers_global, sens_global
    arr = []
    e_values = []
    f_values = []
    g_values = []
    h_values = []
    for a in range(0, simulations):
        path = f'../../CellModel/results/{para_path}/simulation_number_{a}'
        matrix_size = 100  # size of matrix
        l = np.zeros((matrix_size, matrix_size), np.int8)
        create_Glider(50, 50, l)
        # ic.create_img(l,0,path)
        sim_list = []
        print(f"\t \t Simulation # {a}")
        global cell_pop, sens_dead, res_dead, pers_dead
        e_value = []
        f_value = []
        g_value = []
        h_value = []
        counter_variable = 0
        max_capacity = 0
        reset_parameters()
        for step in range(1,num_times):
            cell_treatment(step, cell_pop, sens_global, num_times)
            pers_counter(per_change)
            cell_pop = 0
            sens, res, pers = time_run(l)
            pers_global = pers
            sens_global = sens
            cell_pop = sens + res + pers
            if cell_pop > 9000:
                if counter_variable == 0:
                    # e_values.append(b)
                    counter_variable += 1
                    max_capacity = step
            # ic.create_img(l,step,path)
            e_value.append(sens)
            f_value.append(res)
            g_value.append(pers)
            h_value.append(cell_pop)
            out_put = (sens, res, pers, cell_pop, sens_dead, res_dead, pers_dead, max_capacity, treatment_on_counter, treatment_off_counter)
            out_put_names = "(sens, res, pers, cell_pop, sens_dead, res_dead, pers_dead, max_cap, treat_on, treat_off)"
            # print(b, cell_pop)
            sim_list.append(tuple(out_put))
            reset_dead()
            # print(f"CURRENT LIST {list}")
        arr.append(sim_list)
        e_values.append(e_value)
        f_values.append(f_value)
        g_values.append(g_value)
        h_values.append(h_value)
    df = pd.DataFrame(arr, columns=[f'Timestep {i}' for i in range(1,num_times)], index=[f'Simulations {i+1}' for i in range(0,simulations)])
    return df, out_put_names, e_values, f_values, g_values, h_values

def write_parameters(g, num, start, stop, inter_steps, slow, kill, treat_cell_kill, treat_cell_slow, inter_treat, adapt_treat, const_treat, factor_kill_pers, factor_slow_pers, per_change):
    global exp_treat, metric
    g.write(f"timesteps: {num}\n\n")
    g.write(f"PARAMETERS\n")
    g.write(f"Start: {start}\n")
    g.write(f"Stop: {stop}\n")
    g.write(f"Treatment interval: {inter_steps - 1}\n")
    g.write(f"factor_slow: {slow}\n")
    g.write(f"factor_kill: {kill}\n")
    g.write(f"factor_kill_pers: {factor_kill_pers}\n")
    g.write(f"factor_slow_pers: {factor_slow_pers}\n")
    g.write(f"per_change: {per_change}\n\n")
    g.write(f"BOOL PARAMETERS\n")
    g.write(f"Kill Treatment: {treat_cell_kill}\n")
    g.write(f"Slow Treatment: {treat_cell_slow}\n")
    g.write(f"Intermittent treatment: {inter_treat}\n")
    g.write(f"Adaptive treatment: {adapt_treat}\n")
    g.write(f"Constant treatment: {const_treat}\n\n")
    g.write(f"Experimental treatment \n")
    g.write(f"Experiment treatment: {exp_treat}\n")
    g.write(f"Experiment metric: {metric}\n")
    g.close()


def string_list_conversion(testing_type, i, x):
        if isinstance(testing_type, list):
            if len(testing_type) != 1: 
                if not os.path.exists(testing_type[0]):
                    os.makedirs(testing_type[0])
            print(f"{testing_type[i+1]}:{x}")
            return testing_type[i+1]
        else:
            print(f"{testing_type}:{x}")
            return testing_type

parameter_dict = {}
# testing varies parameters
def parameter_testing(parameter_list,  simulations, testing_type):
    global sen_pop_treat 
    e_values = []
    f_values = []
    g_values = []
    h_values = []
    list_index = 0
    for x in parameter_list:
        sen_pop_treat = x
        var_test = string_list_conversion(testing_type, list_index, x)
        file_path = f"../../CellModel/simulation_Files/parameters_file({var_test}_{x}).txt"
        file = open(file_path, "w")
        write_parameters(file, num_times, start_treat, stop_treat, inter_steps, factor_slow, factor_kill ,treat_cell_kill, treat_cell_slow, inter_treat, adapt_treat, const_treat, factor_kill_pers, factor_slow_pers, per_change)

        k, output_names, e_value, f_value, g_value, h_value = run_Sim(simulations, f"{var_test}_{x}")
        e_values.append(e_value)
        f_values.append(f_value)
        g_values.append(g_value)
        h_values.append(h_value)
        list_index += 1
        parameter_dict[f"{x}"] = k
    return parameter_dict, output_names, e_values, f_values, g_values, h_values

output_path = f"../../CellModel/simulation_Files/file_(testing).xlsx"
def export_to_excel(output_array, file_path, sheet_name_prefix="test"):
    # Create an Excel writer object
    excel_writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    
    # Iterate through the output array, transpose each DataFrame, and write to a new sheet
    for i, df in output_array.items():
        df = df.T  # Transpose the DataFrame
        sheet_name = f'{i}_{sheet_name_prefix}'
        df.to_excel(excel_writer, sheet_name=sheet_name, index=True, header=True)
    
    # Save the Excel file
    excel_writer.close()

df, out_put_names, e_values, f_values, g_values, h_values = parameter_testing([1], 1, "test")
export_to_excel(df, output_path)

