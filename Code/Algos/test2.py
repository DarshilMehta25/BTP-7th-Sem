from Classes.ED import ED
from Classes.Model import Model
from test import layer
import numpy as np

mobilenet = Model(
    name="MobileNet",
    storage=250,  # MB
    layers= layer(5)
)

Wi_list=[]
Fi_list=[]

ed =    ED(
        local_comp_res=12e9, 
        model=mobilenet,
        task_deadline=5,
        channel_coefficient=0.5,
        transmission_power=20e-3,
        energy_consumption_param=0.5,
        transmision_antenna_power_eff_param=0.75
    )

UxNoX: float = 0
g = 0.1
F = 800e9 #Computation Resources on ES in FLOPS
W = 20e6  #Bandwidth of Server 
# print(W)
ratios=np.arange(g,1.1,g)
print(*ratios)
pi_max=float('-inf')

print(W)
w_values=ratios*W
print(*w_values)

print(F)
f_values=ratios*F
print(*f_values)

for w_i in w_values:
    print(f"wi: {w_i}")
    for f_i in f_values:
        print(f"fi: {f_i}")
        if w_i >= W:
                print("w_i >= W")
                continue

        if f_i >= F:
                print("f_i >= F:")
                continue

        if W <= 0 or F <= 0:
                print("W <= 0 or F <= 0")
                break

        best_partition, best_delay, best_rl, best_ru, _ = ed.offloading_decision(w_i, f_i, 0.01) #sigma hardcoded for single server edge case scenario
        print(best_partition, best_delay, best_rl, best_ru)

        if best_partition != -1 and best_delay <= ed.task_deadline:

                local_delay = ed.local_inference_time() / ed.local_comp_res #eqn (2)

                C_i_0 = (  #eqn (8)
                            local_delay
                            * (ed.local_comp_res ** 2)
                            * ed.energy_consumption_param
                            * 0.1
                    )
                
                print(f"Ci: {C_i_0}")

                pi_i = (
                            C_i_0
                            - best_rl * ((ed.local_comp_res ** 2) * ed.energy_consumption_param * 0.1)
                            - best_ru * (ed.transmission_power * ed.transmision_antenna_power_eff_param * 0.1)
                    )
                
                print(f"pi: {pi_i}")


#                 # Select wi, fi corresponding to pi
                if pi_i > pi_max:
                        pi_max = pi_i
                        wi_final = w_i
                        fi_final = f_i

                        # print(pi_max)
                        # print(wi_final)
                        # print(fi_final)


#         #we will store best value
if(wi_final != 0 and fi_final != 0 and pi_max!=float("-inf")):
    print(wi_final, fi_final, pi_max)

            # Wi_list.append(wi_final)
            # Fi_list.append(fi_final)

#         #and update the remaining resources
        # W -= wi_final
        # F -= fi_final

#         #and update utility only if pi is not -inf
      

# print(*Wi_list)
# print(*Fi_list)
# print(UxNoX)