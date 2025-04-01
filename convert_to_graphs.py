import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os


root_path = "../../CellModel/simulation_Files"

xexcel_file_1 = f"{root_path}/file_(Perturbation Reference Lib).xlsx"

def extract_data_from_sheet(excel_file, sheet_name):
    df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
    # drop the first row and the first column
    df = df.drop(0)
    df = df.drop(df.columns[0], axis=1)
    num = df.shape[1] 
    timesteps = []
    for col in range(0, df.shape[1]):  # Iterate through columns
            start = 0
            end = 0 
            t1 = True
            t2 = True
            for row in range(0, df.shape[0]):  # Iterate through rows
                cell_value = df.iloc[row, col]
                if isinstance(cell_value, str):
                    tuple_values = cell_value.split(",")
                    if len(tuple_values) >= 4:  # Check if tuple has at least 4 elements
                        if int(tuple_values[8].strip(")")) > 0 and t1:  # or row == df.shape[0] - 1:
                            start = int(tuple_values[3].strip(")"))
                            t1 = False
                        if int(tuple_values[9].strip(")")) > 0 and t2:
                            end = int(tuple_values[3].strip(")"))
                            t2 = False
                            break
            tim = (end - start)/5
            timesteps.append(tim)
    return timesteps, num, df

def main(excel_file):
    df_dict = {}
    num = 0
    # Open the Excel file
    xls = pd.ExcelFile(excel_file)
    all_data_1 = []
    tumor_size_list = []
    para_2 = []
    for sheet_name in xls.sheet_names:
        if sheet_name == "Vars" or sheet_name == "Default_Params" or sheet_name == "Default_Results":
            continue
        a = sheet_name.split("_")[0]
        b = sheet_name.split("_")[1]
        tumor_size = a
        para2 = b
        list1, num_1, df_1 = extract_data_from_sheet(excel_file, sheet_name)
        df_dict[tumor_size] = df_1
        all_data_1.append(list1)
        num = num_1
        tumor_size_list.append(tumor_size)
        para_2.append(para2)
    return all_data_1, tumor_size_list, para_2, num, df_dict

e_value, parameter_list, para_2, num, df_dic = main(xexcel_file_1)



path = f'{root_path}/AVG_value'
if not os.path.exists(path):
    os.makedirs(path)

e_values = [val for sublist in e_value for val in sublist]
para = [item for item in parameter_list for _ in range(num)]

# Plot the data
sns.set_theme(style="ticks")
plt.figure(figsize=(12, 8))
df = pd.DataFrame({
    "Timesteps": para,
    "Cell population": e_values,
})
df_melt = df.melt('Timesteps', var_name='Cell population', value_name='Value')
path = f'{root_path}/Population_plots'
if not os.path.exists(path):
    os.makedirs(path)
sns.set_theme(style="ticks")
ax1 = sns.barplot(data=df_melt, x="Timesteps", y="Value", hue="Cell population", errorbar="sd")
plt.xlabel("Resuscitation")
ax1.bar_label(ax1.containers[0])
plt.title("Resuscitation vs Max Capacity")
plt.ylabel("Time to reach max capacity")
plt.savefig(f'{path}/Pop_plot.png')
plt.clf()


