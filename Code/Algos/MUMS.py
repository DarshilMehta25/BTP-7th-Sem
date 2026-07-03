#Model Utility Maximization Algorithm

import numpy as np
from Algos.Classes.Model import Model
from Algos.Classes.ED import ED
from typing import List, Set
from Algos.SingletonUM import SUM

def utilized_storage(X: Set[Model]) -> float: #total storage utilized by cached models

   return sum(model.storage for model in X if model is not None)

def pot_offloaders(EDs: List[ED], model: Model) -> Set[ED]: #list of potential offloaders for a particular model

    Nx = {device for device in EDs if(device.model.name == model.name)}
    return Nx

def maxutil(EDs: List[ED], J: Set[Model], W: float, F: float) -> Model: #utility calculate kese ki hain ke jitne device ko model chahie
    utility_to_size = dict()

    for model in J:

        Nj = pot_offloaders(EDs, model)
        model_utility, _ = SUM(Nj, W, F)
        utility_to_size[model] = (model_utility/model.storage)
    
    if(utility_to_size != dict()): return max(utility_to_size, key=utility_to_size.get)

def MUMS(EDs: List[ED], J: List[Model], W: float, F: float, S: int):



    J = J.copy()   # make local copy else giving error of empty list vala in assignment of the model


    X: Set[Model] = set() #set of cached models
    Nx: List[ED] = []

    while(utilized_storage(X) <= S and J != set()):

        j_ = maxutil(EDs, J, W, F) #Model return kare, single

        if (j_ == None): break

        if(S>= utilized_storage((X.union({j_})))): X.add(j_)

        # J.discard(j_) #If J is set
        J.remove(j_) #If J is list
    
    
    for model in X:
        pot_offl = pot_offloaders(EDs, model)
        pot_offl = list(pot_offl)
        # print(f"Potential Offloaders: {model.name} are {pot_offl}")
        Nx += pot_offl
        # print(Nx)

    UxNxO, NxO = SUM(Nx,W,F)
    
    return X, NxO, UxNxO