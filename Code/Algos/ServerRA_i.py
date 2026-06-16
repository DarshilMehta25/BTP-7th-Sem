from Algos.Classes.ED import ED
from Algos.Classes.ED import ED
import numpy as np

#Server Resource Allocation fir Each Device

def SRA_i(ed: ED, W: float, F: float):
    pi_max = float('-inf')
    
    wi_final = 0
    fi_final = 0

    if W <= 0 or F <= 0:
        return pi_max, wi_final, fi_final
    
    g = 0.1
    ratios=np.arange(g,0.6,g)

    w_values=ratios*W
    # print(*w_values)

    f_values=ratios*F
    # print(*f_values)

    local_delay = ed.local_inference_time() / ed.local_comp_res #eqn (2)

    C_i_0 = (  #eqn (8)
                            local_delay
                            * (ed.local_comp_res ** 2)
                            * ed.energy_consumption_param
                            * 0.1
            )
    # print(C_i_0)

    
    for w_i in w_values:
        # print(f"wi: {w_i}")
        for f_i in f_values:
            # print(f"fi: {f_i}")
            if w_i > W:
                continue

            if f_i > F:
                continue

            if W <= 0 or F <= 0:
                break

            best_partition, best_rl, best_ru, _ = ed.offloading_decision(w_i, f_i, 0.01) #sigma hardcoded for single server edge case scenario
            # print(best_partition, best_delay, best_rl, best_ru)

            if best_partition != -1 :

                pi_i = (
                            C_i_0
                            - best_rl * ((ed.local_comp_res ** 2) * ed.energy_consumption_param * 0.1)
                            - best_ru * (ed.transmission_power * ed.transmision_antenna_power_eff_param * 0.1)
                    )
                # print(pi_i)

                # pi_i -= (pw * w_i + pf * f_i)

                # Select wi, fi corresponding to pi
                if pi_i > pi_max:
                        pi_max = pi_i
                        wi_final = w_i
                        fi_final = f_i

                        # print(pi_max)
                        # print(wi_final)
                        # print(fi_final)

                        W -= wi_final
                        F -= fi_final

    return pi_max, wi_final, fi_final