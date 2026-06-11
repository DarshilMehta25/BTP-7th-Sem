from Classes.ED import ED
import numpy as np

#Server Resource Allocation

def SRA(ed: ED, W: int, F: int):

    UxNoX: int = 0
    Wi_list: list[float] = []
    Fi_list: list[float] = []
    pi_max = float('-inf')

    g = 0.1
    ratios=np.arange(g,0.6,g)

    w_values=ratios*W
    f_values=ratios*F

    for w_i in w_values:
        for f_i in f_values:

            if w_i >= W:
                continue

            if f_i >= F:
                continue

            if W <= 0 or F <= 0:
                break

        best_partition, best_delay, best_rl, best_ru, _ = ed.offloading_decision(w_i, f_i, 100) #sigma hardcoded for single server edge case scenario

        if best_partition != -1 and best_delay <= ed.task_deadline:

                local_delay = ed.local_inference_time(best_partition) / ed.local_comp_res #eqn (2)

                C_i_0 = (  #eqn (8)
                            local_delay
                            * (f_i ** 2)
                            * ed.energy_consumption_param
                            * 0.1
                    )


                pi_i = (
                            C_i_0
                            - best_rl * ((f_i ** 2) * ed.energy_consumption_param * 0.1)
                            - best_ru * (ed.transmission_power * ed.transmision_antenna_power_eff_param * 0.1)
                    )


                # Select wi, fi corresponding to pi
                if pi_i > pi_max:
                        pi_max = pi_i
                        wi_final = w_i
                        fi_final = f_i


        #we will store best value
        Wi_list.append(wi_final)
        Fi_list.append(fi_final)

        #and update the remaining resources
        W -= wi_final
        F -= fi_final

        #and update utility only if pi is not -inf
        if (pi_max != float('-inf')):
            UxNoX += pi_max

    return UxNoX, Wi_list, Fi_list