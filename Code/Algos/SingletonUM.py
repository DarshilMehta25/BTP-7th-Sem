from Classes.ED import ED
from typing import List

def SUM(X: set, Nx: List[ED]):
    
    UxSUM = 0
    NxO: List[ED] = []

    while len(Nx) > 0:

        best_density = float('-int')
        i_ = -1
        selected_utility = 0

        for device in Nx:
            U_X_i, Wi_list, Fi_list = SRA(device,W,F)
            total_w = sum(Wi_list)
            total_f = sum(Fi_list)

            # Avoid Division by 0
            if total_w + total_f == 0:
                continue

            density = (U_X_i/(total_w + total_f))

            if density > best_density:
                best_density = density
                i_ = device
                selected_utility = U_X_i
                selected_w = total_w
                selected_f = total_f
        
        if i_ == -1: #No feasible user
            break

        NxO.append(i_)
        Nx.remove(i_)
        UxSUM += selected_utility

        W -= selected_w
        F -= selected_f

        if W <= 0 or F <= 0: #Resource Exhausted
            break

    
    return UxSUM, NxO
