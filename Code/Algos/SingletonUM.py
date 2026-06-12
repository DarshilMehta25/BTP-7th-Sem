from Classes.ED import ED
from typing import List
from ServerRA_i import SRA_i

#Singleton Utility Maximization
def SUM(Nx: List[ED], W:float, F: float):
    
    UxSUM = 0
    NxO: List[ED] = []

    while len(Nx) > 0:

        best_density = float('-inf')
        i_ = -1
        selected_utility = 0

        for device in Nx: #yaha jo device hain yo potential hai, matlab NxO me ho bhi sakta hain ya nhi
            U_X_i, Wi, Fi = SRA_i(device,W,F)


            # Avoid Division by 0
            if Fi + Wi == 0:
                continue

            density = (U_X_i/(Wi + Fi))

            if density > best_density:
                best_density = density
                i_ = device
                selected_utility = U_X_i
                selected_w = Wi
                selected_f = Fi
        
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