def pop_plot():
    for key, df in df_dic.items():
        row, col = df.shape
        
        sens_list = []
        res_list = []
        pers_list = []
        total_list = []

        for j in range(0, col):
            list_sens = []
            list_res = []
            list_pers = []
            list_total = []

            for i_row in range(0, row):
                cell_value = df.iloc[i_row, j]  # Access each cell
                
                if isinstance(cell_value, str):  
                    # Unpack the tuple values from the string
                    a, b, c, d, e, f, g, h, treat_on, treat_off = cell_value.strip("()").split(",")

                    # Convert to integers
                    sens = int(a)
                    res = int(b)
                    pers = int(c)
                    cell_pop = int(d)

                    list_sens.append(sens)
                    list_res.append(res)
                    list_pers.append(pers)
                    list_total.append(cell_pop)
            
            sens_list.append(list_sens)
            res_list.append(list_res)
            pers_list.append(list_pers)
            total_list.append(list_total)
        
        timesteps = list(range(1, row + 1)) * col
        sens_list = [item for sublist in sens_list for item in sublist]
        res_list = [item for sublist in res_list for item in sublist]
        pers_list = [item for sublist in pers_list for item in sublist]
        total_list = [item for sublist in total_list for item in sublist]

        df_plot = pd.DataFrame({
            "Timesteps": timesteps,
            "Sens": sens_list,
            "Res": res_list,
            "Pers": pers_list,
            "Total": total_list
        })

        # Reshape the DataFrame for easier plotting with seaborn
        df_melt = df_plot.melt('Timesteps', var_name='Cell Population', value_name='Value')

        sns.set_theme(style="ticks")
        ax1 = sns.lineplot(data=df_melt, x="Timesteps", y="Value", hue="Cell Population", errorbar="sd")
        ax1.set(xlabel="Timesteps", title=f"Population plot for {key}", ylabel="Population of Cells")
        
        path = f'{root_path}/Population_plots'
        if not os.path.exists(path):
            os.makedirs(path)
        plt.savefig(f'{path}/Pop_plot_{key}.png')
        plt.clf()  
    return True

def pop_plot_by_column():
    for key, df in df_dic.items():
        row, col = df.shape
        

        for j in range(0, col):
            list_sens = []
            list_res = []
            list_pers = []
            list_total = []

            for i_row in range(0, row):
                cell_value = df.iloc[i_row, j]  # Access each cell
                
                if isinstance(cell_value, str):  # Ensure the cell contains a string
                    try:
                        # Unpack the tuple values from the string
                        a, b, c, d, e, f, g, h, treat_on, treat_off = cell_value.strip("()").split(",")

                        # Convert to integers
                        sens = int(a)
                        res = int(b)
                        pers = int(c)
                        cell_pop = int(d)
                        
                        # Append values to respective lists
                        list_sens.append(sens)
                        list_res.append(res)
                        list_pers.append(pers)
                        list_total.append(cell_pop)

                    except ValueError as ve:
                        print(f"Error parsing cell at row {i_row}, column {j}: {ve}")
                        continue
            
            timesteps = list(range(1, row + 1))
            df_plot = pd.DataFrame({
                "Timesteps": timesteps,
                "Sens": list_sens,
                "Res": list_res,
                "Pers": list_pers,
                "Total": list_total
            })

            df_melt = df_plot.melt('Timesteps', var_name='Cell Population', value_name='Value')

            sns.set_theme(style="ticks")
            ax1 = sns.lineplot(data=df_melt, x="Timesteps", y="Value", hue="Cell Population", errorbar="sd")
            ax1.set(xlabel="Timesteps", title=f"Population plot for {key}, #{j+1}", ylabel="Population of Cells")

            path = f'{root_path}/Population_plots Individual'
            if not os.path.exists(path):
                os.makedirs(path)
            plt.savefig(f'{path}/Pop_plot_{key}_col_{j+1}.png')
            plt.clf()  # Clear the current plot for the next column

    return True

def combined_pers_plot():
    all_pers = []
    all_timesteps = []
    key_labels = []

    for key, df in df_dic.items():
        row, col = df.shape
        timesteps = list(range(1, row + 1)) * col  # Repeat timesteps for each column

        pers_values = []

        for j in range(0, col):
            for i_row in range(0, row):
                cell_value = df.iloc[i_row, j]  # Access each cell

                if isinstance(cell_value, str):  
                    try:
                        a, b, c, d, e, f, g, h, treat_on, treat_off = cell_value.split(",")
                        pers = int(d)  # Extract 'pers' value

                        pers_values.append(pers)
                    except ValueError as ve:
                        print(f"Error parsing cell at row {i_row}, column {j}: {ve}")
                        continue
        all_pers.extend(pers_values)
        all_timesteps.extend(timesteps[:len(pers_values)])  # Ensure timesteps match the length of pers values
        key_labels.extend([key] * len(pers_values))  # Track the key for labeling the graph

    df_plot = pd.DataFrame({
        "Timesteps": all_timesteps,
        "Pers": all_pers,
        "Key": key_labels
    })

    sns.set_theme(style="ticks")
    ax = sns.lineplot(data=df_plot, x="Timesteps", y="Pers", hue="Key", errorbar="sd")
    ax.set(xlabel="Timesteps", title="Total population across Resistance", ylabel="Cells Population")

    path = f'{root_path}/Combined_plots'
    if not os.path.exists(path):
        os.makedirs(path)
    plt.savefig(f'{path}/Combined_Total_Plot.png')
    plt.clf()  

    return True

