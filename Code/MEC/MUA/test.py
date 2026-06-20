from Algos.Classes.EdgeServer import  EdgeServer
import pandas as pd
from random import randint

edge_server_data = pd.read_csv(filepath_or_buffer="./Dataset/site-optus-melbCBD.csv")

edge_server_lats = edge_server_data["LATITUDE"].head(3) #Edge Server Latitude
edge_server_longs = edge_server_data["LONGITUDE"].head(3) #Edge Server Longitude
edge_server_coords = pd.DataFrame((edge_server_lats,edge_server_longs)) #Combined coordinates

# print(*edge_server_lats)
# print(*edge_server_longs)
# print(edge_server_coords)

server_lat, server_long = edge_server_coords[randint(0,len(edge_server_coords-1))] #Randomly selects coordinates from given lat long DF
es = EdgeServer(20,800,1024,server_lat,server_long,500)
print(es)
# print(server_lat)
# print(server_long)

def HaversonFormula(x1: float, x2: float, y1: float, y2: float) -> float:
    pass #Returns distance in meters between 2 coordinates

#Flow
# Edge Server ki class mein coordinates randomly assign ho gae hain
# Now from this "users-melbcbd-generated.csv"file, aese users ke coords chahie jo server ke range ke andar ho i.e distance < 500 meters
# Aese users ke coordinates ko list me store karvake baad me ED ke attributes me assign karvana hain
# Distance between 2 coordinates Haverson Formula se nikelage uska code likhdena AI se usme zyada nai hain
# Upar pandas ka function use kiya hain vese hi use karke list me user coords within range and out of range ke 2 alag pandas DF banao isi file mein and commit karo