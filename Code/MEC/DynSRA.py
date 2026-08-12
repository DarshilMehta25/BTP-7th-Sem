from Algos.Classes.ED import ED
from Algos.Classes.EdgeServer import EdgeServer
from typing import List
from Algos.MUMS import pot_offloaders
from Algos.SingletonUM import SUM
from ServerRA import SRA
from dataclasses import replace

def DynSRA(es: EdgeServer, eds: List[ED]): #Dynamically Deallocates Server Resources from Handed Off devices and Allocates to the ones Handed In

    hand_off_eds = [ed for ed in es.EDs if ed not in eds] #bahar gaye hue EDs
    # print("Handed Off EDs")
    # print(len(hand_off_eds))

    hand_in_eds = [ed for ed in eds if ed not in es.EDs] #bahar se aaye hue
    # print("Handed In EDs")
    # print(len(hand_in_eds))

    potential_offloaders: List[ED] = []

    #Server Resource Deallocation

    for idx,ed in enumerate(hand_off_eds):
        if(ed.price_paid != 0): #ED was connected to server

            es.W += ed.allocated_wi
            es.F += ed.allocated_fi

            hand_off_eds[idx] = replace(ed, allocated_wi=0.0 ,allocated_fi=0.0, price_paid=0.0) #free ed from server resources

        else: #ED was not in collaborative inference hence server resources were not given
            continue

    for models in es.X:

        pot_offls = list(pot_offloaders(hand_in_eds, models)) #potential offloaders of models from newly handed in EDs
        potential_offloaders.extend(pot_offls) #to add elements of list in list we use extend instead of append

    # print("Potential Offloaders")
    # print(len(potential_offloaders))
    # print(potential_offloaders)

    UxSUM, NxO = SUM(potential_offloaders, es.W, es.F) #offloaders maximizing utility of Edge Server
    UxNxO,_,_,succ_offl = SRA(NxO, es) #Allocating server resources to newly added EDs

    # print("Successful Offloaders")
    # print(succ_offl)

    #Updating Server Cache List of EDs
    temp_list = [ed for ed in es.EDs if ed not in hand_off_eds] #remove handed off EDs
    es.EDs = temp_list #update server list of connected devices
    es.Utility = UxNxO #update server utility after change in cached models
    es.EDs.extend(NxO) #add handed in EDs only involved in collaborative inference

    return UxNxO, succ_offl