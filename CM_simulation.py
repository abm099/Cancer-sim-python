import timeStep as tS
import numpy as np
import pandas as pd
import cellMatrix as cM
import seaborn as sns
import matplotlib.pyplot as plt
import timeit

print("Start simulation")

start = timeit.default_timer()
num_times = tS.send_num_times()
seed_value = tS.seed_setter()
out_put_path = f"../../CellModel/simulation_Files/E_values({seed_value}).txt"
num_times = tS.send_num_times()
output_array, sens_val, res_val, pers_val, total_val = tS.run_Sim()

parameter_list_str = [i for i in range(1, num_times)]
parameter = parameter_list_str*len(sens_val)

output_path = f"../../CellModel/simulation_Files/excel_file({seed_value}).xlsx"
excel_writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
df = output_array.T
sheet_name = 'Sheet1'
df.to_excel(excel_writer, sheet_name=sheet_name, index=True, header=True)
excel_writer.close()

# Plot the data
df = pd.DataFrame({
    "Parameter": parameter,
    "Sensitive cells": [val for sublist in sens_val for val in sublist],
    "Resistant cells": [val for sublist in res_val for val in sublist],
    "Persistent cells": [val for sublist in pers_val for val in sublist],
    "Total cells": [val for sublist in total_val for val in sublist]
})

sns.set_theme(style="ticks")
plt.figure(figsize=(12, 8))
ax1 = sns.lineplot(data=pd.melt(df, ["Parameter"]), x="Parameter", y="value", hue="variable", errorbar="sd")
sns.color_palette()
ax1.set(xlabel="Timesteps", title="Variation of Cell population", ylabel="Cell population")
plt.legend(title="Cell type", loc="upper left")
plt.savefig(f'../../CellModel/simulation_Files/plot_{seed_value}.png')

stop = timeit.default_timer()
print('Time: ', stop - start)

print("End simulation")

# these are the important parameters
g = open(f"../../CellModel/simulation_Files/parameters_file({seed_value}).txt", "w")
start_treat, stop_treat, inter_steps, factor_slow, factor_kill, treat_cell_kill, treat_cell_slow, inter_treat, control_treat, factor_kill_pers, factor_slow_pers, per_change = tS.send_parameters()
cM.write_parameters(g, seed_value, start_treat, stop_treat, inter_steps, factor_slow, factor_kill ,treat_cell_kill, treat_cell_slow, inter_treat, control_treat, factor_kill_pers, factor_slow_pers, per_change)





