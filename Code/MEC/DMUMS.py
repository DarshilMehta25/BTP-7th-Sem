from copy import deepcopy

import os
import pandas as pd
from Algos.Classes.EdgeServer import EdgeServer
from Algos.Classes.ED import ED
from Algos.Classes.Model import Model
from Algos.MUMS import utilized_storage, pot_offloaders
from Algos.SingletonUM import SUM
from typing import List, Set
# from MEC.DisCNN import DisCNN


# from dataclasses import dataclass
# from MEC.J import J

# @dataclass
# class ModelUtil:
#     model: Model
#     utility: float
#     eds: List[ED]

"""
Step 1:
EDs lena from print snapshot function

Step 2:
Find out unn mese kitne unique models hain

Step 3:
Calculate Utility/Model Storage ka ratio -> Assume ye EDs ke corresponding batayega

Step 4:
Upar ke class ki list banao, list ko non-increasing sort karo wrt util

Step 5:
while loop kab tab chalega for replacement jab tak storage hain, add from 0th index se jab
har ek baar cache ko pehle se bharna hoga

"""

def minutil(EDs: List[ED], X: Set[Model], W: float, F: float):  # utility calculate for minimum model, so that we can eliminate model which gives minimum utility
    utility_to_size = dict()

    for model in X:
        Nj = pot_offloaders(EDs, model)
        model_utility, _ = SUM(Nj, W, F)
        utility_to_size[model] = (model_utility / model.storage)

    if (utility_to_size != dict()):
        min_util_model = min(utility_to_size, key=utility_to_size.get) #model with minimum utility
        model_util = utility_to_size[min_util_model] #corresponding utility
        return min_util_model, model_util

def calc_util(model: Model, es: EdgeServer, eds: List[ED]): #Calulate utility for new model to cache

    Nj = pot_offloaders(eds, model)

    model_utility, _ = SUM(Nj, es.W, es.F)
    return model_utility/model.storage

def total_util(models: Set[Model], es: EdgeServer, eds: List[ED]):

    total_util = 0.0

    for model in models:
        Nj = pot_offloaders(eds, model)
        model_util,_ = SUM(Nj, es.W, es.F)
        total_util += (model_util/model.storage)

    return total_util


def replace_model(ed: ED, eds: List[ED], es:EdgeServer): #logic to eliminate model
    #Here we eliminate subset of models from X such that its utility as lesser compared to new model for EDs present inside Edge Server area also while satisfying storage constraint such that models swapped out shd guarantee new model accomodation inside X

    print(f"Replace Model function invoked for {ed.id} for {ed.model.name}")
    victim_models: Set[Model] = set() #Victim model ka set
    new_model_util = calc_util(ed.model, es, eds)
    # print(f"Demanded model utility {new_model_util}")
    temp = deepcopy(es.X) #replica of cache used rather than real one
    # print([model.name for model in temp])
    server_storage_left = es.Storage - utilized_storage(es.X)  #Storage left of edge server
    # print(server_storage_left)

    while(ed.model.storage >= server_storage_left and temp != set()): #storage constraints to accomodate new model

        victim_model, util = minutil(eds, temp, es.W, es.F)
        # print(victim_model.name)
        # print(util)

        if(util < new_model_util): #victim model ka utility new model utility se kam hain

            temp.remove(victim_model) #remove from cache
            server_storage_left += victim_model.storage #add to left storage
            victim_models.add(victim_model)
            # print(f"Server storage left {server_storage_left}")
            # print(victim_models)

        else: # victim model utility is more than new model utility
            break

    # print(f"Exited While Loop with model in temp {[model.name for model in temp]}")
    # print(victim_models)

    if(victim_models != set()):
        # print(victim_models)

        if(new_model_util > total_util(victim_models, es, eds)): #utility constraint for accomodating new model

            print(f"Model in {victim_models} to be replaced with demanded model")
            return True, victim_models

        else:
            return False,{}

    else:
        return False, {}




def DMUMS(es: EdgeServer, eds: List[ED]): #Dynamic MUMS
    print("DMUMS invoked")

    for ed in eds:

        if(ed.price_paid == 0): # means ED just connected to ES

            if(ed.model in es.X): #newly connected ED ka model already cached hain
                print(f"Model demanded by {ed.id} already present in cache")
                continue  #abhi kuch mat karo baad mein iski utility calculate karke usko resource allocated karenge agar ho sake to
                #Logic for SUM of newly connected device and giving resources

            else: #newly connected ED ka model cached nahi hain
                print(f"Model demanded by {ed.id} not present in cache")
                server_storage_left = es.Storage - utilized_storage(es.X)  # Storage left of edge server
                # print(f"Server Storage Left {server_storage_left}")
                # print(f"Required Model Storage {ed.model.storage}")

                if(ed.model.storage <= server_storage_left): #to check if model can be cached without elimination of any other model
                    print(f"Model added w/o removing any other model")
                    es.X.add(ed.model) #add kardo bcoz model caching is monotonic wrt utility, means model cache karne se server ki utility badhegi hi as per paper
                    #Logic to calculate SUM and allocate resources

                else: #kisi model ko eliminate karna hoga to allocate new model, if possible
                    print(f"Model replace to accomodate new model")
                    decision, victims = replace_model(ed, eds, es)

                    if(decision):

                        es.X = es.X - victims #eliminate all victim models
                        es.X.add(ed.model) #add new model
                        #logic to allocate resources to newly connected devices with corresponding models

                    else:
                        print("Could not replace any model to accomodate new one")

        else: #means ED is old which was already connected to server and resources were allocated
            # print(f"Old ED {ed.id} already connected ")
            continue


