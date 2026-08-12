from MEC.DMUMS import DMUMS
from MEC.DisCNN import DisCNN
from MEC.DynSRA import DynSRA
from MEC.N import initialize_EDs, initialize_ED_out
import os
from MEC.DynMCS import DynMCS
import pandas as pd
from Algos.Classes.EdgeServer import  EdgeServer
from MEC.simulate_global_snapshot_with_time import run
import matplotlib.pyplot as plt
from Code.BaseLineAlgos.PMC import PMC
import time
import numpy as np
from MUMS import utilized_storage
from Algos.MUMS import MUMS
from MEC.J import J
from typing import List
from Algos.Classes.ED import ED

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

server_lat, server_long = edge_server_coords[3]  # Server Coorinates assigned
es = EdgeServer(
    20,
    800,
    1024,
    server_lat,
    server_long,
    800 #Server Range in Meters
)

# EDs_in = initialize_EDs(es) #server ki range me ED
# EDs_out = initialize_ED_out(es) #server ke bahar

#Change 1 added parameter in N file functions
#Change 2 added parameter of inner EDs in DisCNN
#Change 3 added parameter in run function of gloabal snapshot that takes NoX, outside EDs as parameter
#Change 4 run ke andar modify karke andar DMUMS invoke kia for each snapshot
#Change 5 in simulate global function wala file, comment out es, all_eds as neccessary, same for DisCNN file
#Change 6 agar sidha simulate global chalana hain for that, DisCNN se ED parameter remove; invoke DisCNN in the former file, comment first defination of all_eds, run mein comment out NoX, outer_eds, initialize es defined in local file, after all this run file....

