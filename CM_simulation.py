import timeStep as tS
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import time

num_times = tS.send_num_times()
seed_value = tS.seed_setter()
parameter_list_3 = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
parameter_list = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0]
parameter_list_2 = [0.25, 0.5, 0.75]

def string_list_conversion(testing_type, i):
    if isinstance(testing_type, list): 
        if len(testing_type) != 1: 
            return testing_type[i+1]
    else:
        return testing_type

type_of_simulation = "perturbation"
start_time = time.time()
output_array, out_put_names, e_vales, f_vales, g_vales, h_vales = tS.parameter_testing(parameter_list_3, 5, type_of_simulation, parameter_list, parameter_list_2)
end_time = time.time()
notes_df = pd.DataFrame({"Notes": [out_put_names]})
j = 0
type_sim = "Perturbation Reference Lib"
output_path = f"../../CellModel/simulation_Files/file_({type_sim}).xlsx"
excel_writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
for i, df in output_array.items(): 
    testing_types = string_list_conversion(type_of_simulation, j)
    df = df.T
    sheet_name = f'{i}_{testing_types}'
    df.to_excel(excel_writer, sheet_name=sheet_name, index=True, header=True)
    j += 1
notes_df.to_excel(excel_writer, sheet_name='Vars', index=False, header=False)
excel_writer.close()

para = [x for x in range(1,num_times)]
para = para* len(e_vales[0]*len(e_vales))

e_values =  [val for sublist in e_vales for subsublist in sublist for val in subsublist]
f_values =  [val for sublist in f_vales for subsublist in sublist for val in subsublist]
g_values =  [val for sublist in g_vales for subsublist in sublist for val in subsublist]
h_values =  [val for sublist in h_vales for subsublist in sublist for val in subsublist]


# Plot the data
sns.set_theme(style="ticks")
plt.figure(figsize=(12, 8))
df = pd.DataFrame({
    "Timesteps": para,
    "Sens": e_values,
    "Res": f_values,
    "Pers": g_values,
    "Total": h_values
})
df_melt = df.melt('Timesteps', var_name='Cell population', value_name='Value')

sns.set_theme(style="ticks")
ax1 = sns.lineplot(df_melt, x="Timesteps", y="Value", hue="Cell population", errorbar="sd")
ax1.set(xlabel="Timesteps", title="Population Plot", ylabel="Population of Cells")
plt.savefig(f'../../CellModel/simulation_Files/plot_treat_factors.png')
del ax1
plt.clf()


ax2 = sns.lineplot(df_melt, x="Timesteps", y="Value", hue="Cell population", errorbar="sd")
ax2.set(xlabel="Timesteps", title="Intermittent Treatment Representative", ylabel="Population of Cells")
ax2.set_ylim(0, 250)
plt.savefig(f'../../CellModel/simulation_Files/plot_treat_factors_adjusted.png')
del ax2
plt.clf()

