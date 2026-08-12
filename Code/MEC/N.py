from Algos.Classes.ED import ED
import random
from Algos.Classes.EdgeServer import EdgeServer
from MEC.J import J
import pandas as pd
from MEC.HaverSineFormula import HaversineFormula
# from test2 import EDs
import os,sys

#File contains ED to simulate Collaborative inference
parent_dir = os.path.dirname(os.getcwd())
sys.path.append(parent_dir)
#For simulation of MUMS,SRA, all devices have randomly assigned models

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

user_coords_file_path = os.path.join(
    BASE_DIR,
    "MUA",
    "Dataset",
    "users-melbcbd-generated.csv"
)

users_data = pd.read_csv(user_coords_file_path)

in_range_user_coords = [] #list of user coordinates within range of server
out_of_range_user_coords = [] #list of user coordinates out or range

def initialize_EDs(es:EdgeServer, n: int): #Function returns list of ED in a server vicinity
    # J_ = J[0:10]
    for i in range(users_data.shape[0] - 1):
        user_lat, user_long = users_data.iloc[i]
        dist = HaversineFormula(user_lat, user_long, es.x, es.y)

        if (dist <= es.coverage_area):
            in_range_user_coords.append((user_lat, user_long))
        else:
            out_of_range_user_coords.append((user_lat, user_long))

    EDs = []
    for i in range(n):
        # print(len(J.J))
        ed = ED(
            local_comp_res=random.uniform(10, 15) * 1e9,               # Unif[10, 15] GFLOPS
            model=random.choice(J),                                           # Models assigned randomly
            task_deadline=random.uniform(3, 6),                        # Unif[3, 6] s
            channel_coefficient=random.uniform(0.1, 1.0),              # Unif[0.1, 1]
            transmission_power=random.uniform(10, 100) * 1e-3,         # Unif[10, 100] mW
            energy_consumption_param=random.uniform(0.1, 1.0),         # Unif[0.1, 1]
            transmision_antenna_power_eff_param=random.uniform(0.5, 1.0), # Unif[0.5, 1]
            x = in_range_user_coords[i][0],
            y = in_range_user_coords[i][1]
        )
        EDs.append(ed)
        # print("id(J.J) =", id(J.J))
        # print("len(J.J) =", len(J.J))
        # print(ed.model.name)
        # print(type(J.J))

    return EDs

def initialize_ED_out(es: EdgeServer, n:int): #initialize users out of server range and returns a list of users
    # J_ = J[8:14]
    for i in range(users_data.shape[0] - 1):
        user_lat, user_long = users_data.iloc[i]
        dist = HaversineFormula(user_lat, user_long, es.x, es.y)

        if (dist <= es.coverage_area):
            in_range_user_coords.append((user_lat, user_long))
        else:
            out_of_range_user_coords.append((user_lat, user_long)) #isme out of the coverage area vale EDs aa rhe hai

    EDs = []
    for i in range(n):
        # print(len(J.J))
        ed = ED(
            local_comp_res=random.uniform(10, 15) * 1e9,  # Unif[10, 15] GFLOPS
            model=random.choice(J),  # Models assigned randomly
            task_deadline=random.uniform(3, 6),  # Unif[3, 6] s
            channel_coefficient=random.uniform(0.1, 1.0),  # Unif[0.1, 1]
            transmission_power=random.uniform(10, 100) * 1e-3,  # Unif[10, 100] mW
            energy_consumption_param=random.uniform(0.1, 1.0),  # Unif[0.1, 1]
            transmision_antenna_power_eff_param=random.uniform(0.5, 1.0),  # Unif[0.5, 1]
            x=out_of_range_user_coords[i][0],
            y=out_of_range_user_coords[i][1]
        )
        EDs.append(ed)
        # print("id(J.J) =", id(J.J))
        # print("len(J.J) =", len(J.J))
        # print(ed.model.name)
        # print(type(J.J))

    return EDs

#For simulation of SUM, all devices are assigned with a single Model

# print(EDs_SUM[0])
# print(len(EDs_SUM))