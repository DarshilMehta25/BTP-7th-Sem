from MEC.HaverSineFormula import HaversineFormula
from MEC.N import initialize_EDs, initialize_ED_out
import os
import pandas as pd
from Algos.Classes.EdgeServer import  EdgeServer

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

EDs_in = initialize_EDs(es) #server ki range me ED
EDs_out = initialize_ED_out(es) #server ke bahar

# print(*EDs_in)
# print(es.x,es.y)

#code to confirm that EDs in EDs_out are out of range from server
# for eds in EDs_out:
#     print(HaversineFormula(es.x, eds.x, es.y, eds.y)>es.coverage_area)

#Simlutaneously Move users from inner and outer

