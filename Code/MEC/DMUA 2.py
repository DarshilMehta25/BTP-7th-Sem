from MEC.DisCNN import DisCNN
from MEC.N import initialize_EDs, initialize_ED_out
import os
import pandas as pd
from Algos.Classes.EdgeServer import  EdgeServer
from MEC.simulate_global_snapshot_with_time import run
import matplotlib.pyplot as plt


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

no_of_devices = []
models_added = []
models_removed = []

for i in range(10,51,5): #10 ke gap mein EDs initialize honge andar bahar
    no_of_devices.append(i)
    print(f"Devices initialized {i}")

    EDs_in = initialize_EDs(es,i) #i jitne andar
    EDs_out = initialize_ED_out(es,i) #i jitne bahar

    NoX = DisCNN(es,EDs_in) #jitne andar hain unko pehle statically assign karo resources
    X1 = es.X.copy()
    print({models.name for models in es.X})

    run(NoX, EDs_out, es,6) #run for moving users and dynamic caching decision

    print({models.name for models in es.X})
    print("*"*50)
    X2  = es.X.copy()
    X_ = X2 - X1
    print("Models added:")
    print({models.name for models in X_})
    models_added.append(len(X_))

    X_ = X1 - X2
    print("Models removed:")
    print({models.name for models in X_})
    models_removed.append(len(X_))

    print("=="*50)
    es.X.clear() #Clear cache for next iteration of devices

plt.plot(no_of_devices,models_added,label = "Models Added",color="blue", marker="o")
plt.plot(no_of_devices,models_removed,label = "Models Removed",color="green", marker="o")
plt.xlabel("No of Moving Devices")
plt.ylabel("Model Caching Decision")
plt.title("Model Caching Decision in Dynamic Scenario")
plt.legend()
plt.savefig('./Results/MCD.png', dpi=150)