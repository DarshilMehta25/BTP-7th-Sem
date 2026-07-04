from Algos.Classes.EdgeServer import EdgeServer
from Algos.Classes.ED import ED
import pandas as pd
import copy
from MEC.DisCNN import DisCNN
from MEC.HaverSineFormula import HaversineFormula
from typing import List
from MEC.Random_Direction_Model import RandomDirectionModel
from dataclasses import replace
from Algos import test

import threading,time
from _thread import start_new_thread
from MEC.N import initialize_EDs

# Setting Up Location of Edge Server

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
#Server instance defined globally
# print(es)

# Offloaders taken after model caching, utility maximization and resource allocation at t=0
NoX = DisCNN(es)
# print(*NoX)

# print(es) #Server Utility changes as it is passed by reference to DisCNN function

# In DMUA.py

from Algos.test import HaversineFormula

def initiate_handoff(ed: ED, es: EdgeServer) -> bool:
    for state in RandomDirectionModel(ed,es):

        dist = HaversineFormula(state.x, state.y, es.x, es.y)

        if dist > es.coverage_area:
            es.Utility -= ed.price_paid
            # print(ed.price_paid)
            return True

    return False


def spawn_threads(eds_chunk, es_ref, results, barrier, start_index, threads):
    n = len(eds_chunk)

    # Base case
    if n <= 3:
        for j, ed in enumerate(eds_chunk):
            t = threading.Thread(
                target=_simulate_ed,
                args=(start_index + j, ed, es_ref, results, barrier),
                daemon=True
            )
            threads.append(t)
            t.start()
        return

    # Recursive case: split in half
    mid = n // 2
    spawn_threads(eds_chunk[:mid], es_ref, results, barrier, start_index,       threads)
    spawn_threads(eds_chunk[mid:], es_ref, results, barrier, start_index + mid, threads)

import threading
print_lock = threading.Lock()

# def _simulate_ed(index, ed, es_ref, results, barrier):
#     barrier.wait()
#
#     dist = HaversineFormula(ed.x, ed.y, es_ref.x, es_ref.y)
#     with print_lock:
#         print(f"ID: {ed.id} initial distance = {dist}")
#
#     for state in RandomDirectionModel(ed,es):
#         dist = HaversineFormula(ed.x, ed.y, es_ref.x, es_ref.y)
#
#
#         # if dist > es_ref.coverage_area:
#         #     results[index] = (True, ed.price_paid)
#         #     return
#
#     with print_lock:
#         print(f"ID {ed.id} final distance = {dist}")
#         print("--------------------------------------")
#
#     # print("ID",ed.id,"final distance = ", dist)
#     # print("--------------------------------------")
#     results[index] = (False, 0)


print_lock = threading.Lock()

def _simulate_ed(index, ed, es_ref, results, barrier):
    barrier.wait()

    dist1 = HaversineFormula(ed.x, ed.y, es_ref.x, es_ref.y)

    for state in RandomDirectionModel(ed, es_ref):
        dist2 = HaversineFormula(state.x, state.y, es_ref.x, es_ref.y)

    with print_lock:
        print(f"""
ID = {ed.id}
Initial = {dist1}
Final   = {dist2}
-------------------------
""")





def MUA(NoX: List[ED], es_copy: EdgeServer) -> tuple:

    n = len(NoX)

    # threading
    results = [(False, 0)] * n
    threads = []
    barrier = threading.Barrier(n + 1)

    spawn_threads(NoX, es_copy, results, barrier, 0, threads)  # recursive split

    barrier.wait()   # release all threads simultaneously

    for t in threads:
        t.join()     # wait for all to finish

    # tally results
    handoff_count = 0
    offloaded_eds = []

    for i, (did_handoff, price) in enumerate(results):
        if did_handoff:
            handoff_count += 1
            es_copy.Utility -= price
            offloaded_eds.append(NoX[i])

    return es_copy.Utility, handoff_count, offloaded_eds


from MEC import Random_Direction_Model
from MEC.N import initialize_ED_out
import random
def xyz():
    all_eds = NoX + initialize_ED_out(es)
    random.shuffle(all_eds)

    print(len(all_eds))

    utility = []
    offloaders_handoff = []

    time_stamp = []

    for i in range(0,101,10):


        #threading
        #10 -> [1,2,3,4,5,6,7,8,9,10] -> [1,2,3] || [4,5,6] || [7,8] || [9,10]
        #12 -> 6,6 -> 3,3,3,3 -> min = 2 || 3
        #20 -> 10, 10 -> 5, 5, -> 2,3,2,3



        eds = copy.deepcopy(all_eds[:i])
        # print(*eds)
        es_copy = copy.deepcopy(es)

        y_value, handoff_count, offloaded = MUA(eds, es_copy)

        utility.append(float(y_value))
        offloaders_handoff.append(handoff_count)


        # print(f"Devices={i}, Utility={y_value:.2f}, Handoffs={handoff_count}")
    #
    # print("\nUtility:", utility)
    # print("Handoffs per batch:", offloaders_handoff)

    return utility,offloaders_handoff

#
# DMUA.py — do NOT call run() at module level
utility = []
offloaders_handoff = []

# def run():
#     global utility, offloaders_handoff
#     es_copy = copy.deepcopy(es)
#     for i in range(5, 51, 5):
#         eds = copy.deepcopy(NoX[:i])
#         y_value, handoff_count, offloaded = MUA(eds, es_copy)
#         utility.append(float(y_value))
#         offloaders_handoff.append(handoff_count)

if __name__ == "__main__":
    xyz()         # runs only when you execute DMUA.py directly
    # print("run")