def combined_pers_plot_avg():
    all_pers = []
    all_timesteps = []
    key_labels = []

    for key, df in df_dic.items():
        row, col = df.shape
        timesteps = list(range(1, row + 1)) * col  # Repeat timesteps for each column

        pers_values = []

        for j in range(0, col):
            for i_row in range(0, row):
                cell_value = df.iloc[i_row, j]  

                if isinstance(cell_value, str):  
                    try:
                        # Unpack the tuple values from the string
                        a, b, c, d, e, f, g, h, treat_on, treat_off = cell_value.split(",")
                        pers = int(d)  

                        pers_values.append(pers)
                    except ValueError as ve:
                        print(f"Error parsing cell at row {i_row}, column {j}: {ve}")
                        continue

        all_pers.extend(pers_values)
        all_timesteps.extend(timesteps[:len(pers_values)])  
        key_labels.extend([key] * len(pers_values))  

    df_plot = pd.DataFrame({
        "Timesteps": all_timesteps,
        "Pers": all_pers,
        "Key": key_labels
    })

    df_avg = df_plot.groupby(["Timesteps", "Key"]).agg({"Pers": "mean"}).reset_index()

    sns.set_theme(style="ticks")
    ax = sns.lineplot(data=df_avg, x="Timesteps", y="Pers", hue="Key", errorbar="sd")
    ax.set(xlabel="Timesteps", title="Average Population across Resistance", ylabel="Average Cells Population")

    path = f'{root_path}/Combined_plots'
    if not os.path.exists(path):
        os.makedirs(path)
    plt.savefig(f'{path}/Combined_Average_Plot.png')
    plt.clf()  # Clear the current plot for the next run
    return True

def smooth_data(data, window_size=5):
    return data.rolling(window=window_size, center=True).mean()

