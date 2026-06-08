from typing import List
from Classes.ED import ED
import numpy as np

#Server Resource Allocation

def SRA(NxO: List[ED], W: int, F: int):

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
