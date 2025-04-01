import timeStep

 #these are the important parameters
start_treat, stop_treat, inter_steps, factor_slow, factor_kill, treat_cell_kill, treat_cell_slow, inter_treat, control_treat, factor_kill_pers, factor_slow_pers, per_change = timeStep.send_parameters()

# write a function to that the parameters and write them to a file g
def write_parameters(g, num, start, stop, inter_steps, slow, kill, treat_cell_kill, treat_cell_slow, inter_treat, control_treat, factor_kill_pers, factor_slow_pers, per_change):
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
    g.write(f"Adaptive treatment: {control_treat}\n")
    g.write(f"Constant treatment: {not (control_treat and inter_treat)}\n")
    g.close()
# write_parameters(g, seed_value, start_treat, stop_treat, inter_steps, factor_slow, factor_kill ,treat_cell_kill, treat_cell_slow, inter_treat, control_treat, factor_kill_pers, factor_slow_pers, per_change)

# print("End simulation")

# Commmit changes to the repository