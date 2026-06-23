from Algos.Classes.EdgeServer import EdgeServer
from Algos.Classes.ED import ED
import pandas as pd
from DisCNN import DisCNN
from HaverSineFormula import HaversineFormula
from typing import List
from dataclasses import replace

import threading
from _thread import start_new_thread

# Setting Up Location of Edge Server

edge_server_coords_file_path = "./MUA/Dataset/site-optus-melbCBD.csv"
edge_server_data = pd.read_csv(filepath_or_buffer=edge_server_coords_file_path)
edge_server_lats = edge_server_data["LATITUDE"].head(5)  # Edge Server Latitude
edge_server_longs = edge_server_data["LONGITUDE"].head(5)  # Edge Server Longitude
edge_server_coords = pd.DataFrame((edge_server_lats, edge_server_longs))  # Combined coordinates

server_lat, server_long = edge_server_coords[0]  # Server Coorinates assigned
es = EdgeServer(20, 800, 1024, server_lat, server_long,500) #Server instance defined globally
# print(es)

# Offloaders taken after model caching, utility maximization and resource allocation at t=0
NoX = DisCNN(es)
# print(*NoX)

# print(es) #Server Utility changes as it is passed by reference to DisCNN function

def handoff_decision(ed: ED, es: EdgeServer):

    if(HaversineFormula(ed.x,ed.y,es.x,es.y) <= es.coverage_area): #calculates distance of the ED from Edge Server
        return False #Handoff not required, if within range of server
    else:
        return True #If ED outside coverage area, then handoff required

def initiate_handoff(ed: ED, es: EdgeServer): #device gone out of server coverage area

   if(handoff_decision(ed,es)):
       es.Utility -= ed.price_paid
       # ed = ed.replace(ed, price_paid = 0)
       return
   else:
       return

max_util = es.Utility
utility = [] #Y axis, values to be populated, not difference between old and new values!!!!
number_of_mobile_devices_from_NoX = [2,4,6,8,10,12,14,16,18,20] #X axis

def MUA(NoX: List[ED], ed:EdgeServer):
    #test file ka logic likhna with help of above 2 functions, eds -> NoX
    #2 nested loop chalegi
    pass

