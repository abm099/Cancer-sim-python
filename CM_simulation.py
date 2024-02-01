import timeStep as tS
import numpy as np
import pandas as pd
import cellMatrix as cM
import seaborn as sns
import matplotlib.pyplot as plt
import timeit

start = timeit.default_timer()

print("Start simulation")

seed_value = tS.seed_setter()

print("seed value")
out_put_path = f"../../CellModel/simulation_Files/E_values({seed_value}).txt"
num_times = tS.send_num_times()
parameter_list, e_values = tS.parameter_testing(out_put_path)
# data_array = np.array(output_array)
# n = data_array.shape


# print(f"e_values: {e_values}")
h = open(f"../../CellModel/simulation_Files/parameters_file({seed_value}).txt", "w")
for e_value in e_values:
    print(e_value)
    h.write(str(e_value) + '\n')

# Plot the data
df = pd.DataFrame({'Parameter': parameter_list, 'Cycles of Treatment': e_values})
sns.set_theme(style="whitegrid")
sns.lineplot(x="Parameter", y="Cycles of Treatment", data=df, errorbar='sd')
plt.title("Treatment delay vs Cycles of Treatment")
plt.savefig(f'../../CellModel/results/plot_{seed_value}.png')
plt.show()

# Run the simulation and get the data array

# sheet_numbers,x = 0 ,249
# for x in n:
#     sheet_numbers += 1 
# print(f"Number of simulations: {n}")

# output_path = f"../../CellModel/simulation_Files/excel_file({seed_value}).txt"
# # Create a Pandas DataFrame from your data_array
# df = pd.DataFrame(data_array, columns=range(num_cols), index=range(1, num_rows + 1))
# excel_writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
# for param, output_tuple in zip(parameter_list, output_array):
#     e_values = [output_tuple[4]]
#     df_param = pd.DataFrame({'Parameter': [param], 'e': e_values})
#     sheet_name = f'Parameter_{param}'
#     df_param.to_excel(excel_writer, sheet_name=sheet_name, index=False, header=False)
#     workbook = excel_writer.book
#     worksheet = excel_writer.sheets[sheet_name]
#     worksheet.write(0, 0, "Parameter") 
#     worksheet.write(0, 1, "e") 
#     header_format = workbook.add_format({'bold': True, 'align': 'center'})
#     for col_num, value in enumerate(["Parameter", "e"]):
#         worksheet.write(1, col_num, value, header_format)

# # Write the main DataFrame to a separate sheet (optional)
# df.to_excel(excel_writer, sheet_name='Sheet1', index=True, header=False)

# excel_writer.close()

# these are the important parameters
# start_treat, stop_treat, inter_steps, factor_slow, factor_kill, treat_cell_kill, treat_cell_slow, inter_treat, control_treat, factor_kill_pers, factor_slow_pers, per_change = tS.send_parameters()
# cM.write_parameters(seed_value, start_treat, stop_treat, inter_steps, factor_slow, factor_kill ,treat_cell_kill, treat_cell_slow, inter_treat, control_treat, factor_kill_pers, factor_slow_pers, per_change)

stop = timeit.default_timer()
print('Time: ', stop - start)

print("End simulation")



