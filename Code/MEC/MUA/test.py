from Algos.Classes.EdgeServer import  EdgeServer
import pandas as pd
from random import randint
import math
from Algos.Classes.ED import ED

#Base file addresses
edge_server_coords_file_path = "./Dataset/site-optus-melbCBD.csv"
user_coords_file_path = "./Dataset/users-melbcbd-generated.csv"

edge_server_data = pd.read_csv(filepath_or_buffer=edge_server_coords_file_path)
users_data = pd.read_csv(filepath_or_buffer=user_coords_file_path) #Already in DF format just have to filter coordinates with server range

edge_server_lats = edge_server_data["LATITUDE"].head(5) #Edge Server Latitude
edge_server_longs = edge_server_data["LONGITUDE"].head(5) #Edge Server Longitude
edge_server_coords = pd.DataFrame((edge_server_lats,edge_server_longs)) #Combined coordinates

# print(users_data)
# print(*edge_server_lats)
# print(*edge_server_longs)
# print(edge_server_coords)

server_lat, server_long = edge_server_coords[0] #Server Coorinates assigned
es = EdgeServer(20,800,1024,server_lat,server_long,500) #coverage area kept 500meters can be changed later as per server configuration

# print(es)
# print(es.coverage_area)
# print(server_lat)
# print(server_long)

def HaversineFormula(x1: float, y1: float, x2: float, y2: float) -> float: #returns distance b/w 2 coordinates in meters

    lat1, lon1, lat2, lon2 = map(math.radians, [x1, y1, x2, y2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    r = 6371.0 #radius of earth
    return c * r * 1000 #multiply with 100 to convert distance to meters

# print(user_lat, user_long)
# print(users_data.iloc[0])
# print(users_data.shape[0])

in_range_user_coords = [] #list of user coordinates within range of server
out_of_range_user_coords = [] #list of user coordinates out or range

for i in range(users_data.shape[0]-1):
    user_lat, user_long = users_data.iloc[i]
    dist = HaversineFormula(user_lat, user_long, server_lat, server_long)

    if(dist <= es.coverage_area):
        in_range_user_coords.append((user_lat, user_long))
    else:
        out_of_range_user_coords.append((user_lat, user_long))

# print(*in_range_user_coords)
# print(*out_of_range_user_coords)

# print(len(in_range_user_coords))
in_range_user_coords = in_range_user_coords[:20] #list size reduces to number of test users
# print(len(in_range_user_coords))

# Flow
# Make a function of random direction where once ED is passed, its coordinates change such that it goes out of range of server within 3-6 seconds to simulate mobile users
# No need to pass user coordinates as it is device position independent
# For using subset of users slice the ED list
# Make ED instances here from ED class
# ED ke instance idhar banadena as per requirement jo bhi attribute dalne ho dal dena abhi coordinates change karne se kaam hain
# This function does not return any value just change user coordinates
# Replace function use karke ED ko har ek baar pura replicate kar na hoga cuz attributes once defined are freezed

def RandomDirectionModel(ed: ED):
    pass