# if __name__ == "__main__":
#
#     from J import J
#     import random
#
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#
#     user_coords_file_path = os.path.join(
#         BASE_DIR,
#         "MUA",
#         "Dataset",
#         "site-optus-melbCBD.csv"
#     )
#
#     edge_server_data = pd.read_csv(user_coords_file_path)
#
#     edge_server_lats = edge_server_data["LATITUDE"].head(5)  # Edge Server Latitude
#     edge_server_longs = edge_server_data["LONGITUDE"].head(5)  # Edge Server Longitude
#     edge_server_coords = pd.DataFrame((edge_server_lats, edge_server_longs))  # Combined coordinates
#
#     server_lat, server_long = edge_server_coords[0]  # Server Coorinates assigned
#     es = EdgeServer(20,
#                     800,
#                     1024,
#                     server_lat,
#                     server_long,
#                     800
#                     )

"""
Case 1:
Without removing new Models are added, small models are used
"""
"""
J = J[0:5] #First 5 models

EDs = []
for i in range(10):
    # print(len(J.J))
    ed = ED(
        local_comp_res=random.uniform(10, 15) * 1e9,  # Unif[10, 15] GFLOPS
        model=random.choice(J),  # Models assigned randomly
        task_deadline=random.uniform(3, 6),  # Unif[3, 6] s
        channel_coefficient=random.uniform(0.1, 1.0),  # Unif[0.1, 1]
        transmission_power=random.uniform(10, 100) * 1e-3,  # Unif[10, 100] mW
        energy_consumption_param=random.uniform(0.1, 1.0),  # Unif[0.1, 1]
        transmision_antenna_power_eff_param=random.uniform(0.5, 1.0),  # Unif[0.5, 1]
        x= 0.0,
        y = 0.0
    )
    EDs.append(ed)

NoX = DisCNN(es, EDs) #Allocated Resources to 10 devices

# print(len(NoX))
# print({eds.model.name for eds in NoX})
# print([models.name for models in es.X])

#Appending additional devices with same model demand w/o removing any from NoX
for i in range(10):
    ed = ED(
        local_comp_res=random.uniform(10, 15) * 1e9,  # Unif[10, 15] GFLOPS
        model=random.choice(J),  # Models assigned randomly
        task_deadline=random.uniform(3, 6),  # Unif[3, 6] s
        channel_coefficient=random.uniform(0.1, 1.0),  # Unif[0.1, 1]
        transmission_power=random.uniform(10, 100) * 1e-3,  # Unif[10, 100] mW
        energy_consumption_param=random.uniform(0.1, 1.0),  # Unif[0.1, 1]
        transmision_antenna_power_eff_param=random.uniform(0.5, 1.0),  # Unif[0.5, 1]
        x= 0.0,
        y = 0.0
    )
    EDs.append(ed)

print("Models b4 DMUMS")
print(len(es.X))
print([models.name for models in es.X])
DMUMS(es, EDs)
print("Models after DMUMS")
print(len(es.X))
print([models.name for models in es.X])
"""

"""
Case 2: 
Large Models used in cache first so we may have to remove some models later on, uske liye NoX mese kush devices ko nikal denge
"""
"""
J_ = J[11:14] #Last 4 Models, biggers ones, combined storage 945 MB

EDs = []
for i in range(10):
    # print(len(J.J))
    ed = ED(
        local_comp_res=random.uniform(10, 15) * 1e9,  # Unif[10, 15] GFLOPS
        model=random.choice(J_),  # Models assigned randomly
        task_deadline=random.uniform(3, 6),  # Unif[3, 6] s
        channel_coefficient=random.uniform(0.1, 1.0),  # Unif[0.1, 1]
        transmission_power=random.uniform(10, 100) * 1e-3,  # Unif[10, 100] mW
        energy_consumption_param=random.uniform(0.1, 1.0),  # Unif[0.1, 1]
        transmision_antenna_power_eff_param=random.uniform(0.5, 1.0),  # Unif[0.5, 1]
        x= 0.0,
        y = 0.0
    )
    EDs.append(ed)

NoX = DisCNN(es, EDs) #Allocated Resources to 10 devices

#NoX mese kuch EDs ko remove kardo, specificall VGG 16 wale devices ko remove kar diya, so uski utility nahi ayegi
NoX = [eds for eds in NoX if eds.model.name != "VGG16"]

J_ = J[10:12] #Model storage 150MB, One Model common
newEDs = []
for i in range(10): #Initialing EDs with one commmon and another new model
    # print(len(J.J))
    ed = ED(
        local_comp_res=random.uniform(10, 15) * 1e9,  # Unif[10, 15] GFLOPS
        model=random.choice(J_),  # Models assigned randomly
        task_deadline=random.uniform(3, 6),  # Unif[3, 6] s
        channel_coefficient=random.uniform(0.1, 1.0),  # Unif[0.1, 1]
        transmission_power=random.uniform(10, 100) * 1e-3,  # Unif[10, 100] mW
        energy_consumption_param=random.uniform(0.1, 1.0),  # Unif[0.1, 1]
        transmision_antenna_power_eff_param=random.uniform(0.5, 1.0),  # Unif[0.5, 1]
        x= 0.0,
        y = 0.0
    )
    newEDs.append(ed)

EDs = NoX + newEDs #combined list of new devices and old devices jisme se VGG 16 wale remove kar diye
print("Models b4 DMUMS")
print(len(es.X))
print([models.name for models in es.X])
# print([eds for eds in NoX if eds.model.name == "VGG16"])
DMUMS(es, EDs)
print("Models after DMUMS")
print(len(es.X))
print([models.name for models in es.X])
"""