def simulate_mcs():
    no_of_devices = []
    models_added_mums = []
    models_added_dmums = []
    models_added_pmc = []
    models_added_dynmcs = []
    models_removed_dmums = []
    models_removed_mums = []
    models_removed_pmc = []
    models_removed_dynmcs = []
    server_storage_left_dmums = []
    server_storage_left_pmc = []
    server_storage_left_mums = []
    server_storage_left_dynmcs = []
    execution_time_dmums = []
    avg_execution_time_dmums = []
    execution_time_pmc = []
    avg_execution_time_pmc = []
    execution_time_mums = []
    avg_execution_time_mums = []
    execution_time_dynmcs = []
    avg_execution_time_dynmcs = []

    for i in range(10,101,10): #5 ke gap mein EDs initialize honge andar bahar

        no_of_devices.append(2*i)
        print(f"Total Devices initialized {i+i}")

        EDs_in = initialize_EDs(es,i) #i jitne andar
        EDs_out = initialize_ED_out(es,i) #i jitne bahar

        NoX = DisCNN(es,
                     EDs_in
                     ) #jitne andar hain unko pehle statically assign karo resources
        X1 = es.X.copy()
        print("Models Assigned Statically using DisCNN Framework")
        print({models.name for models in es.X})

        snapshots = run(NoX, EDs_out, es,10) #run for moving users and dynamic caching decision

        for t in sorted(snapshots):
            # print(snapshots[t])
            # print(type(snapshots[t]))
            start_time = time.time()
            DMUMS(es,snapshots[t])
            end_time = time.time()
            execution_time_dmums.append((end_time - start_time))

        avg_execution_time_dmums.append(np.mean(execution_time_dmums))
        execution_time_dmums.clear()

        print("Models in Cache After DMUMS: ")
        print({models.name for models in es.X})

        print("*"*50)
        X2  = es.X.copy()
        X_ = X2 - X1

        print("Models added DMUMS:")
        print({models.name for models in X_})
        models_added_dmums.append(len(X_))

        X_ = X1 - X2
        print("removed DMUMS:")
        print({models.name for models in X_})
        models_removed_dmums.append(len(X_))

        server_storage_left_dmums.append(es.Storage - utilized_storage(es.X))

        print("=="*50)

        for t in sorted(snapshots):
            start_time = time.time()
            PMC(es, snapshots[t])
            end_time = time.time()
            execution_time_pmc.append((end_time - start_time))

        avg_execution_time_pmc.append(np.mean(execution_time_pmc))
        execution_time_pmc.clear()

        print("Models in Cache After PMC: ")
        print({models.name for models in es.X})
        print("*"*50)
        X3 = es.X.copy()

        X_ = X3 - X1
        print("Models added PMC:")
        print({models.name for models in X_})
        models_added_pmc.append(len(X_))

        X_ = X1 - X3
        print("Models removed PMC:")
        print({models.name for models in X_})
        models_removed_pmc.append(len(X_))

        server_storage_left_pmc.append(es.Storage - utilized_storage(es.X))

        print("=="*50)

        for t in sorted(snapshots):
            start_time = time.time()
            MUMS(snapshots[t],J, es)
            end_time = time.time()
            execution_time_mums.append((end_time - start_time))

        avg_execution_time_mums.append(np.mean(execution_time_mums))
        execution_time_mums.clear()

        print("Models in Cache After MUMS: ")
        print({models.name for models in es.X})
        print("*" * 50)
        X4 = es.X.copy()

        X_ = X4 - X1
        print("Models added MUMS:")
        print({models.name for models in X_})
        models_added_mums.append(len(X_))

        X_ = X1 - X4
        print("Models removed MUMS:")
        print({models.name for models in X_})
        models_removed_mums.append(len(X_))

        server_storage_left_mums.append(es.Storage - utilized_storage(es.X))

        print("==" * 50)

        for t in sorted(snapshots):
            start_time = time.time()
            DynMCS(es, snapshots[t])
            end_time = time.time()
            execution_time_dynmcs.append((end_time - start_time))

        avg_execution_time_dynmcs.append(np.mean(execution_time_mums))
        execution_time_dynmcs.clear()

        print("Models in Cache After DynMCS: ")
        print({models.name for models in es.X})
        print("*" * 50)
        X5 = es.X.copy()

        X_ = X5 - X1
        print("Models added DynMCS:")
        print({models.name for models in X_})
        models_added_dynmcs.append(len(X_))

        X_ = X1 - X5
        print("Models removed DynMCS:")
        print({models.name for models in X_})
        models_removed_dynmcs.append(len(X_))

        server_storage_left_dynmcs.append(es.Storage - utilized_storage(es.X))
        es.X.clear() #Clear cache for next iteration of devices

    plt.figure(1)
    plt.plot(no_of_devices,models_added_dmums,label = "Models Added DMUMS",color="black", marker="o")
    plt.plot(no_of_devices, models_added_pmc, label = "Models Added PMC",color="red", marker="o")
    plt.plot(no_of_devices, models_added_mums, label = "Models Added MUMS",color="green", marker="o")
    plt.plot(no_of_devices, models_added_dynmcs, label = "Models Added DynMCS",color="blue", marker="o")
    plt.xlabel("No of End Devices")
    plt.ylabel("Model Caching Decision")
    plt.title("Model Caching Decision (Models Added) in Dynamic Scenario \n using Greedy Strategy vs PMC vs MUMS vs DynMCS")
    plt.legend()
    plt.savefig('./Results/MCD_Models_Added_DMUMSvsPMCvsMUMSvsDynMCS.png', dpi=300)

    plt.figure(4)
    plt.plot(no_of_devices,models_removed_dmums,label = "Models Removed DMUMS",color="green", marker="o")
    plt.plot(no_of_devices, models_removed_pmc, label = "Models Removed PMC",color="magenta", marker="o")
    plt.plot(no_of_devices, models_removed_mums, label = "Models Removed MUMS",color="blue", marker="o")
    plt.plot(no_of_devices, models_removed_dynmcs, label = "Models Removed DynMCS",color="red", marker="o")
    plt.xlabel("No of End Devices")
    plt.ylabel("Model Caching Decision")
    plt.title("Models Caching Decision (Models Removed) in Dynamic Scenario \n using Greedy Strategy vs PMC vs MUMS vs DynMCS")
    plt.legend()
    plt.savefig('./Results/MCD_Models_Removed_DMUMSvsPMCvsMUMSvsDynMCS.png', dpi=300)

    plt.figure(2)
    plt.plot(no_of_devices, server_storage_left_dmums, color="red",label="DMUMS", linestyle="-.", marker="o")
    plt.plot(no_of_devices, server_storage_left_pmc, color="black",label="PMC", linestyle="-.", marker="o")
    plt.plot(no_of_devices, server_storage_left_mums, color="olive",label="MUMS", linestyle="-.", marker="o")
    plt.plot(no_of_devices, server_storage_left_dynmcs, color="green",label="DynMCS", linestyle="-.", marker="o")
    plt.xlabel("No of End Devices")
    plt.ylabel("Server Storage Left in MBs")
    plt.title("Server Storage Left in Dynamic Scenario \n for DMUMS vs PMC vs MUMS Algorithm vs DynMCS")
    plt.legend()
    plt.savefig("./Results/Server_Storage_Left_DMUMSvsPMCvsMUMSvsDynMCS.png", dpi=300)

    plt.figure(3)
    plt.plot(no_of_devices,avg_execution_time_dmums,label="DMUMS", color="blue", linestyle="-.")
    plt.plot(no_of_devices,avg_execution_time_pmc,label="PMC", color="green", linestyle="-.")
    plt.plot(no_of_devices,avg_execution_time_mums,label="MUMS", color="cyan", linestyle="-.")
    plt.plot(no_of_devices,avg_execution_time_dynmcs,label="DynMCS", color="black", linestyle="-.")
    plt.xlabel("No of End Devices")
    plt.ylabel("Average Execution Time in seconds")
    plt.title("Average Execution Time in DMUMS vs PMC vs MUMS vs DynMCS Algorithm")
    plt.legend()
    plt.savefig('./Results/Average_Execution_Time_DMUMSvsPMCvsMUMSvsDynMCS.png', dpi=300)

    print("Graphs Plotted and Saved!")

    #If u cant see in Graph print the list here
    # print(avg_execution_time_dynmcs)
    # print(models_removed_dynmcs)
    # print(models_removed_dmums)