def dead_plots():
    for key, df in df_dic.items():
        row, col = df.shape
        timesteps = list(range(1, row + 1))
        for j in range(0, col):
            list_sens = []
            list_res = []
            list_pers = []
            list_total = []
            list_sens_dead = []
            list_res_dead = []
            list_pers_dead = []
            list_total_dead = []
            lsens = 9
            lres = 0
            lpers = 0
            ltotal = 9
            rate_sens = []
            rate_res = []
            rate_pers = []
            rate_total = []
            for i in range(0, row):
                cell_value = df.iloc[i, j]
                a, b, c, d, e, f, g = cell_value.split(",")
                a_cleaned = a.replace('(', '')
                g_cleaned = g.replace(')', '')
                a, b, c, d, e, f, g = int(a_cleaned), int(b), int(c), int(d), int(e), int(f), int(g_cleaned)
                h = e + f + g
                list_sens.append(a)
                list_res.append(b)
                list_pers.append(c)
                list_total.append(d)
                if h == 0:
                    list_sens_dead.append(0)
                    list_res_dead.append(0)
                    list_pers_dead.append(0)
                    list_total_dead.append(0)
                    rate_sens.append((0))
                    rate_res.append((0))
                    rate_pers.append((0))
                    rate_total.append((0))
                else:
                    list_sens_dead.append((e / h) * 100)
                    list_res_dead.append((f / h) * 100)
                    list_pers_dead.append((g / h) * 100)
                    list_total_dead.append(100)  # Total percentage is always 100
                    rate_sens.append((a - lsens) / lsens * 100 if lsens != 0 else 0)
                    rate_res.append((b - lres) / lres * 100 if lres != 0 else 0)
                    rate_pers.append((c - lpers) / lpers * 100 if lpers != 0 else 0)
                    rate_total.append((d - ltotal) / ltotal * 100 if ltotal != 0 else 0)
                    lsens = a
                    lres = b
                    lpers = c
                    ltotal = d

            path = f'../../CellModel/simulation_Files/Delay {key} #{j+1}'
            if not os.path.exists(path):
                os.makedirs(path)

            df_plot = pd.DataFrame({
                "Timesteps": timesteps,
                "Sens": list_sens,
                "Res": list_res,
                "Pers": list_pers,
                "Total": list_total
            })
            df_melt = df_plot.melt('Timesteps', var_name='Cell population', value_name='Value')
            sns.set_theme(style="ticks")
            ax1 = sns.lineplot(df_melt, x="Timesteps", y="Value", hue="Cell population", errorbar="sd")
            ax1.set(xlabel="Timesteps", title="Population plot", ylabel="Population of Cells")
            plt.savefig(f'../../CellModel/simulation_Files/Delay {key} #{j+1}/pp_delay_{key}_#{j+1}.png')
            del df_plot
            plt.clf()
            df_plot_dead = pd.DataFrame({
                "Timesteps": timesteps,
                "Sens": list_sens_dead,
                "Res": list_res_dead,
                "Pers": list_pers_dead
            })
            df_melt_dead = df_plot_dead.melt('Timesteps', var_name='Cell population', value_name='Value')
            sns.set_theme(style="ticks")
            ax2 = sns.lineplot(df_melt_dead, x="Timesteps", y="Value", hue="Cell population", errorbar="sd")
            ax2.set(xlabel="Timesteps", title="Cell death plot", ylabel="# of Dead Cells")
            ax2.set(ylim=(0, 100))
            plt.savefig(f'../../CellModel/simulation_Files/Delay {key} #{j+1}/pp_dead_delay_{key}_#{j+1}.png')
            del df_plot_dead
            plt.clf()

            df_rate_sens = pd.DataFrame({
                "Timesteps": timesteps,
                "Sens": rate_sens
            })
            df_rate_sens = df_rate_sens.apply(smooth_data)
            df_rate_sens = df_rate_sens.melt('Timesteps', var_name='Cell population', value_name='Value')
            ax3 = sns.lineplot(df_rate_sens, x="Timesteps", y="Value", hue="Cell population", palette={"Sens": "#1f77b4"}, errorbar="sd")
            ax3.axhline(0, color='black', linewidth=1)
            ax3.set(xlabel="Timesteps", title="Rate of death of Sensitive cells", ylabel="Rate of death")
            plt.savefig(f'../../CellModel/simulation_Files/Delay {key} #{j+1}/sens_rate_delay_{key}_#{j+1}.png')
            del df_rate_sens
            plt.clf()
            df_rate_res = pd.DataFrame({
                "Timesteps": timesteps,
                "Res": rate_res
            })
            df_rate_res = df_rate_res.apply(smooth_data)
            df_rate_res = df_rate_res.melt('Timesteps', var_name='Cell population', value_name='Value')
            sns.set_theme(style="ticks")
            ax4 = sns.lineplot(df_rate_res, x="Timesteps", y="Value", hue="Cell population", palette={"Res": "#ff7f0e"}, errorbar="sd")
            ax4.axhline(0, color='black', linewidth=1)
            ax4.set(xlabel="Timesteps", title="Rate of death of Resistant cells", ylabel="Rate of death")
            plt.savefig(f'../../CellModel/simulation_Files/Delay {key} #{j+1}/res_rate_delay_{key}_#{j+1}.png')
            del df_rate_res
            plt.clf()
            df_rate_pers = pd.DataFrame({
                "Timesteps": timesteps,
                "Pers": rate_pers
            })
            df_rate_pers = df_rate_pers.apply(smooth_data)
            df_rate_pers = df_rate_pers.melt('Timesteps', var_name='Cell population', value_name='Value')
            sns.set_theme(style="ticks")
            ax5 = sns.lineplot(df_rate_pers, x="Timesteps", y="Value", hue="Cell population", palette={"Pers": "green"}, errorbar="sd")
            ax5.set(xlabel="Timesteps", title="Rate of death of Persistant cells", ylabel="Rate of death")
            ax5.axhline(0, color='black', linewidth=1)
            plt.savefig(f'../../CellModel/simulation_Files/Delay {key} #{j+1}/pers_rate_delay_{key}_#{j+1}.png')
            del df_rate_pers
            plt.clf()

            df_rate = pd.DataFrame({
                "Timesteps": timesteps,
                "Sens": rate_sens,
                "Res": rate_res,
                "Pers": rate_pers
            })
            df_melt_rate = df_rate.melt('Timesteps', var_name='Cell population', value_name='Value')
            sns.set_theme(style="ticks")
            ax6 = sns.lineplot(df_melt_rate, x="Timesteps", y="Value", hue="Cell population", errorbar="sd")
            ax6.set(xlabel="Timesteps", title="Combinded rate of death", ylabel="Rate of death")
            ax6.axhline(0, color='black', linewidth=1)
            plt.savefig(f'../../CellModel/simulation_Files/Delay {key} #{j+1}/pp_rate_delay_{key}_#{j+1}.png')
            del df_rate
            plt.clf()

