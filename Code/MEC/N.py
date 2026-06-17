import os,sys

current_dir = os.path.dirname(os.path.abspath(__file__))
# print(current_dir)
project_root = os.path.dirname(current_dir)
# print(project_root)
if project_root not in sys.path:
    sys.path.append(project_root)
# print(sys.path)

from Algos.Classes.ED import ED
import random
from J import J

#File contains ED to simulate Collaborative inference

#For simulation of MUMS,SRA, all devices have randomly assigned models
EDs = []
for _ in range(50):
    ed = ED(
        local_comp_res=random.uniform(10, 15) * 1e9,               # Unif[10, 15] GFLOPS
        model=random.choice(J),                                           # Models assigned randomly 
        task_deadline=random.uniform(3, 6),                        # Unif[3, 6] s
        channel_coefficient=random.uniform(0.1, 1.0),              # Unif[0.1, 1]
        transmission_power=random.uniform(10, 100) * 1e-3,         # Unif[10, 100] mW
        energy_consumption_param=random.uniform(0.1, 1.0),         # Unif[0.1, 1]
        transmision_antenna_power_eff_param=random.uniform(0.5, 1.0) # Unif[0.5, 1]
    )
    EDs.append(ed)
# print(len(EDs))

#For simulation of SUM, all devices are assignet with a single Model
EDs_SUM = []
for _ in range(50):
    ed = ED(
        local_comp_res=random.uniform(10, 15) * 1e9,               # Unif[10, 15] GFLOPS
        model= J[0],                                               # strictly assignet googlenet
        task_deadline=random.uniform(3, 6),                        # Unif[3, 6] s
        channel_coefficient=random.uniform(0.1, 1.0),              # Unif[0.1, 1]
        transmission_power=random.uniform(10, 100) * 1e-3,         # Unif[10, 100] mW
        energy_consumption_param=random.uniform(0.1, 1.0),         # Unif[0.1, 1]
        transmision_antenna_power_eff_param=random.uniform(0.5, 1.0) # Unif[0.5, 1]
    )
    EDs_SUM.append(ed)
# print(EDs_SUM[0])
# print(len(EDs_SUM))