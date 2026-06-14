from Classes.ED import ED
from Classes.Model import Model
from test import layer
import numpy as np
from ServerRA import SRA
from ServerRA_i import SRA_i

mobilenet = Model(
    name="MobileNet",
    storage=250,  # MB
    layers= layer(5)
)

resnet18 = Model(
    name="Resnet18",
    storage=350,
    layers=layer(18)
)

resnet50 = Model(
    name="Resnet50",
    storage=550,
    layers=layer(50)
)

# Wi_list=[]
# Fi_list=[]

# UxNoX: float = 0
# g = 0.1
# F = 800e9 #Computation Resources on ES in FLOPS
# W = 20e6  #Bandwidth of Server 
# # print(W)
# ratios=np.arange(g,1.1,g)
# print(*ratios)
# pi_max=float('-inf')

# print(W)
# w_values=ratios*W
# print(*w_values)

# print(F)
# f_values=ratios*F
# print(*f_values)

# for w_i in w_values:
#     print(f"wi: {w_i}")
#     for f_i in f_values:
#         print(f"fi: {f_i}")
#         if w_i >= W:
#                 print("w_i >= W")
#                 continue

#         if f_i >= F:
#                 print("f_i >= F:")
#                 continue

#         if W <= 0 or F <= 0:
#                 print("W <= 0 or F <= 0")
#                 break

#         best_partition, best_delay, best_rl, best_ru, _ = ed.offloading_decision(w_i, f_i, 0.01) #sigma hardcoded for single server edge case scenario
#         print(best_partition, best_delay, best_rl, best_ru)

#         if best_partition != -1 and best_delay <= ed.task_deadline:

#                 local_delay = ed.local_inference_time() / ed.local_comp_res #eqn (2)

#                 C_i_0 = (  #eqn (8)
#                             local_delay
#                             * (ed.local_comp_res ** 2)
#                             * ed.energy_consumption_param
#                             * 0.1
#                     )
                
#                 print(f"Ci: {C_i_0}")

#                 pi_i = (
#                             C_i_0
#                             - best_rl * ((ed.local_comp_res ** 2) * ed.energy_consumption_param * 0.1)
#                             - best_ru * (ed.transmission_power * ed.transmision_antenna_power_eff_param * 0.1)
#                     )
                
#                 print(f"pi: {pi_i}")


# #                 # Select wi, fi corresponding to pi
#                 if pi_i > pi_max:
#                         pi_max = pi_i
#                         wi_final = w_i
#                         fi_final = f_i

#                         # print(pi_max)
#                         # print(wi_final)
#                         # print(fi_final)


# #         #we will store best value
# if(wi_final != 0 and fi_final != 0 and pi_max!=float("-inf")):
#     print(wi_final, fi_final, pi_max)

            # Wi_list.append(wi_final)
            # Fi_list.append(fi_final)

#         #and update the remaining resources
        # W -= wi_final
        # F -= fi_final

#         #and update utility only if pi is not -inf
      

# print(*Wi_list)
# print(*Fi_list)
# print(UxNoX)

# print(SRA_i(ed, 20e6, 800e9))

EDs = [

    # MobileNet users
    ED(
        local_comp_res=12,
        model=mobilenet,
        task_deadline=5,
        # local_computation_power=2,
        channel_coefficient=0.5,
        transmission_power=80e-3,
        energy_consumption_param=0.5,
        transmision_antenna_power_eff_param=0.75
    ),

    ED(
        local_comp_res=10,
        model=mobilenet,
        task_deadline=2,
        # local_computation_power=2,
        channel_coefficient=0.2,
        transmission_power=25e-3,
        energy_consumption_param=0.7,
        transmision_antenna_power_eff_param=0.80
    ),

    ED(
        local_comp_res=13,
        model=mobilenet,
        task_deadline=4,
        # local_computation_power=3,
        channel_coefficient=0.35,
        transmission_power=10e-3,
        energy_consumption_param=0.3,
        transmision_antenna_power_eff_param=0.82
    ),

    ED(
        local_comp_res=10,
        model=resnet18,
        task_deadline=1,
        # local_computation_power=3,
        channel_coefficient=0.75,
        transmission_power=50e-3,
        energy_consumption_param=0.95,
        transmision_antenna_power_eff_param=0.85
    ),

    ED(
        local_comp_res=15,
        model=mobilenet,
        task_deadline=6,
        # local_computation_power=4,
        channel_coefficient=0.95,
        transmission_power=50e-3,
        energy_consumption_param=0.45,
        transmision_antenna_power_eff_param=0.88
    ),

    ED(
        local_comp_res=10,
        model=resnet50,
        task_deadline=6,
        # local_computation_power=5,
        channel_coefficient=1,
        transmission_power=100e-3,
        energy_consumption_param=0.15,
        transmision_antenna_power_eff_param=0.90
    )
]

# for ed in EDs:
#     print(SRA_i(ed,20e6, 800e9))

# result= SRA(EDs,20e6, 800e9) #W = 20MHz F = 800 GFlopsPS
# Utility = result[0]
# Wi_list = result[1]
# Fi_list = result[2]

# print(Utility)

# print("Wi_List:")
# for i,j in enumerate(Wi_list):
#     print(i,j)

# print("*"*30)
# print("Fi_List:")
# for i,j in enumerate(Fi_list):
#     print(i,j)

models = {mobilenet,resnet18,resnet50}

