from Algos.Classes.ED import ED
import random
from Algos.Classes.EdgeServer import EdgeServer
from MEC import J
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

# user_coords_file_path = "./MUA/Dataset/users-melbcbd-generated.csv"
# users_data = pd.read_csv(filepath_or_buffer=user_coords_file_path) #Already in DF format just have to filter coordinates with server range

in_range_user_coords = [] #list of user coordinates within range of server
out_of_range_user_coords = [] #list of user coordinates out or range

def initialize_EDs(es:EdgeServer): #Function returns list of ED in a server vicinity

    for i in range(users_data.shape[0] - 1):
        user_lat, user_long = users_data.iloc[i]
        dist = HaversineFormula(user_lat, user_long, es.x, es.y)

        if (dist <= es.coverage_area):
            in_range_user_coords.append((user_lat, user_long))
        else:
            out_of_range_user_coords.append((user_lat, user_long))

    EDs = []
    for i in range(50):
        # print(len(J.J))
        ed = ED(
            local_comp_res=random.uniform(10, 15) * 1e9,               # Unif[10, 15] GFLOPS
            model=random.choice(J.J),                                           # Models assigned randomly
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

def initialize_ED_out(es: EdgeServer): #initialize users out of server range and returns a list of users

    for i in range(users_data.shape[0] - 1):
        user_lat, user_long = users_data.iloc[i]
        dist = HaversineFormula(user_lat, user_long, es.x, es.y)

        if (dist <= es.coverage_area):
            in_range_user_coords.append((user_lat, user_long))
        else:
            out_of_range_user_coords.append((user_lat, user_long))

    EDs = []
    for i in range(50):
        # print(len(J.J))
        ed = ED(
            local_comp_res=random.uniform(10, 15) * 1e9,  # Unif[10, 15] GFLOPS
            model=random.choice(J.J),  # Models assigned randomly
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