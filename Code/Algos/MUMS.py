#Model Utility Maximization Algorithm

import numpy as np
from Classes.Model import Model
from Classes.ED import ED
from typing import List, Set
from SingletonUM import SUM

def utilized_storage(X: Set[Model]) -> float: #total storage utilized by cached models

   return sum(model.storage for model in X if model is not None)

def pot_offloaders(EDs: List[ED], model: Model) -> Set[ED]: #list of potential offloaders for a particular model

    Nx = {device for device in EDs if(device.model.name == model.name)}
    return Nx

def maxutil(EDs: List[ED], J: Set[Model]) -> Model:
    utility_to_size = dict()

    for model in J:

        Nj = pot_offloaders(EDs, model)
        utility_to_size[model] = (len(Nj)/model.storage)
    
    if(utility_to_size != dict()): return max(utility_to_size, key=utility_to_size.get)

def MUMS(EDs: List[ED], J: set, W: float, F: float, S: float): 
    X: Set[Model] = set() #set of cached models
    Ux: int = 0 #utility gained by caching models X
    Nx: List[Model] = []
    while(utilized_storage(X) <= S and J != Set[Model]):

        sj = utilized_storage(X)
        j_ = maxutil(EDs, J)

        if (j_ == None): break

        if(S>= utilized_storage((X.union({j_})))): X.add(j_)

        J.discard(j_)
    
    
    for model in X:
        pot_offl = pot_offloaders(EDs, model)
        pot_offl = list(pot_offl)
        Nx += pot_offl

    NxO, UxNxO = SUM(X, Nx)
    return X, NxO, UxNxO