def simulate_SRA(i: int):

    no_of_devices_inside: list[int] = [] #list of EDs inside server at any time t
    timeline = []

    models_added_mums = []
    models_added_dmums = []
    models_added_dynmcs = []

    models_removed_dmums = []
    models_removed_mums = []
    models_removed_dynmcs = []

    server_util_dmums = []
    server_util_mums = []
    server_util_dynmcs = []


    EDs_in = initialize_EDs(es, i)  # i jitne andar
    EDs_out = initialize_ED_out(es, i)  # i jitne bahar

    NoX = DisCNN(es,
                 EDs_in
                 )  # jitne andar hain unko pehle statically assign karo resources
    X1 = es.X.copy()

    #Base case scenarios/configurations after static resources assignment
    eds = es.EDs
    w  = es.W
    f = es.F
    util = es.Utility

    print("Models Assigned Statically using DisCNN Framework")
    print({models.name for models in es.X})

    snapshots = run(NoX, EDs_out, es, 10)  # run for moving users and dynamic caching decision

    for t in sorted(snapshots):

        no_of_devices_inside.append(len(snapshots[t]))
        timeline.append(t)

        # """
        DMUMS(es, snapshots[t]) #DMUMS Running
        X2 = es.X.copy()

        X_ = X1 - X2 #Comparing Models Added
        models_added_dmums.append(len(X_))
        print(f"Models Added after DMUMS at {t} seconds")
        print({models.name for models in X_})

        X_ = X2 - X1 #Comparing Models Removed
        models_removed_dmums.append(len(X_))
        print(f"Models Removed after DMUMS at {t} seconds")
        print({models.name for models in X_})

        DynSRA(es, snapshots[t])
        print("Dynamic Server Resources Assigned after Running DMUMS")
        server_util_dmums.append(es.Utility) #Server Utility After DMUMS

        X_ = {}

        #Resetting server configurations to base
        es.EDs = eds
        es.W = w
        es.F = f
        es.Utility = util

        MUMS(snapshots[t], J, es) #MUMS Running
        X3 = es.X.copy()

        X_ = X1 - X3
        models_added_mums.append(len(X_))
        print(f"Models Added after MUMS at {t} seconds")
        print({models.name for models in X_})


        X_ = X3 - X1
        models_removed_mums.append(len(X_))
        print(f"Models Removed after MUMS at {t} seconds")
        print({models.name for models in X_})


        DynSRA(es, snapshots[t])
        print("Dynamic Server Resources Assigned after Running MUMS")
        server_util_mums.append(es.Utility)

        X_ = {}

        #Resetting server configurations to base
        es.EDs = eds
        es.W = w
        es.F = f
        es.Utility = util
        es.X = X1 #Reassigning Statically cached so uske comparison main aa sake

        DynMCS(es, snapshots[t])
        X4 = es.X.copy()

        X_ = X1 - X4
        models_added_dynmcs.append(len(X_))
        print(f"Models Added after DynMCS at {t} seconds")
        print({models.name for models in X_})

        X_ = X4 - X1
        models_removed_dynmcs.append(len(X_))
        print(f"Models Removed after DynMCS at {t} seconds")
        print({models.name for models in X_})

        DynSRA(es, snapshots[t])
        print("Dynamic Server Resources Assigned after Running DynMCS")
        server_util_dynmcs.append(es.Utility)

    plt.figure(2)
    plt.plot(timeline, models_added_dmums, color="blue", label="DMUMS")
    plt.plot(timeline, models_added_mums, color = "red", label="MUMS")
    plt.plot(timeline, models_added_dynmcs, color = "green", label = "DynMCS")
    plt.xlabel("Timeline")
    plt.ylabel("Models Added")
    plt.legend()
    plt.title("Models Caching Decision, Models Added (every 0.5s) \n compared to static assignment at t=0")
    plt.savefig("./DMUA2Result/MCD_Models_Added.png", dpi=300)

    plt.figure(3)
    plt.plot(timeline, models_removed_dmums, color="blue", label="DMUMS")
    plt.plot(timeline, models_removed_mums, color = "red", label="MUMS")
    plt.plot(timeline, models_removed_dynmcs, color = "green", label = "DynMCS")
    plt.xlabel("Timeline")
    plt.ylabel("Models Removed")
    plt.legend()
    plt.title("Models Caching Decision, Models Removed(every 0.5s) \n compared to static assignment at t=0")
    plt.savefig("./DMUA2Result/MCD_Models_Removed.png", dpi=300)

    plt.figure(4)
    plt.plot(timeline, server_util_dmums, color="blue", label="DMUMS")
    plt.plot(timeline, server_util_mums, color = "red", label="MUMS")
    plt.plot(timeline, server_util_dynmcs, color = "green", label = "DynMCS")
    plt.xlabel("Timeline")
    plt.ylabel("Server Utilization")
    plt.legend()
    plt.title("Models Caching Decision effect on Server Utility (every 0.5s) \n compared to static assignment at t=0")
    plt.savefig("./DMUA2Result/MCD_Server_Util.png", dpi=300)

    # print("Graphs Plotted and Saved!")
    # """

    #Plot for Mobile Devices in Server with Time
    plt.figure(1)
    plt.plot(timeline, no_of_devices_inside, marker="o", color = "cyan", linestyle="-")
    plt.xlabel("TimeLine")
    plt.ylabel("End Devices inside Server Range")
    plt.title("Movement of EDs inside Edge Server with time (0.5s) interval")
    plt.savefig("./DMUA2Result/EDs_Inside_Edge_Server_Timeline.png", dpi=300)
    print("Graphs Plotted and Saved!")


if __name__ == "__main__":
    # simulate_mcs()
    simulate_SRA(101)