import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from MEC.J import J
from MEC.N import initialize_EDs
import pandas as pd
from Algos.Classes.EdgeServer import EdgeServer
from Algos.Classes.ESP import ESP, ED
import random, copy
import time
from typing import Set, List
from Algos.Classes.Model import Model
from Algos.MUMS import utilized_storage
from MEC import Random_Direction_Model

# eds = EDs
# offloaders = EDs_SUM


# results = esp.MUMS(EDs, J, 20, 800, 1024)
# results = esp.SUM(EDs_SUM,20, 800)
# results = esp.SRA(EDs, 20, 800)

# MUMS
# X = results[0] 
# Offl = results[1] #SUM
# Utility = results[2] #SUM
 
# SRA
# Wi_l = results[1]
# Fi_l = results[2]
# no_of_offl = results[3]
# Utility = results[0]

# for models in X:
#     print(models.name)

# for devices in Offl:
#     print(devices.id)

# print(*Wi_l)
# print(*Fi_l)
# print(no_of_offl)
# print(Utility)
#

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
user_coords_file_path = os.path.join(
    BASE_DIR,
    "MUA",
    "Dataset",
    "site-optus-melbCBD.csv"
)

edge_server_data = pd.read_csv(user_coords_file_path)
edge_server_lats = edge_server_data["LATITUDE"].head(5)  # Edge Server Latitude
edge_server_longs = edge_server_data["LONGITUDE"].head(5)  # Edge Server Longitude
edge_server_coords = pd.DataFrame((edge_server_lats, edge_server_longs))  # Combined coordinates
server_lat, server_long = edge_server_coords[0]  # Server Coorinates assigned
es = EdgeServer(20, 800, 1024, server_lat, server_long,500)  # coverage area kept 500meters can be changed later as per server configuration

def Simulate():

    EDs_SUM = []
    for _ in range(50):
        ed = ED(
            local_comp_res=random.uniform(10, 15) * 1e9,               # Unif[10, 15] GFLOPS
            model= J[0],                                               # strictly assignet googlenet
            task_deadline=random.uniform(3, 6),                        # Unif[3, 6] s
            channel_coefficient=random.uniform(0.1, 1.0),              # Unif[0.1, 1]
            transmission_power=random.uniform(10, 100) * 1e-3,         # Unif[10, 100] mW
            energy_consumption_param=random.uniform(0.1, 1.0),         # Unif[0.1, 1]
            transmision_antenna_power_eff_param=random.uniform(0.5, 1.0), # Unif[0.5, 1]
            x = 0.0,
            y = 0.0
        )
        EDs_SUM.append(ed)
    esp = ESP(servers=es)

    EDs = initialize_EDs(es)

    x_values1 = []
    y_values1 = []
    y_values2 = []
    y_values3 = []
    successful_offloaders_mums = []
    successful_offloaders_sra = []
    successful_offloaders_sum = []

    time_of_MUMS_execution=[]
    time_of_SRA_execution=[]
    time_of_SUM_execution=[]

    for i in range(0, len(EDs) + 1, 5):

        curr_EDs = copy.deepcopy(EDs[:i])
        curr_EDs_SUM = copy.deepcopy(EDs_SUM[:i])
        curr_models = copy.deepcopy(J)


        start1=time.time()
        _, Nx01, UxNxO_mums=esp.MUMS(curr_EDs,curr_models,20,800,1024)
        finish1=time.time()

        start2 = time.time()
        UxNoX_sra, _, _, Nx02 = esp.SRA(curr_EDs,20,800)
        finish2 = time.time()

        start3=time.time()
        UxSUM, Nx03 = esp.SUM(curr_EDs_SUM,20,800)
        finish3=time.time()

        # print(f"{i} EDs -> Utility: {UxNxO}")
        x_values1.append(i)
        y_values1.append(UxNxO_mums) #utility from MUMS
        y_values2.append(UxNoX_sra) #utility from SRA
        y_values3.append(UxSUM) #utility from SUM
        time_of_MUMS_execution.append((finish1-start1)/2)
        time_of_SRA_execution.append((finish2-start2)/2)
        time_of_SUM_execution.append((finish3-start3)/2)
        successful_offloaders_mums.append(len(Nx01))
        successful_offloaders_sra.append(Nx02)
        successful_offloaders_sum.append(len(Nx03))

    fig, axs = plt.subplots(3, 1, figsize=(8, 12))

    # MUMS
    axs[0].plot(x_values1, y_values1)
    axs[0].set_title("Dis CNN")
    axs[0].set_xlabel("Number of EDs")
    axs[0].set_ylabel("Max Total Utility")
    axs[0].set_xticks(x_values1)

    # SRA
    axs[1].plot(x_values1, y_values2)
    axs[1].set_title("SRA")
    axs[1].set_xlabel("Offloaders")
    axs[1].set_ylabel("Max Total Utility")
    axs[1].set_xticks(x_values1)

    # SUM
    axs[2].plot(x_values1, y_values3)
    axs[2].set_title("SUM")
    axs[2].set_xlabel("Number of EDs")
    axs[2].set_ylabel("Max Total Utility")
    axs[2].set_xticks(x_values1)

    plt.tight_layout()
    plt.savefig("./Results/Max_Total_Utility.png")
    # plt.show()

    """

    Issue: MUMS() was modifying the original EDs or models objects. Since Python passes objects by reference, changes made in the first call remained for later calls.

    So:

    MUMS(first 2 EDs)  # modifies objects
    MUMS(first 4 EDs)  # uses already modified objects → utility becomes 0

    How deepcopy fixed it:

    curr_EDs = copy.deepcopy(no_of_offloaders[:i])
    curr_models = copy.deepcopy(models)

    deepcopy creates completely new independent objects, so each call to MUMS() starts with fresh data and cannot affect later calls.

    """

    # print("x =", x_values1)
    # print("y =", y_values1)

    # print(*x_values1)
    # print(*y_values1)

    # plt.plot(x_values1, y_values1)
    # plt.xlabel("Number of Offloaders")
    # plt.ylabel("Max Total Utility")
    # plt.title("Number of Offloaders vs Max Total Utility")
    # plt.savefig("no_of_offloadersVSmax_total_utility.png")

    #Number of offloaders vs Total Energy Consumption
    #Number of Offloaders vs Successful Offloaders

    fig, axs = plt.subplots(3, 1, figsize=(8, 12))

    # MUMS
    axs[0].plot(x_values1, successful_offloaders_mums)
    axs[0].set_title("DisCNN")
    axs[0].set_xlabel("Number of EDs")
    axs[0].set_ylabel("Successful Offloaders")
    axs[0].set_xticks(x_values1)
    axs[0].grid(True)

    # SRA
    axs[1].plot(x_values1, successful_offloaders_sra)
    axs[1].set_title("SRA")
    axs[1].set_xlabel("Offloaders")
    axs[1].set_ylabel("Successful Offloaders")
    axs[1].set_xticks(x_values1)
    axs[1].grid(True)

    # SUM
    axs[2].plot(x_values1, successful_offloaders_sum)
    axs[2].set_title("SUM")
    axs[2].set_xlabel("Number of EDs")
    axs[2].set_ylabel("Successful Offloaders")
    axs[2].set_xticks(x_values1)
    axs[2].grid(True)

    plt.tight_layout()
    plt.savefig("./Results/Successful_Offloaders.png", dpi=300)
    # plt.show()


    # for i in successful_offloaders:
    #     print(len(i))
    #Number of Offloaders vs Average Inference Delay



    #Number of Offloaders vs Average Execution Time

    fig, axs = plt.subplots(3, 1, figsize=(8, 12))

    # MUMS
    axs[0].plot(x_values1, time_of_MUMS_execution,
                marker='o')
    axs[0].set_title("DisCNN")
    axs[0].set_xlabel("Number of EDs")
    axs[0].set_ylabel("Average Execution Time (s)")
    axs[0].set_xticks(x_values1)
    axs[0].grid(True)

    # SRA
    axs[1].plot(x_values1, time_of_SRA_execution,
                marker='s')
    axs[1].set_title("SRA")
    axs[1].set_xlabel("Number of Offloaders")
    axs[1].set_ylabel("Average Execution Time (s)")
    axs[1].set_xticks(x_values1)
    axs[1].grid(True)

    # SUM
    axs[2].plot(x_values1, time_of_SUM_execution,
                marker='^')
    axs[2].set_title("SUM")
    axs[2].set_xlabel("Number of EDs")
    axs[2].set_ylabel("Average Execution Time (s)")
    axs[2].set_xticks(x_values1)
    axs[2].grid(True)

    plt.tight_layout()
    plt.savefig("./Results/Avg_Execution_Time.png", dpi=300)
    # plt.show()
    plt.close()