def avg_plot():
    pop_dict = {}
    for key, df in df_dic.items():
        row, col = df.shape
        sens_list, res_list, pers_list, total_list = [], [], [], []
        for j in range(0, col):
            list_sens = []
            list_res = []
            list_pers = []
            list_total = []
            treat_days = 0
            for i in range(0, row):
                cell_value = df.iloc[i, j]
                a, b, c, d, e, f, g, h, treat_on, treat_off = cell_value.strip("()").split(",")
                list_sens.append(a)
                list_res.append(b)
                list_pers.append(c)
                list_total.append(d)
            sens_list.append(list_sens)
            res_list.append(list_res)
            pers_list.append(list_pers)
            total_list.append(list_total)
    pop_dict[key] = {
            'sens_list': sens_list,
            'res_list': res_list,
            'pers_list': pers_list,
            'total_list': total_list
        }

    flat_dict = {
        'Cell population': [],
        'Value': [],
    }
    for key, lists in pop_dict.items():
        for list_group in lists:
            for sublist in list_group:
                for value in sublist:
                    flat_dict['Cell population'].append(key)
                    flat_dict['Value'].append(value)
    df = pd.DataFrame(flat_dict)
    df_melt = df.melt(id_vars=['Cell population'], var_name='Variable', value_name='Value')

    sns.set_theme(style="ticks")
    ax = sns.lineplot(data=df_melt, x="Cell population", y="Value")
    ax.set(xlabel="Cell population", title="Cell population vs Timesteps", ylabel="Population of Cells")
    plt.savefig(f'../../CellModel/simulation_Files/plot_pop_avg.png')


sns.set_theme(style="ticks")
plt.figure(figsize=(12, 8))
df = pd.DataFrame({
    "Timesteps": para,
    "Sens": e_values,
    # "Res": f_values,
    # "Pers": g_values,
    # "Total": h_values
})
df_melt = df.melt('Timesteps', var_name='Cell population', value_name='Value')

sns.set_theme(style="ticks")
ax1 = sns.lineplot(df, x="Timesteps", y="Sens", errorbar="sd")
ax1.set(xlabel="Resistance Level", title="Persistor Delay vs Max Capacity", ylabel="Max Capacity")
# set the y-axis to start from 0 to 350
# plt.ylim(0, 350)
plt.savefig(f'../../CellModel/simulation_Files/plot_img.png')


ax2 = sns.lineplot(df, x="Timesteps", y="Sens", errorbar="sd")
ax2.set(xlabel="Persistor Delay", title="Persistor Delay vs Max Capacity", ylabel="Max Capacity")
# set the y-axis to start from 0 to 350
plt.ylim(0, 350)
plt.savefig(f'../../CellModel/simulation_Files/plot_img_adj.png')
print("End simulation")