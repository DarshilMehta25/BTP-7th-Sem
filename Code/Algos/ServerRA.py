from Classes.ED import ED
import numpy as np
from typing import List
from ServerRA_i import SRA_i
from Classes.ED import ED
import numpy as np
from typing import List
from ServerRA_i import SRA_i

#Server Resource Allocation

def SRA(NoX: List[ED], W: float, F: float):

    how_many_get_res=0

    UxNoX: float = 0
    Wi_list: list[float] = []
    Fi_list: list[float] = []

    # pi_max = float('-inf')

    # wi_final = 0
    # fi_final = 0

    # g = 0.1
    # ratios=np.arange(g,1.1,g)

    # w_values=ratios*W
    # print(*w_values)

    # f_values=ratios*F
    # print(*f_values)

    for ed in NoX:
       
     result = SRA_i(ed, W, F)
     # print(ed.id, result)
       
     if result is None:
            continue
       
     utility, wi, fi = result
     # print(utility, wi, fi)

     if utility > 0 and wi > 0 and fi > 0:
                
          UxNoX += utility
          Wi_list.append(wi)
          Fi_list.append(fi)
                
          W -= wi
          F -= fi
          how_many_get_res += 1

     else:

          Wi_list.append(0.0)
          Fi_list.append(0.0)

        # local_delay = ed.local_inference_time()/ed.local_comp_res
        # C_i_0 = (  #eqn (8)
        #                         local_delay
        #                         * (ed.local_comp_res ** 2)
        #                         * ed.energy_consumption_param
        #                         * 0.1
        #     )
        #     # print(C_i_0)
        # for w_i in w_values:
        #     # print(f"wi: {w_i}")
        #     for f_i in f_values:
        #         # print(f"fi: {f_i}")
        #         if w_i > W:
        #             continue

        #         if f_i > F:
        #             continue

        #         if W <= 0 or F <= 0:
        #             break

        #         best_partition, best_delay, best_rl, best_ru, _ = ed.offloading_decision(w_i, f_i, 0.01) #sigma hardcoded for single server edge case scenario
        #         # print(best_partition, best_delay, best_rl, best_ru)

        #         if best_partition != -1 and best_delay <= ed.task_deadline:
        #             pi_i = (
        #                         C_i_0
        #                         - best_rl * ((ed.local_comp_res ** 2) * ed.energy_consumption_param * 0.1)
        #                         - best_ru * (ed.transmission_power * ed.transmision_antenna_power_eff_param * 0.1)
        #                 )
                    
        #             # print(pi_i)


        #             # Select wi, fi corresponding to pi
        #             if pi_i > pi_max:
        #                     pi_max = pi_i
        #                     wi_final = w_i
        #                     fi_final = f_i

        #                     # print(pi_max)
        #                     # print(wi_final)
        #                     # print(fi_final)


        #     #we will store best value
        #     if(wi_final != 0 and fi_final != 0):
        #         Wi_list.append(wi_final)
        #         Fi_list.append(fi_final)

        #     #and update the remaining resources
        #     W -= wi_final
        #     F -= fi_final

        #     #and update utility only if pi is not -inf
        #     if (pi_max != float('-inf')):
        #         UxNoX += pi_max

    return UxNoX, Wi_list, Fi_list, how_many_get_res
    # return UxNoX, Wi_list, Fi_list