# edge_server_coords_file_path = "./MUA/Dataset/site-optus-melbCBD.csv"
# edge_server_data = pd.read_csv(filepath_or_buffer=edge_server_coords_file_path)

import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

user_coords_file_path = os.path.join(
    BASE_DIR,
    "MUA",
    "Dataset",
    "site-optus-melbCBD.csv"
)

edge_server_data = pd.read_csv(user_coords_file_path)

def DisCNN(es:EdgeServer,
           EDs: List[ED]
           ):

    # edge_server_lats = edge_server_data["LATITUDE"].head(5)  # Edge Server Latitude
    # edge_server_longs = edge_server_data["LONGITUDE"].head(5)  # Edge Server Longitude
    # edge_server_coords = pd.DataFrame((edge_server_lats, edge_server_longs))  # Combined coordinates



    # server = [EdgeServer(20, 800, 1024, 500)]
    esp = ESP(es)
    # EDs = initialize_EDs(es,50) #EDs initialized as within server placement
    #

    # print(*EDs)

    #Test ED Object created for testing changes in SRA function and ED class
    
    # EDs = [   ED(
    #     local_comp_res=10e9,
    #     model=J[0],
    #     task_deadline=6,
    #     # local_computation_power=5,
    #     channel_coefficient=1,
    #     transmission_power=100e-3,
    #     energy_consumption_param=0.15,
    #     transmision_antenna_power_eff_param=0.90
    # )]

    es.X, NxO, _ = esp.MUMS(EDs, J, es) #Model Caching Decision
    es.Utility, Wi_List, Fi_List, no_offloaders = esp.SRA(NxO,es) #Resource Allocation to EDs maximizing utility of ESP

    es.EDs = NxO #assigning EDs which are involved in collaborative inference to server to maintain its record
    es.X = {eds.model for eds in NxO} #Faltu me cache kie hue models nikal jae

    # X = {eds.model for eds in NxO}
    # print(X)
    # print(es.X)
    # X = es.X.intersection(X)
    # print(X)
    # print(es.X)
    # es.X = X
    # print(es.X)

    # print(len(X))
    # print(len(NxO))
    # print(es.Utility)
    # print(no_offloaders)
    return NxO


    # print(*Wi_List)
    # print(*Fi_List)

    # print(*NxO)

if __name__ == "__main__":
    # Simulate() #For Simulation
    DisCNN(es) #For actual Model Caching and Resource Allocation
    # print(models.name for models in es.X)
    # print(es.X)
    # print(utilized_storage(es.X))
    # print(len(es.EDs))
    # print([eds.id for eds in es.EDs])
