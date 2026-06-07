from typing import List
from Classes.ED import ED
import numpy as np

def SRA(NxO: List[ED], W: int, F: int):

    UxNoX: int = 0
    Wi_list: list[float] = []
    Fi_list: list[float] = []
    pi_max = float('-inf')

    